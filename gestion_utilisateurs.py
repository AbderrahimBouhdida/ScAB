import gestion
import sys
import os
import time
import dlib
import cv2 as cv
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from shutil import rmtree
from picamera.array import PiRGBArray
from picamera import PiCamera
import sqlite3
from utils import extract_left_eye_center, extract_right_eye_center, get_rotation_matrix, crop_image
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (352, 272)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(352, 272))
time.sleep(0.1)


lbp_classifier_face = 'Data/lbpcascade_frontalface.xml'
users_dir = 'Users'
data = 'Data/model.xml'

(im_width, im_height) = (110, 90)
size = 1


class Manager(QtWidgets.QMainWindow, gestion.Ui_MainWindow):
	closed = False

	def __init__(self, parent=None):
		super(Manager, self).__init__(parent)
		#usernames = sorted(self.names())
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.scene = QtWidgets.QGraphicsScene(self)
		self.preview.setScene(self.scene)
		self.train.clicked.connect(self.on_click_train)
		self.add.clicked.connect(self.on_click_add)
		self.delete_2.clicked.connect(self.on_click_del)
		self.stop.clicked.connect(self.on_click_stop)
		self.local_DB = sqlite3.connect('Data/users.db')
		self.cur = self.local_DB.cursor()
		self.names()
		self.log()
		image = QtGui.QImage('camera.png')
		pixmap = QtGui.QPixmap.fromImage(image)
		pixmap_resized = pixmap.scaled(350, 260, QtCore.Qt.KeepAspectRatio)
		pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap_resized)
		self.scene.addItem(pixmapItem)
		self.trained = True
		self.changed = False

	def closeEvent(self, event):
		self.on_click_stop()
		try:
			self.local_DB.close()
		except :
			print("already closed")
		if self.changed:
			if not self.trained:
				self.on_click_train()
		event.accept()

	def on_click_stop(self):
		self.working = False
		rawCapture.seek(0)
		rawCapture.truncate(0)

	def on_click_add(self):
		nom = self.user_nom.text()
		prenom = self.user_prenom.text()
		departement = str(self.user_departement.currentText())
		rowPosition = self.tableWidget.rowCount()
		print(rowPosition)
		self.cur.execute("SELECT (id) FROM users WHERE nom= ? AND prenom = ? AND depatement = ?" , (nom, prenom, departement))
		numrows = self.cur.fetchall()
		if len(numrows) == 0:
			self.cur.execute("INSERT INTO users (id,nom,prenom,depatement) VALUES (?,?,?,?)" , (rowPosition,nom,prenom,departement))
			self.local_DB.commit()
			self.tableWidget.insertRow(rowPosition)
			self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(nom))
			self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(prenom))
			self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(departement))
		self.user_nom.clear()
		self.user_prenom.clear()
		self.capture(str(rowPosition), nom)
		self.trained = False
		self.changed = True

	def on_click_del(self):

		self.local_DB.commit()
		# self.on_click_train()
		self.trained = False

	def on_click_clear_log(self):
		self.log.setText('')

	def log(self):
		while (self.tableWidget_2.rowCount() > 0) :
			self.tableWidget_2.removeRow(0)
		self.cur.execute("SELECT * FROM log")
		numrows = self.cur.fetchall()
		# Get and display one row at a time
		for row in numrows:
			rowPosition = self.tableWidget.rowCount()
			print(rowPosition)
			self.tableWidget_2.insertRow(rowPosition-3)
			self.tableWidget_2.setItem(rowPosition-3, 0, QtWidgets.QTableWidgetItem(row[1]))
			self.tableWidget_2.setItem(rowPosition-3, 1, QtWidgets.QTableWidgetItem(row[2]))
			self.tableWidget_2.setItem(rowPosition-3, 2, QtWidgets.QTableWidgetItem(row[3]))
			self.tableWidget_2.setItem(rowPosition-3, 3, QtWidgets.QTableWidgetItem(row[4]))
	
	def names(self):
		while (self.tableWidget.rowCount() > 0) :
			self.tableWidget.removeRow(0)
		self.cur.execute("SELECT * FROM users")
		numrows = self.cur.fetchall()
		# Get and display one row at a time
		for row in numrows:
			print(row[1])
			self.tableWidget.insertRow(row[0])
			self.tableWidget.setItem(row[0], 0, QtWidgets.QTableWidgetItem(row[1]))
			self.tableWidget.setItem(row[0], 1, QtWidgets.QTableWidgetItem(row[2]))
			self.tableWidget.setItem(row[0], 2, QtWidgets.QTableWidgetItem(row[3]))
	
	
	def delete(self, name):
		try:
			user_name = name
		except SyntaxError:
			print("Invalid name")
			sys.exit(0)
		path = os.path.join(users_dir, user_name)
		if not os.path.isdir(path):
			print("{0} not found in db".format(user_name))
			return False
			sys.exit(0)
		for subdirs, dirs, files in os.walk(users_dir):
			for subdir in dirs:
				if subdir == user_name:
					rmtree(path)
					print("deleted {0}".format(user_name))
					break
		return True

	def capture(self, id, name):
		try:
			user_name = name
			id = id
		except:
			print("Vous devez entrer un nom")
		path = os.path.join(users_dir, user_name)
		if not os.path.isdir(path):
			os.mkdir(path)
		# Generate name for image file
		pin = sorted([int(n[:n.find('.')]) for n in os.listdir(path)
					  if n[0] != '.'] + [0])[-1] + 1
		print("Le programmes va capturer 20 images. \
		\nDeplacez votre tete pour augmenter la precision pendant le fonctionnement.\n")

		# The program loops until it has 20 images of the face.
		count = 0
		pause = 0
		t = 0
		count_max = 20
		# Loop until the camera is working

		# Loop until the camera is working
		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

			if count >= count_max:
				rawCapture.seek(0)
				rawCapture.truncate(0)
				break

			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			frame = frame.array

			# Get image size
			height, width, channels = frame.shape
			r = 100.0 / width
			dim = (100, int(height * r))

			# Flip frame
			frame = cv.flip(frame, 1, 0)

			# Convert to grayscale
			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

			# Detect faces
			dets = detector(frame, 1)

			for i, det in enumerate(dets):
				shape = predictor(frame, det)
				left_eye = extract_left_eye_center(shape)
				right_eye = extract_right_eye_center(shape)

				M = get_rotation_matrix(left_eye, right_eye)
				rotated = cv.warpAffine(frame, M, (width, height), flags=cv.INTER_CUBIC)

				cropped = crop_image(rotated, det)
				cv.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), (255, 255, 0), 2)


				# Remove false positives

				if(False):
					print("Non claire")
				else:
					# To create diversity, only save every fith detected image
					if(pause == 0):
						print("enregistrement de la capture "+str(count+1)+"/"+str(count_max))

						# Save image file
						cv.imwrite('%s/%s.png' % (path, pin), cropped)
						pin += 1
						count += 1
						pause = 1

			if(pause > 0):
				pause = (pause + 1) % 3
			qtimg = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
			#qtimg = cv.resize(qtimg, dim, interpolation = cv.INTER_AREA)
			image = QtGui.QImage(qtimg, width,
								 height, width * 3, QtGui.QImage.Format_RGB888)
			pixmap = QtGui.QPixmap.fromImage(image)
			pixmap_resized = pixmap.scaled(350, 260, QtCore.Qt.KeepAspectRatio)
			pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap_resized)
			if count == count_max:
				image = QtGui.QImage('camera.png')
				pixmap = QtGui.QPixmap.fromImage(image)
				pixmap_resized = pixmap.scaled(
					350, 260, QtCore.Qt.KeepAspectRatio)
				pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap_resized)
			self.scene.addItem(pixmapItem)
			rawCapture.seek(0)
			rawCapture.truncate(0)
			QtWidgets.QApplication.processEvents()
			key = cv.waitKey(10)

			if key == 27:
				break
		image = QtGui.QImage('/camera.png')
		idle = QtGui.QPixmap.fromImage(image)
		idle_resized = pixmap.scaled(350, 260, QtCore.Qt.KeepAspectRatio)
		pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap_resized)
		self.scene.addItem(pixmapItem)
		cv.destroyAllWindows()
		QtWidgets.QApplication.processEvents()

	def on_click_train(self):
		print('Training...')
		(images, lables, names, id) = ([], [], {}, 0)
		for (subdirs, dirs, files) in os.walk(users_dir):

			# Loop through each folder named after the subject in the photos
			for subdir in dirs:
				names[id] = subdir
				user = os.path.join(users_dir, subdir)
				# Loop through each photo in the folder
				for filename in os.listdir(user):

					# Skip non-image formates
					f_name, f_extension = os.path.splitext(filename)
					if(f_extension.lower() not in
							['.png', '.jpg', '.jpeg', '.gif', '.pgm']):
						print(filename + " n'est pas une image")
						continue
					path = user + '/' + filename
					lable = id

					# Add to training data
					images.append(cv.imread(path, 0))
					lables.append(int(lable))
				id += 1

		# Create a np array from the two lists above
		(images, lables) = [np.array(lis) for lis in [images, lables]]

		# Create LBP Face recoggnizer and save data
		model = cv.face.LBPHFaceRecognizer_create()
		model.train(images, lables)
		model.write(data)
		self.trained = True
		print("training complete")


def main():
	app = QtWidgets.QApplication(sys.argv)
	form = Manager()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()
