# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys, time, platform, os
from M_Dialog import AboutDialog
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
username = ""
absPath = ""
class FailedWindow(QMainWindow):
	def __init__(self,parent=None):
		global username, password, rememberpassword, autologin, firstFlag
		super(FailedWindow,self).__init__(parent)
		self.resize(425,300) #设置窗口大小
		self.setWindowTitle(self.tr("登陆失败"))
		getRealPath()
		#设置图标
		micon = QtGui.QIcon()
		micon.addPixmap(QtGui.QPixmap(changePath("images/python_128px")),
			QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(micon)
		#禁止最大化按钮
		self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowMinMaxButtonsHint | 
			QtCore.Qt.WindowMinimizeButtonHint) 
		#禁止拉伸窗口大小  
		self.setFixedSize(self.width(), self.height())

		#系统托盘
		self.tray = QtGui.QSystemTrayIcon() 
		self.trayIcon = QtGui.QIcon(changePath("images/python_128px"))
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
		self.banner=QPixmap(changePath("images/huxi.png"))
		self.bannerLabel.setPixmap(self.banner)
		self.topLayout.addWidget(self.bannerLabel)
		
		#底级布局
		self.bottomLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.bottomLayout)

		#firstLabel
		self.firstLabel = QLabel(self.tr("可能的原因:"))
		self.bottomLayout.addWidget(self.firstLabel)

		#secondLabel
		self.secondLabel = QLabel(self.tr("    * 账号或者密码错误"))
		self.bottomLayout.addWidget(self.secondLabel)

		#thirdLabel
		self.thirdLabel = QLabel(self.tr("    * ip地址设置有误"))
		self.bottomLayout.addWidget(self.thirdLabel)

		#fourthLabel
		self.fourthLabel = QLabel(self.tr("    * 网线或者网卡故障"))
		self.bottomLayout.addWidget(self.fourthLabel)

		#fifthLabel
		self.fifthLabel = QLabel(self.tr("    * dns服务异常"))
		self.bottomLayout.addWidget(self.fifthLabel)

		#按钮布局
		self.buttonLayout = QGridLayout()
		self.bottomLayout.addLayout(self.buttonLayout)

		#取消按钮
		self.redoPushButton=QPushButton(self.tr("取消"))
		self.buttonLayout.addWidget(self.redoPushButton, 0, 0, Qt.AlignHCenter)

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
		#登陆界面和托盘出现
		self.savedWindow.getSavedWindow().showCurrentWindow()
		#当前界面和托盘消失
		self.closeCurrentWindow()
def getRealPath():
	global absPath
	if platform.system() == "Windows":
		absPath = os.path.dirname(os.path.realpath(sys.argv[0])).decode('gbk').encode('utf-8')
		#print absPath
	else:
		absPath = os.path.dirname(os.path.realpath(sys.argv[0]))

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
	#登陆失败界面
	failedWindow=FailedWindow()
	app.exec_()	
if __name__ == '__main__':
	main()