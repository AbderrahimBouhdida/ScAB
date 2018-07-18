import mainlay
import sys
import os
import time
import dlib
import cv2 as cv
import numpy as np
import requests
from picamera.array import PiRGBArray
from picamera import PiCamera
from PyQt5 import QtCore, QtGui, QtWidgets
from utils import extract_left_eye_center, extract_right_eye_center, get_rotation_matrix, crop_image
import sqlite3
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(2,gpio.OUT)
p=gpio.PWM(2,50)
url = 'url_for_web/single.php'
urlb = 'url_for_web/hb.php'

# initialize the camera and grab a reference to the raw camera capture

camera = PiCamera()
camera.resolution = (421,321)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(421, 321))
time.sleep(0.1)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

lbp_classifier = 'Data/lbpcascade_frontalface.xml'
users_dir = 'Users'
data = 'Data/model.xml'
(im_width, im_height) = (110, 90)
size = 1


class Thread(QtCore.QThread):
	changePixmap = QtCore.pyqtSignal(QtWidgets.QGraphicsPixmapItem)
	status = QtCore.pyqtSignal(str)
	user = QtCore.pyqtSignal(str)

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent=parent)
		self.names, self.model, self.lbp_cascade = self.setup()
		self.working = False
		print(self.names)

	def setup(self):
		model = cv.face.LBPHFaceRecognizer_create()
		model.read(data)
		lbp_cascade = cv.CascadeClassifier(lbp_classifier)
		# Open camera
		# Create a list of images and a list of corresponding names
		names = {}
		id = 0
		for (subdirs, dirs, files) in os.walk(users_dir):

			# Loop through each folder named after the subject in the photos
			for subdir in dirs:
				names[id] = subdir
				id += 1
		return names, model, lbp_cascade
	def temp(self):
		res = os.popen('vcgencmd measure_temp').readline()
		return(res.replace("temp=","").replace("'C\n",""))
	def activate_fan(self):
		p.start(50)
	def deactivate_fan(self):
		p.stop()
	def run(self):
		old = ""
		self.count, self.count_u, confidence = 0, 0, 0
		print("thread is : ", int(self.thread().currentThreadId()))
		local_DB = sqlite3.connect('Data/users.db')
		cur = local_DB.cursor()
		start = time.time()
		while True:
			dur = time.time() - start
			dirty = False
			if dur > 10.0:
				queryb = {'id': 1}
				if float(self.temp()) > 60 :
					self.activate_fan()
				else :
					self.deactivate_fan()
				try:
					res1 = requests.post(urlb, data=queryb)
					#print(res1.text)
					start = time.time()
					print("pulsed")
					# mergeDB()
				except requests.ConnectionError as e:
					print("no connection")
					dirty = True

			while self.working:
				dure = time.clock()
				for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
					# grab the raw NumPy array representing the image, then initialize the timestamp
					# and occupied/unoccupied text
					if (not self.working):
						rawCapture.seek(0)
						rawCapture.truncate(0)
						break
					frame = frame.array

					height, width, channels = frame.shape
					# Convert to grayscalel
					gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

					# Resize to speed up detection (optinal, change size above)
					mini = cv.resize(
						frame, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

					# Detect faces and loop through each one
					# faces = self.lbp_cascade.detectMultiScale(mini, 1.1, 3)
					dets = detector(gray, 1)
					um_faces = len(dets)
					if um_faces == 0:
						self.status.emit("Denied")
						self.user.emit("aucun personne")
					for i, det in enumerate(dets):
						shape = predictor(frame, det)
						left_eye = extract_left_eye_center(shape)
						right_eye = extract_right_eye_center(shape)

						M = get_rotation_matrix(left_eye, right_eye)
						rotated = cv.warpAffine(
							frame, M, (int(width / size), int(height / size)), flags=cv.INTER_CUBIC)

						cropped = crop_image(rotated, det)
						cropped = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
						# Try to recognize the face
						if cropped is None:
							continue
						prediction, confidence = self.model.predict(cropped)
						print(confidence)
						cv.rectangle(frame, (det.left(), det.top()),
									 (det.right(), det.bottom()), (255, 255, 0), 2)
						if confidence < 160:
							# Grant accesss
							cur.execute("SELECT prenom, depatement FROM users WHERE nom = ?",(self.names[prediction],))
							row = cur.fetchone()
							print(row)
							print(prediction)
							if old == self.names[prediction]:
								self.count += 1
								if self.count > 3:
									count = 0
									self.status.emit("Autoriser")
									self.user.emit(
										"Bienvenue, Mr,{}".format(old))
									cur.execute(
										"INSERT INTO log (nom,prenom,departement,date) VALUES (?,?,?,datetime('now'))", (old, row[0], row[1]))
									local_DB.commit()
									query = {'name': old,
											 'prenom': row[0],
											 'departement':row[1]}
									if not dirty:
										res = requests.post(url, data=query)
									self.stop()
							else :
								old = self.names[prediction]
						else:
							self.status.emit("Denied")
							self.user.emit("non reconue")
							self.count_u += 1
							if self.count_u > 5:
								self.count_u = 0
								self.stop()
					# Show the image and check for ESC being pressed
					qtimg = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
					# qtimg = cv.resize(qtimg, dim, interpolation = cv.INTER_AREA)
					image = QtGui.QImage(qtimg, width,
										 height, width * 3, QtGui.QImage.Format_RGB888)
					pixmap = QtGui.QPixmap.fromImage(image)
					pixmap_resized = pixmap.scaled(
						350, 260, QtCore.Qt.KeepAspectRatio)
					pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap)
					self.changePixmap.emit(pixmapItem)
					rawCapture.seek(0)
					rawCapture.truncate(0)
					if (time.clock() - dure) > 20:
						self.stop()
					QtWidgets.QApplication.processEvents()

	def stop(self):
		self.working = False
		# self._isRunning = False

	def st(self):
		self.working = True
		gpio.cleanup()


class Main(QtWidgets.QMainWindow, mainlay.Ui_MainWindow):
	def __init__(self, parent=None):
		super(Main, self).__init__(parent)
		self.setupUi(self)
		# self.threadpool = QtCore.QThreadPool()
		# print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.scene = QtWidgets.QGraphicsScene(self)
		self.preview.setScene(self.scene)

		self.on.clicked.connect(self.start)
		self.th = Thread(self)
		self.th.status.connect(self.handle_message)
		self.th.user.connect(self.handle)
		self.th.changePixmap.connect(self.scene.addItem)
		self.th.start()

	def handle_message(self, message):
		self.status.setText(message)

	def handle(self, message):
		self.user.setText(message)

	def showMenu(self):
		camera.close()
		from gestion_utilisateurs import Manager
		self.Menu = Manager(self)
		self.Menu.show()

	def closeEvent(self, event):
		rawCapture.seek(0)
		rawCapture.truncate(0)
		gpio.cleanup()
		print("Exiting...")
		camera.close()
		self.th.stop()
		event.accept()

	def change_label(self, s):
		print(s)

	def start(self):
		self.th.st()


def main():
	app = QtWidgets.QApplication(sys.argv)
	form = Main()
	form.show()
	print("Main application thread is : ", int(app.thread().currentThreadId()))
	app.exec_()


if __name__ == '__main__':

	main()
