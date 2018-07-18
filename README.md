# Biometric Security Access 

An autonomous access control system with the IoT concept on a Raspberry Pi that uses facial recognition for user identification

## Dependencies
- Python 3.6
- PyQt 5
- Dlib
- OpenCV 3
- PiCamera
- RPi.GPIO

Download  [*shape_predictor_68_face_landmarks.dat*](https://sourceforge.net/projects/dclib/files/dlib/v18.10/shape_predictor_68_face_landmarks.dat.bz2/download)and put it inside the Data folder 

## Description

The system has 3 interfaces:
- Administrator interface: an interface that is used to manage the members to allow and to see the log of use
  ![Admin](https://raw.githubusercontent.com/AbderrahimBouhdida/ScAB/master/sc/admin.jpg?token=AKCLWUCG4ELxT8TYTH1DX5ki3zbyrPUuks5bWJWNwA%3D%3D)

- user interface: this is the main interface that allows the recognition and identification of members
  ![user](https://raw.githubusercontent.com/AbderrahimBouhdida/ScAB/master/sc/user.jpg?token=AKCLWXKP0Lx-ijK-gGQpEPnbrtK4mOSHks5bWJVswA%3D%3D)
  
- Web interface: a website that allows the administrator to view the system status and usage log from any location
  ![Web](https://raw.githubusercontent.com/AbderrahimBouhdida/ScAB/master/sc/web1.jpg?token=AKCLWdallMyc_gKrKStM_QHwN8oEMwNpks5bWJVRwA%3D%3D)
  ![Web](https://raw.githubusercontent.com/AbderrahimBouhdida/ScAB/master/sc/web2.jpg?token=AKCLWWNeQwGeT_agAD8ArKq3HyRCFzL9ks5bWJUxwA%3D%3D)
