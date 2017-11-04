# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys, time, platform, os
from M_Dialog import AboutDialog, SetupDialog
from DrcomThread import LoginThread
from Run import MainWindow
from Logining import LoginingWindow
from random import randint
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
username = ""
password = ""
rememberpassword = False
autologin = False
loginThread = None
mainWindow = None
loginingWindow =  None
absPath = ""
class LoginWindow(QMainWindow):
	def __init__(self,parent=None):
		global username, password, rememberpassword, autologin
		super(LoginWindow,self).__init__(parent)
		self.resize(425,300) #设置窗口大小
		self.setWindowTitle(self.tr("校园网登陆客户端python版"))
		#设置图标
		self.micon = QtGui.QIcon()
		if os.path.exists(changePath("images\python_128px.ico")):
			print "exists"
		else:
			print "not exists"
		self.micon.addPixmap(QtGui.QPixmap(changePath("images\python_128px.ico")),
			QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(self.micon)
		#禁止最大化按钮
		self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowMinMaxButtonsHint | 
			QtCore.Qt.WindowMinimizeButtonHint) 
		#禁止拉伸窗口大小  
		self.setFixedSize(self.width(), self.height())

		#系统托盘
		self.tray = QtGui.QSystemTrayIcon()
		self.trayIcon = QtGui.QIcon(changePath("images\python_128px.ico"))
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
		self.banner=QPixmap(changePath("images\huxi.jpg"))
		self.bannerLabel.setPixmap(self.banner)
		self.topLayout.addWidget(self.bannerLabel)
		
		#底级布局
		self.bottomLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.bottomLayout)

		#登陆布局
		self.loginLayout = QHBoxLayout()
		self.bottomLayout.addLayout(self.loginLayout)
		self.loginLayout.setMargin(20)
		#头像
		self.iconLabel=QLabel()
		self.icon=QPixmap(changePath("images\python_72px.ico"))
		self.iconLabel.setPixmap(self.icon)
		self.iconLabel.resize(self.icon.width(),self.icon.height())
		self.loginLayout.addWidget(self.iconLabel)

		#登陆选项布局
		self.loginOptionsLayout = QGridLayout()
		self.loginLayout.addLayout(self.loginOptionsLayout)

		self.labelCol=0
		self.contentCol=1

		#用户名
		self.passwordLabel = QLabel(self.tr("username:"))
		self.usernameLineEdit=QLineEdit()	 
		self.loginOptionsLayout.addWidget(self.passwordLabel,0,self.labelCol)
		self.loginOptionsLayout.addWidget(self.usernameLineEdit,0,self.contentCol)

		#密码
		self.passwordLabel = QLabel(self.tr("password:"))
		self.passwordLineEdit=QLineEdit()
		self.passwordLineEdit.setEchoMode(QLineEdit.Password)
		self.passwordLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
		self.loginOptionsLayout.addWidget(self.passwordLabel,1,self.labelCol)
		self.loginOptionsLayout.addWidget(self.passwordLineEdit,1,self.contentCol)

		#options布局
		self.optionsLayout =  QHBoxLayout()
		self.loginOptionsLayout.addLayout(self.optionsLayout,2,1)

		#记住密码
		self.rememberPasswordBox = QCheckBox(self.tr("记住密码"),self)
		self.optionsLayout.addWidget(self.rememberPasswordBox)

		self.optionsLayout.addStretch(5) #剩下空白部分的按比例分布

		#自动登陆
		self.autoLoginBox = QCheckBox(self.tr("自动登陆"),self)
		self.optionsLayout.addWidget(self.autoLoginBox)

		#按钮布局
		self.buttonLayout = QHBoxLayout()
		self.bottomLayout.addLayout(self.buttonLayout)

		#登陆按钮
		self.loginPushButton=QPushButton(self.tr("登陆"))

		#清除按钮
		self.clearPushButton=QPushButton(self.tr("清除"))

		#配置按钮
		self.setupPushButton=QPushButton(self.tr("配置"))

		self.buttonLayout.addStretch(1)
		self.buttonLayout.addWidget(self.loginPushButton)
		self.buttonLayout.addWidget(self.clearPushButton)
		self.buttonLayout.addWidget(self.setupPushButton)
		self.buttonLayout.addStretch(1)

		self.show()
		

		#信号与槽
		self.connect(self.rememberPasswordBox,QtCore.SIGNAL('stateChanged(int)'),self.rememberPassword)
		self.connect(self.autoLoginBox,QtCore.SIGNAL('stateChanged(int)'),self.autoLogin)
		
		self.connect(self.loginPushButton,QtCore.SIGNAL('clicked()'),self.loginFunction)
		self.connect(self.clearPushButton,QtCore.SIGNAL('clicked()'),self.clearInfo)
		self.connect(self.setupPushButton,QtCore.SIGNAL('clicked()'),self.setupInfo)

		#打开软件时就获取一个登陆ip，避免在线程里多次获取导致第二次登陆失败
		self.host_ip = "172.24.30." + str(randint(2,200))
		#初始化之后载入参数
		self.loadcfg()
		if rememberpassword == True:
			self.usernameLineEdit.setText(username)
			self.passwordLineEdit.setText(password)
			self.rememberPasswordBox.setCheckState(Qt.Checked) 
			if autologin == True :
				self.autoLoginBox.setCheckState(Qt.Checked)
				self.loginFunction()
		
	def clearInfo(self):
		global username, password, rememberpassword, autologin
		self.settings = QSettings("QingFeng","Drcom")
		rememberpassword = False
		autologin = False
		username = ""
		password = ""
		self.usernameLineEdit.setText(username)
		self.passwordLineEdit.setText(password)
		self.rememberPasswordBox.setCheckState(Qt.Unchecked) 	
		self.autoLoginBox.setCheckState(Qt.Unchecked)
		self.settings.setValue("username",QVariant(username))
		self.settings.setValue("password",QVariant(password))
		self.settings.setValue("autologin",QVariant(autologin))
		self.settings.setValue("rememberpassword",QVariant(rememberpassword))

	def setupInfo(self):
		self.setupDialog = SetupDialog()
		self.setupDialog.setModal(True)   #此处ture为模态，false为非模态 ,模态时原窗口不可点击
		self.setupDialog.show()

	def trayclick(self, res):
		if res == QSystemTrayIcon.DoubleClick:
			self.tray.showMessage(u"提示",u"客户端处于最小化",icon=1)

	def aboutMe(self):
		self.aboutDialog = AboutDialog()
		self.aboutDialog.setModal(True)   #此处ture为模态，false为非模态 ,模态时原窗口不可点击
		self.aboutDialog.show()

	def rememberPassword(self, res):
		global rememberpassword
		global autologin
		if self.rememberPasswordBox.isChecked():
			rememberpassword = True
		else:			
			self.autoLoginBox.setCheckState(Qt.Unchecked) 
			rememberpassword = False
			autologin = False

	def autoLogin(self, res):
		global rememberpassword
		global autologin
		if self.autoLoginBox.isChecked():
			self.rememberPasswordBox.setCheckState(Qt.Checked) 
			rememberpassword = True
			autologin = True
		else:			
			autologin = False

	def savecfg(self):
		global username, password, rememberpassword, autologin
		self.settings = QSettings("QingFeng","Drcom")
		self.settings.setValue("username",QVariant(username))
		self.settings.setValue("password",QVariant(password))
		self.settings.setValue("autologin",QVariant(autologin))
		self.settings.setValue("rememberpassword",QVariant(rememberpassword))

	def loadcfg(self):
		global username, password, rememberpassword, autologin
		self.settings = QSettings("QingFeng","Drcom")
		rememberpassword = self.settings.value("rememberpassword").toBool()
		autologin = self.settings.value("autologin").toBool()
		if rememberpassword == True:
			username = self.settings.value("username").toString()
			password = self.settings.value("password").toString()

	def getcfg(self):
		global username, password
		username = self.usernameLineEdit.text()
		password = self.passwordLineEdit.text()

	def loginFunction(self):
		global username, password, loginThread, loginingWindow
		self.getcfg()
		if username == "": 
			QMessageBox.information(self, self.tr("提示!"),
				self.tr("username不能为空"))
		elif password == "":
			QMessageBox.information(self, self.tr("提示!"),
				self.tr("password不能为空"))
		else:
			temp_username = str(username)
			temp_password = str(password)
			self.loginThread = LoginThread()
			self.loginThread.setUsernamePassword(temp_username, temp_password)
			self.loginThread.setStopFlag(False)
			self.loginThread.setHostIp(self.host_ip)
			#连接线程中的信号和登陆槽
			self.loginThread.finishSignal.connect(self.callRunWindow)
			#加载一次数据
			self.loginThread.loadParaToThread()
			#启动
			self.loginThread.start()
			#正在登陆界面和托盘出现
			self.loginingWindow = LoginingWindow()
			#并将自己传递过去
			self.loginingWindow.setSavedWindow(self)
			#当前界面和托盘消失
			self.closeCurrentWindow()
			self.loginingWindow.loginedDetect()

	def callRunWindow(self, sendList):
		print "sendList:",sendList
		self.savecfg()
		#成功登陆界面和托盘出现
		self.mainWindow = MainWindow()
		self.mainWindow.setWindowTitle(self.usernameLineEdit.text())
		self.mainWindow.stateList = sendList
		self.mainWindow.showIPInfo()
		#并把线程传递给它管理
		self.mainWindow.setSavedThread(self.loginThread)
		#正在登陆界面和托盘消失
		self.loginingWindow.closeCurrentWindow()
		#将自己传递过去
		self.mainWindow.setSavedWindow(self)
		#在应用程序所有窗口都关闭的时候不关闭应用程序
		QtGui.QApplication.setQuitOnLastWindowClosed(False)
		
		

	def closeCurrentWindow(self):
		self.setVisible(False)
		self.tray.setVisible(False)

	def showCurrentWindow(self):
		self.setVisible(True)
		self.tray.setVisible(True)


def getRealPath():
	global absPath
	if platform.system() == "Windows":
		absPath = os.path.dirname(os.path.realpath(sys.argv[0])).decode('gbk').encode('utf-8')
		print absPath
	else:
		absPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		print absPath

def changePath(path):
	global absPath
	if platform.system() == "Windows":
		path = absPath + "\\" + path
		print path
	else:
		path = absPath + "/" + path
		print path
	return path

def main():
	app=QApplication(sys.argv)
	getRealPath()
	#欢迎界面
	splash=QSplashScreen(QPixmap(changePath("images\huxi3.jpg")))
	splash.show()
	QThread.sleep(2)
	#app.processEvents()
	#登陆界面
	loginWindow = LoginWindow()
	splash.finish(loginWindow)

	app.exec_()	
if __name__ == '__main__':
	main()