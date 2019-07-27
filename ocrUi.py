#coding:utf-8
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, cgitb, cv2, os
from Model import videocap, Leven_dist
from Model.detector import detector
import Global_Var
import os
import numpy as np

# 引入下面这句话界面部分报错时不会卡住
cgitb.enable( format = 'text')
Global_Var._init()

# 直接引用Qt Designer生成的UI文件，不需要将ui文件转换成py文件
Ui_MainWindow, QtbaseClass_0 = uic.loadUiType("./ocr.ui")

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.threadUnlock = Thread_unlock()
        self.threadUnlock.unlock_Siganl.connect(self.unlockResult)
        self.threadUnlock.unlocklist_Siganl.connect(self.unlocklistResult)

        self.threadReco = Thread_reco()
        self.threadReco.reco_Siganl.connect(self.recoResult)

    @pyqtSlot()
    def on_pushButton_selectFile_clicked(self):
        pass
        print('testing')
        imagePath = QFileDialog.getOpenFileName(self, 'open file', '/')[0]
        if imagePath:
            print(imagePath)
            self.threadUnlock.setVideoPath(imagePath)
            self.lineEdit_videoPath.setText(imagePath)

    @pyqtSlot()
    def on_pushButton_Unlock_clicked(self):
        pass
        imagePath = QtWidgets.QFileDialog.getExistingDirectory()
        if imagePath:
            print(imagePath)
            self.threadUnlock.setOutputPath(imagePath)
            self.textEdit_unlock.append('output frames...')
            self.threadUnlock.start()

    @pyqtSlot()
    def on_pushButton_chooseFrame_clicked(self):
        pass
        imagePath = QFileDialog.getOpenFileName(self, 'open file', '/')[0]
        if imagePath:
            self.showImage(self.label_origin, imagePath)
            self.framePath = imagePath

    @pyqtSlot()
    def on_pushButton_recognize_clicked(self):
        pass
        if self.framePath:
            self.threadReco.setPath(self.framePath)
            self.threadReco.start()

    @pyqtSlot()
    def on_pushButton_editDistance_clicked(self):
        outputStr = self.textEdit_output.toPlainText()
        inputStr = self.textEdit_input.toPlainText()
        distance = Leven_dist.normal_leven(outputStr, inputStr)
        self.lineEdit_distance.setText(str(distance))


    def showImage(self, labelName, imagePath):
        QPimg= QPixmap(imagePath)
        Position = labelName.geometry()
        scaredPixmap = QPimg.scaled(Position.width(),
                                            Position.height())
        labelName.setPixmap(scaredPixmap)
        labelName.setScaledContents(True)

    def unlockResult(self, result):
        self.textEdit_unlock.append(result)

    def unlocklistResult(self, textlist):
        for item in textlist:
            self.textEdit_output.append(item)


    def recoResult(self, text):
        img = Global_Var.Get_value('img')
        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.QtImg = QImage(self.img_rgb.data, self.img_rgb.shape[1], self.img_rgb.shape[0],
                                  QImage.Format_RGB888)
        QPimg= QPixmap(self.QtImg)
        Position = self.label_after.geometry()
        scaredPixmap = QPimg.scaled(Position.width(),
                                            Position.height())
        self.label_after.setPixmap(scaredPixmap)
        self.label_after.setScaledContents(True)
        self.lineEdit_info.setText(text)
        self.textEdit_output.append(text)




class Thread_unlock(QThread):
    unlock_Siganl = pyqtSignal(str)
    unlocklist_Siganl = pyqtSignal(list)
    def __int__(self):
        super(Thread_unlock, self).__init__()

    def run(self):
        self.outputPath += '/'
        videocap.unlock_mv(self.videoPath, self.outputPath)
        self.unlock_Siganl.emit('success unlocking')
        self.unlock_Siganl.emit('text extracting...')
        lists = os.listdir(self.outputPath)
        print(lists)
        for i in lists:
            if i == '.DS_Store':
                lists.remove(i)
        lists.sort(key=lambda x: int(x[:-4]))
        print(lists)
        textlist = []
        de = detector()
        for item in lists:
            if item.split('.')[-1] == 'jpg':
                print(item)
                img, text = de.detector(self.outputPath + '/' + item)
                textlist.append(text)
        # print(textlist)
        ordered_textlist = list(set(textlist))
        ordered_textlist.sort(key=textlist.index)
        print(ordered_textlist)
        self.unlocklist_Siganl.emit(ordered_textlist)
        self.unlock_Siganl.emit('extract end!')


    def setVideoPath(self, path):
        self.videoPath = path

    def setOutputPath(self, path):
        self.outputPath = path

class Thread_reco(QThread):
    reco_Siganl = pyqtSignal(str)
    def __int__(self):
        # 初始化函数，默认
        super(Thread_reco, self).__init__()

    def run(self):
        de = detector()
        img, text= de.detector(self.framePath)
        Global_Var.Set_value('img', img)
        self.reco_Siganl.emit(text)

    def setPath(self, path):
        self.framePath = path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    #ui.showMaximized()
    ui.show()
    sys.exit(app.exec_())
