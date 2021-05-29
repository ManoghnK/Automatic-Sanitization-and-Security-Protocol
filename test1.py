import cv2
import numpy as np
import os,sys,time
import random
from keras.models import load_model
from firebase import firebase

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# firebase= firebase.FirebaseApplication("https://maskdetection-81460-default-rtdb.firebaseio.com/",None)
firebaseDB = firebase.FirebaseApplication("https://assp-server-c10wn-default-rtdb.firebaseio.com/sensors", None)
# firebaseRef = db.reference("https://assp-efa06-default-rtdb.europe-west1.firebasedatabase.app/sensors")
status = 'No Mask'
temp=98 #temporary temperature
sansta=0 #sanitization status
sanitization='Not Sanitized'
model=load_model("C:\\Users\\rohit\\model2-002.model")

results={0:'without mask',1:'mask'}
GR_dict={0:(0,0,255),1:(0,255,0)}
mask_on= False
rect_size = 4
cap = cv2.VideoCapture(0) 

haarcascade = cv2.CascadeClassifier('C:\\Users\\rohit\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
start_time = 0

while True:
    (rval, im) = cap.read()
    im=cv2.flip(im,1,1) 

    
    rerect_size = cv2.resize(im, (im.shape[1] // rect_size, im.shape[0] // rect_size))
    faces = haarcascade.detectMultiScale(rerect_size)
    for f in faces:
        (x, y, w, h) = [v * rect_size for v in f] 
        
        face_img = im[y:y+h, x:x+w]
        rerect_sized=cv2.resize(face_img,(150,150))
        normalized=rerect_sized/255.0
        reshaped=np.reshape(normalized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)
        
        mask_on=np.argmax(result,axis=1)[0]
      
        cv2.rectangle(im,(x,y),(x+w,y+h),GR_dict[mask_on],2)
        cv2.rectangle(im,(x,y-40),(x+w,y),GR_dict[mask_on],-1)
        cv2.putText(im, results[mask_on], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    cv2.imshow('Mask Detect',im)
    key = cv2.waitKey(10)
    if not mask_on :
        start_time = time.time()
        print("No mask")
        st = status
    if mask_on and (time.time() - start_time > 3):
        print("Mask detected")
        st = status.replace('No Mask', 'Masked')
        break
    #print(st)
    temp=random.randint(95,105)
    #print(temp)
    sansta=random.randint(0,1)
    #print(sansta)
    if sansta==1:
        x=sanitization.replace('Not Sanitized','Sanitized')
    else:
        x=sanitization
    #print(x)
    data = {
        'Mask On': st == 'Masked',
        'Temp': temp,
        'Fever': temp not in range(97, 102),
        'Hands Sanitized': x == 'Sanitized',
        'RFID': True
        }

    key = cv2.waitKey()
    if key == 27: 
        break

cap.release()
cv2.destroyAllWindows()
# current = firebaseRef.get()
# print(current)
# result = firebaseDB.post('/sensors', data)
result = firebaseDB.put('/sensors','Mask On',st == 'Masked')
result = firebaseDB.put('/sensors','Temperature',98.6)
result = firebaseDB.put('/sensors','Fever',False)
result = firebaseDB.put('/sensors','Hands Sanitized',False)
result = firebaseDB.put('/sensors','RFID', False)


sanitized = False
temperature = 98.6
fever = False
maskOn = True
RFIDauth = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 618)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.maskLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.maskLabel.setFont(font)
        self.maskLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.maskLabel.setObjectName("maskLabel")
        self.gridLayout.addWidget(self.maskLabel, 3, 0, 1, 1)
        self.tempLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.tempLabel.setFont(font)
        self.tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tempLabel.setObjectName("tempLabel")
        self.gridLayout.addWidget(self.tempLabel, 2, 0, 1, 1)
        self.RFIDLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.RFIDLabel.setFont(font)
        self.RFIDLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RFIDLabel.setObjectName("RFIDLabel")
        self.gridLayout.addWidget(self.RFIDLabel, 5, 0, 1, 1)
        self.HSLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.HSLabel.setFont(font)
        self.HSLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.HSLabel.setObjectName("HSLabel")
        self.gridLayout.addWidget(self.HSLabel, 1, 0, 1, 1)
        self.HSStatus = QtWidgets.QLabel(self.centralwidget)
        self.HSStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.HSStatus.setObjectName("HSStatus")
        self.gridLayout.addWidget(self.HSStatus, 1, 1, 1, 1)
        self.tempStatus = QtWidgets.QLabel(self.centralwidget)
        self.tempStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.tempStatus.setObjectName("tempStatus")
        self.gridLayout.addWidget(self.tempStatus, 2, 1, 1, 1)
        self.maskStatus = QtWidgets.QLabel(self.centralwidget)
        self.maskStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.maskStatus.setObjectName("maskStatus")
        self.gridLayout.addWidget(self.maskStatus, 3, 1, 1, 1)
        self.RFIDStatus = QtWidgets.QLabel(self.centralwidget)
        self.RFIDStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.RFIDStatus.setObjectName("RFIDStatus")
        self.gridLayout.addWidget(self.RFIDStatus, 5, 1, 1, 1)
        self.tempBool = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tempBool.sizePolicy().hasHeightForWidth())
        self.tempBool.setSizePolicy(sizePolicy)
        self.tempBool.setCheckable(True)
        self.tempBool.setObjectName("tempBool")
        self.gridLayout.addWidget(self.tempBool, 2, 2, 1, 1)
        self.maskBool = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maskBool.sizePolicy().hasHeightForWidth())
        self.maskBool.setSizePolicy(sizePolicy)
        self.maskBool.setCheckable(True)
        self.maskBool.setChecked(True)
        self.maskBool.setObjectName("maskBool")
        self.gridLayout.addWidget(self.maskBool, 3, 2, 1, 1)
        self.HSBool = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HSBool.sizePolicy().hasHeightForWidth())
        self.HSBool.setSizePolicy(sizePolicy)
        self.HSBool.setCheckable(True)
        self.HSBool.setObjectName("HSBool")
        self.gridLayout.addWidget(self.HSBool, 1, 2, 1, 1)
        self.RFIDBool = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RFIDBool.sizePolicy().hasHeightForWidth())
        self.RFIDBool.setSizePolicy(sizePolicy)
        self.RFIDBool.setCheckable(True)
        self.RFIDBool.setObjectName("RFIDBool")
        self.gridLayout.addWidget(self.RFIDBool, 5, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.HSBool.clicked.connect(self.toggleHS)
        self.tempBool.clicked.connect(self.toggleTemp)
        self.maskBool.clicked.connect(self.toggleMask)
        self.RFIDBool.clicked.connect(self.toggleRFID)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.maskLabel.setText(_translate("MainWindow", "Mask On"))
        self.tempLabel.setText(_translate("MainWindow", "Thermometer"))
        self.RFIDLabel.setText(_translate("MainWindow", "RFID"))
        self.HSLabel.setText(_translate("MainWindow", "Hand Sanitizer"))
        self.HSStatus.setText(_translate("MainWindow", "Not sanitized"))
        self.tempStatus.setText(_translate("MainWindow", "No Fever. Temp: 98.6ºF"))
        self.maskStatus.setText(_translate("MainWindow", "Mask is on"))
        self.RFIDStatus.setText(_translate("MainWindow", "Not authorized"))
        self.tempBool.setText(_translate("MainWindow", "Generate random temperature"))
        self.maskBool.setText(_translate("MainWindow", "Toggle mask"))
        self.HSBool.setText(_translate("MainWindow", "Activate dispenser"))
        self.RFIDBool.setText(_translate("MainWindow", "Scan RFID"))

    def toggleHS(self):
        global sanitized
        if not self.HSBool.isChecked():
            self.HSBool.setChecked(False)
            self.HSStatus.setText("Not sanitized")
            self.HSBool.setText("Activate dispenser")
            sanitized = False
            
        else:
            self.HSBool.setChecked(True)
            self.HSStatus.setText("Sanitized")
            self.HSBool.setText("Deactivate dispenser")
            sanitized = True
        result = firebaseDB.put('/sensors','Hands Sanitized',sanitized)    

    def toggleTemp(self):
        global temperature, fever
        if not self.tempBool.isChecked():
            self.tempBool.setChecked(False)
            temperature = random.randrange(968, 1002)/10
            self.tempStatus.setText("No Fever. Temperature: " + str(temperature) + "ºF")
            fever = False

        else:
            self.tempBool.setChecked(True)
            temperature = random.randrange(1002, 1040)/10
            self.tempStatus.setText("Fever. Temperature: " + str(temperature) + "ºF")
            fever = True
        result = firebaseDB.put('/sensors','Temperature',temperature)
        result = firebaseDB.put('/sensors','Fever',fever)

    def toggleMask(self):
        global maskOn
        if not self.maskBool.isChecked():
            self.maskBool.setChecked(False)
            self.maskStatus.setText("No Mask")
            maskOn = False
        else:
            self.maskBool.setChecked(True)
            self.maskStatus.setText("Mask is on")
            maskOn = True
        result = firebaseDB.put('/sensors','Mask On',maskOn)

    def toggleRFID(self):
        global RFIDauth
        if not self.RFIDBool.isChecked():
            self.RFIDBool.setChecked(False)
            self.RFIDStatus.setText("Not authorized")
            RFIDauth = False
        else:
            self.RFIDBool.setChecked(True)
            self.RFIDStatus.setText("Authorized")
            RFIDauth = True
        result = firebaseDB.put('/sensors','RFID', RFIDauth)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
