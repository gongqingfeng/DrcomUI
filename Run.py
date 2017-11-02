#!/usr/bin/env python
#coding:utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
from M_Dialog import AboutDialog

reload(sys)
sys.setdefaultencoding('utf-8')
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class MainWindow(QMainWindow):
	def __init__(self,parent=None):
		super(MainWindow,self).__init__(parent)
		self.resize(280,460) #设置窗口大小
		self.move(1500,200)
		#设置图标
		micon = QtGui.QIcon()
		micon.addPixmap(QtGui.QPixmap("images/python_128px.ico"),
			QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(micon)
		self.stateList = []
		#只显示关闭按钮
		self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowMinMaxButtonsHint) 
		#禁止拉伸窗口大小  
		self.setFixedSize(self.width(), self.height())
		#系统托盘
		self.tray = QtGui.QSystemTrayIcon()
		self.trayIcon = QtGui.QIcon('images/python_128px')
		self.tray.setIcon(self.trayIcon)
		self.tray.show()
		self.tray.showMessage(u"提示",u"客户端正在运行",icon=1)
		# 在系统托盘区域的图标被点击就会触发activated连接的函数
		self.tray.activated.connect(self.trayclick)
		self.tray_menu = QtGui.QMenu(QApplication.desktop()) #创建菜单  
		self.RestoreAction = QAction(u'显示主界面 ', self, triggered=self.showNormal) #添加一级菜单动作选项(还原主窗口)  
		self.AboutAction = QAction(u'关于', self, triggered=self.aboutMe) #添加一级菜单关于选项
		self.QuitAction = QAction(u'注销', self, triggered=self.logout) #添加一级菜单动作选项(退出程序)  
		self.tray_menu.addAction(self.RestoreAction) #为菜单添加动作  
		self.tray_menu.addAction(self.AboutAction)  
		self.tray_menu.addAction(self.QuitAction)
		self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单

		#主布局
		self.mainLayout=QVBoxLayout()
		self.widget = QtGui.QWidget()
		self.widget.setLayout(self.mainLayout)
		self.setCentralWidget(self.widget)

		#图片布局
		self.topLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.topLayout)
		self.bannerLabel=QLabel()
		self.banner=QPixmap("images/huxi.jpg")
		self.bannerLabel.setPixmap(self.banner)
		self.topLayout.addWidget(self.bannerLabel)
		
		#底级布局
		self.bottomLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.bottomLayout)

		#参数布局
		self.paraLayout = QGridLayout()
		self.bottomLayout.addLayout(self.paraLayout)
		self.paraLayout.setMargin(40)
		self.paraLayout.setSpacing(10)
		#serverLabel
		self.serverLabel = QLabel(self.tr("远程服务器ip:"))
		self.paraLayout.addWidget(self.serverLabel, 0, 0)

		self.serverValueLabel = QLabel('202.202.0.180')
		self.paraLayout.addWidget(self.serverValueLabel, 0, 1)

		#host_ipLabel
		self.host_ipLabel = QLabel(self.tr("本地登陆ip:"))
		self.paraLayout.addWidget(self.host_ipLabel, 1, 0)

		self.host_ipValueLabel = QLabel('202.202.0.180')
		self.paraLayout.addWidget(self.host_ipValueLabel, 1, 1)

		#dnsLabel
		self.dnsLabel = QLabel(self.tr("dns服务器ip:"))
		self.paraLayout.addWidget(self.dnsLabel, 2, 0)

		self.dnsValueLabel = QLabel('202.202.0.180')
		self.paraLayout.addWidget(self.dnsValueLabel, 2, 1)

		#注销按钮
		self.logoutPushButton=QPushButton(self.tr("注销"))
		self.paraLayout.addWidget(self.logoutPushButton, 3, 0)

		#退出按钮
		self.exitPushButton=QPushButton(self.tr("退出"))
		self.paraLayout.addWidget(self.exitPushButton, 3, 1)

		#信号与槽
		self.connect(self.logoutPushButton,QtCore.SIGNAL('clicked()'),self.logout)
		self.connect(self.exitPushButton,QtCore.SIGNAL('clicked()'),qApp.quit)

		self.show()

	def trayclick(self,res):
		if res == QSystemTrayIcon.DoubleClick: #注意此处不能判断Trigger
			self.show()	

	def aboutMe(self):
		self.aboutDialog = AboutDialog()
		self.aboutDialog.setModal(True)   #此处ture为模态，false为非模态 ,模态时原窗口不可点击
		self.aboutDialog.show()

	def logout(self):
		self.savedThread.setStopFlag(True)
		#将成功登陆标志改为False
		#self.savedThread.setSucceedFlag(False)
		#登陆界面和托盘出现
		self.savedWindow.loginThread.quit()
		self.savedWindow.showCurrentWindow()
		#当前界面和托盘消失
		self.closeCurrentWindow()
		#在应用程序所有窗口都关闭的时候也关闭应用程序
		QtGui.QApplication.setQuitOnLastWindowClosed(True)

	def closeCurrentWindow(self):
		self.setVisible(False)
		self.tray.setVisible(False)
	
	def setSavedWindow(self, savedWindow):
		self.savedWindow = savedWindow

	def getSavedWindow(self):
		return self.savedWindow 

	def setSavedThread(self, savedThread):
		self.savedThread = savedThread

	def getSavedThread(self):
		return self.savedThread

	def showIPInfo(self):
		self.host_ipValueLabel.setText(self.stateList[1])
		self.serverValueLabel.setText(self.stateList[2]) 
		self.dnsValueLabel.setText(self.stateList[3])

def main():
	app=QApplication(sys.argv)
	#登陆成功界面
	window=MainWindow()
	window.show()
	#在应用程序所有窗口都关闭的时候不关闭应用程序
	QtGui.QApplication.setQuitOnLastWindowClosed(False)
	app.exec_()	
	
if __name__ == '__main__':
		main()	
