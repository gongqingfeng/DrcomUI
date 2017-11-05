# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys, time, platform, os
from M_Dialog import AboutDialog
from DrcomThread import LoginedFlagThread
from Failed import FailedWindow
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
username = ""
password = ""
rememberpassword = False
autologin = False

absPath = ""
class LoginingWindow(QMainWindow):
	def __init__(self,parent=None):
		global username, password, rememberpassword, autologin, firstFlag
		super(LoginingWindow,self).__init__(parent)
		self.resize(425,300) #设置窗口大小
		self.setWindowTitle(self.tr("登陆中..."))
		getRealPath()
		#设置图标
		micon = QtGui.QIcon() 
		micon.addPixmap(QtGui.QPixmap(changePath("images/python_128px.ico")),
			QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(micon)
		#禁止最大化按钮
		self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowMinMaxButtonsHint | 
			QtCore.Qt.WindowMinimizeButtonHint) 
		#禁止拉伸窗口大小  
		self.setFixedSize(self.width(), self.height())

		#系统托盘
		self.tray = QtGui.QSystemTrayIcon()
		self.trayIcon = QtGui.QIcon(changePath("images/python_128px.ico"))
		self.tray.setIcon(self.trayIcon)
		self.tray.show()
		# 在系统托盘区域的图标被点击就会触发activated连接的函数
		self.tray.activated.connect(self.trayclick)
		self.tray_menu = QtGui.QMenu(QApplication.desktop()) #创建菜单  
		self.RestoreAction = QAction(u'显示主界面 ', self, triggered=self.showNormal) #添加一级菜单动作选项(还原主窗口)  
		self.AboutAction = QAction(u'关于', self, triggered=self.aboutMe) #添加一级菜单关于选项
		self.QuitAction = QAction(u'退出', self, triggered=qApp.quit) #添加一级菜单动作选项(退出程序)  
		self.tray_menu.addAction(self.RestoreAction) #为菜单添加动作  
		self.tray_menu.addAction(self.AboutAction) 
		self.tray_menu.addAction(self.QuitAction)  
		self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单

		#主布局
		self.mainLayout=QVBoxLayout()
		self.widget = QtGui.QWidget()
		self.widget.setLayout(self.mainLayout)
		self.setCentralWidget(self.widget)

		#顶级布局
		self.topLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.topLayout)
		self.bannerLabel=QLabel()
		self.banner=QPixmap(changePath("images/huxi.jpg"))
		self.bannerLabel.setPixmap(self.banner)
		self.topLayout.addWidget(self.bannerLabel)
		
		#底级布局
		self.bottomLayout = QGridLayout()
		self.mainLayout.addLayout(self.bottomLayout)

		#头像
		self.iconLabel=QLabel() 
		self.icon=QPixmap(changePath("images/python_72px.ico"))
		self.iconLabel.setPixmap(self.icon)
		self.iconLabel.resize(self.icon.width(),self.icon.height())
		self.bottomLayout.addWidget(self.iconLabel, 0, 0, Qt.AlignHCenter)

		#账号显示
		self.usernameLabel = QLabel()
		self.bottomLayout.addWidget(self.usernameLabel, 1, 0, Qt.AlignHCenter)

		#取消按钮
		self.redoPushButton=QPushButton(self.tr("取消"))
		self.bottomLayout.addWidget(self.redoPushButton, 2, 0, Qt.AlignHCenter)

		self.show()

		#信号与槽
		self.connect(self.redoPushButton,QtCore.SIGNAL('clicked()'),self.redoWindow)


	def trayclick(self,res):
		if res == QSystemTrayIcon.DoubleClick:
			self.tray.showMessage(u"提示",u"客户端处于最小化",icon=1)

	def aboutMe(self):
		self.aboutDialog = AboutDialog()
		self.aboutDialog.setModal(True)   #此处ture为模态，false为非模态 ,模态时原窗口不可点击
		self.aboutDialog.show()

	def closeCurrentWindow(self):
		self.setVisible(False)
		self.tray.setVisible(False)

	def setSavedWindow(self, savedWindow):
		self.savedWindow = savedWindow

	def getSavedWindow(self):
		return self.savedWindow 

	def redoWindow(self):
		#通知线程不要发送超时信息
		self.loginedFlagThread.setRedoFlag(True)
		#登陆界面和托盘出现
		self.savedWindow.showCurrentWindow()
		#自己和托盘消失
		self.closeCurrentWindow()

	def loginedDetect(self):
		self.usernameLabel.setText(self.savedWindow.usernameLineEdit.text())
		#启动检测登陆超时线程
		self.loginedFlagThread = LoginedFlagThread()
		self.loginedFlagThread.start()
		#绑定信号与槽
		self.loginedFlagThread.failedSignal.connect(self.loginedFailed)
		#避免点取消后再登陆无法检测超时问题
		self.loginedFlagThread.setRedoFlag(False)

	def loginedFailed(self, signal):
		self.loginedFlag = signal
		if self.loginedFlag == True:
			#登陆失败
			#失败界面和托盘出现
			self.failedWindow = FailedWindow()
			#并将自己传递过去
			self.failedWindow.setSavedWindow(self)
			#当前界面和托盘消失
			self.closeCurrentWindow()
def getRealPath():
	global absPath
	if platform.system() == "Windows":
		absPath = os.path.dirname(os.path.realpath(sys.argv[0])).decode('gbk').encode('utf-8')
		#print absPath
	else:
		absPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		#print absPath

def changePath(path):
	global absPath
	if platform.system() == "Windows":
		path = absPath + "\\" + path
		#print path
	else:
		path = absPath + "/" + path
		#print path
	return path			

def main():
	app=QApplication(sys.argv)
	#登陆中界面
	loginingWindow=LoginingWindow()
	app.exec_()	
if __name__ == '__main__':
	main()