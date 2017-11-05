# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys, platform, os
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
absPath = ""
class AboutDialog(QDialog):
	def __init__(self,parent=None):
		super(AboutDialog,self).__init__(parent)
		self.resize(425,300) #设置窗口大小
		self.center()
		self.setWindowTitle(self.tr("关于应用"))
		getRealPath()
		#设置图标
		micon = QtGui.QIcon() 
		micon.addPixmap(QtGui.QPixmap(changePath("images/python_128px.ico")),
			QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(micon)
		#只显示关闭按钮
		self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowContextHelpButtonHint) 
		#禁止拉伸窗口大小  
		self.setFixedSize(self.width(), self.height())

		#主布局
		self.mainLayout=QVBoxLayout()
		self.setLayout(self.mainLayout)

		#firstLabel
		self.firstLabel = QLabel(self.tr("说明"))
		self.mainLayout.addWidget(self.firstLabel)

		#secondLabel
		self.secondLabel = QLabel(self.tr("*本应用采用python语言开发"))
		self.mainLayout.addWidget(self.secondLabel)

		#thirdLabel
		self.thirdLabel = QLabel(self.tr("*纯属免费应用，作者从未获取任何利益"))
		self.mainLayout.addWidget(self.thirdLabel)

		#fourthLabel
		self.fourthLabel = QLabel(self.tr("*代码托管在github和码云上"))
		self.mainLayout.addWidget(self.fourthLabel)

		#fifthLabel
		self.fifthLabel = QLabel(self.tr("*若被告知侵犯他人权益"))
		self.mainLayout.addWidget(self.fifthLabel)

		#sixthLabel
		self.sixthLabel = QLabel(self.tr("*作者会立即下架被删除应用"))
		self.mainLayout.addWidget(self.sixthLabel)

		#seventhLabel
		self.seventhLabel = QLabel(self.tr("关于我:一个爱马刺的程序员"))
		self.mainLayout.addWidget(self.seventhLabel)

		#eiththLabel
		self.eiththLabel = QLabel(self.tr('*个人博客: <a href="http://blog.spursgo.com" style="color:#0000ff;"><b> http://blog.spursgo.com </b></a>'))
		self.mainLayout.addWidget(self.eiththLabel)

		#ninthLabel
		self.ninthLabel = QLabel(self.tr('*github: <a href="https://github.com/gongqingfeng" style="color:#0000ff;"><b> https://github.com/gongqingfeng </b></a>'))
		self.mainLayout.addWidget(self.ninthLabel)

		#tenthLabel
		self.tenthLabel = QLabel(self.tr('*码云: <a href="https://gitee.com/gospursgo1996" style="color:#0000ff;"><b> https://gitee.com/gospursgo1996 </b></a>'))
		self.mainLayout.addWidget(self.tenthLabel)

	def center(self):  
		screen =QtGui.QDesktopWidget().screenGeometry()  
		size = self.geometry()  
		self.move(screen.width() * 3 / 4,    
		(screen.height() - size.height()) / 2)


class SetupDialog(QDialog):
	def __init__(self,parent=None):
		super(SetupDialog,self).__init__(parent)
		#self.resize(425,300) #设置窗口大小
		self.center()
		self.setWindowTitle(self.tr("配置参数"))
		#设置图标
		micon = QtGui.QIcon()
		micon.addPixmap(QtGui.QPixmap(changePath("images/python_128px.ico")),
			QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(micon)
		#只显示关闭按钮
		self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowContextHelpButtonHint) 
		#禁止拉伸窗口大小  
		self.setFixedSize(self.width(), self.height())

		#主布局
		self.mainLayout=QVBoxLayout()
		self.setLayout(self.mainLayout)

		#参数布局
		self.paraLayout = QGridLayout()
		self.mainLayout.addLayout(self.paraLayout)
		self.paraLayout.setMargin(20)
		self.paraLayout.setSpacing(20)
		#firstLabel
		self.firstLabel = QLabel("server")
		self.paraLayout.addWidget(self.firstLabel, 0, 0)

		self.serverLineEdit = QLineEdit('202.202.0.180')
		self.paraLayout.addWidget(self.serverLineEdit, 0, 1)

		#secondLabel
		self.secondLabel = QLabel("controlcheckstatus")
		self.paraLayout.addWidget(self.secondLabel, 1, 0)

		self.controlcheckstatusLineEdit = QLineEdit('\\x20')
		self.paraLayout.addWidget(self.controlcheckstatusLineEdit, 1, 1)

		#thirdLabel
		self.thirdLabel = QLabel("adapternum")
		self.paraLayout.addWidget(self.thirdLabel, 2, 0)

		self.adapternumLineEdit = QLineEdit('\\x05')
		self.paraLayout.addWidget(self.adapternumLineEdit, 2, 1)

		#fourthLabel
		#self.fourthLabel = QLabel("host_ip")
		#self.paraLayout.addWidget(self.fourthLabel, 3, 0)

		#self.host_ipLineEdit = QLineEdit('172.24.30.3')
		#self.paraLayout.addWidget(self.host_ipLineEdit, 3, 1)

		#fifthLabel
		self.fifthLabel = QLabel("ipdog")
		self.paraLayout.addWidget(self.fifthLabel, 4, 0)

		self.ipdogLineEdit = QLineEdit('\\x01')
		self.paraLayout.addWidget(self.ipdogLineEdit, 4, 1)

		#sixthLabel
		self.sixthLabel = QLabel("host_name")
		self.paraLayout.addWidget(self.sixthLabel, 5, 0)

		self.host_nameLineEdit = QLineEdit('DRCOMFUCKER')
		self.paraLayout.addWidget(self.host_nameLineEdit, 5, 1)

		#seventhLabel
		self.seventhLabel = QLabel("primary_dns")
		self.paraLayout.addWidget(self.seventhLabel, 6 , 0)

		self.primary_dnsLineEdit = QLineEdit('202.202.0.34')
		self.paraLayout.addWidget(self.primary_dnsLineEdit, 6, 1)

		#eiththLabel
		self.eiththLabel = QLabel("dhcp_server")
		self.paraLayout.addWidget(self.eiththLabel, 7, 0)

		self.dhcp_serverLineEdit = QLineEdit('202.202.2.50')
		self.paraLayout.addWidget(self.dhcp_serverLineEdit, 7, 1)

		#ninthLabel
		self.ninthLabel = QLabel("auth_version")
		self.paraLayout.addWidget(self.ninthLabel, 8, 0)

		self.auth_versionLineEdit = QLineEdit('\\x25\\x00')
		self.paraLayout.addWidget(self.auth_versionLineEdit, 8, 1)

		#tenthLabel
		self.tenthLabel = QLabel("mac")
		self.paraLayout.addWidget(self.tenthLabel, 9, 0)

		self.macLineEdit = QLineEdit('0xf0761cbd01b3')
		self.paraLayout.addWidget(self.macLineEdit, 9, 1)

		#eleventhLabel
		self.eleventhLabel = QLabel("host_os")
		self.paraLayout.addWidget(self.eleventhLabel, 10, 0)

		self.host_osLineEdit = QLineEdit('WINDIAOS')
		self.paraLayout.addWidget(self.host_osLineEdit, 10, 1)

		#twelfthLabel
		self.twelfthLabel = QLabel("keep_alive_version")
		self.paraLayout.addWidget(self.twelfthLabel, 11, 0)

		self.keep_alive_versionLineEdit = QLineEdit('\\xdc\\x02')
		self.paraLayout.addWidget(self.keep_alive_versionLineEdit, 11, 1)

		#按钮布局
		self.buttonLayout = QGridLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		#保存按钮
		self.savePushButton = QPushButton(self.tr("保存"))
		self.buttonLayout.addWidget(self.savePushButton,0, 1,  Qt.AlignHCenter)

		#信号与槽
		self.connect(self.savePushButton,QtCore.SIGNAL('clicked()'),self.savePara)
		self.loadParaToView()

	def center(self):  
		screen =QtGui.QDesktopWidget().screenGeometry()  
		size = self.geometry()  
		self.move((screen.width() - size.width()) / 2,    
		(screen.height() - size.height()) / 2)

	def savePara(self):
		self.settings = QSettings("QingFeng","Drcom")
		self.settings.setValue("loadParaFlag",QVariant(True))
		self.settings.setValue("server",QVariant(self.serverLineEdit.text()))
		self.settings.setValue("controlcheckstatus",QVariant(self.controlcheckstatusLineEdit.text()))
		self.settings.setValue("adapternum",QVariant(self.adapternumLineEdit.text()))
		self.settings.setValue("ipdog",QVariant(self.ipdogLineEdit.text()))
		self.settings.setValue("host_name",QVariant(self.host_nameLineEdit.text()))
		self.settings.setValue("primary_dns",QVariant(self.primary_dnsLineEdit.text()))
		self.settings.setValue("dhcp_server",QVariant(self.dhcp_serverLineEdit.text()))
		self.settings.setValue("auth_version",QVariant(self.auth_versionLineEdit.text()))
		self.settings.setValue("mac",QVariant(self.macLineEdit.text()))
		self.settings.setValue("host_os",QVariant(self.host_osLineEdit.text()))
		self.settings.setValue("keep_alive_version",QVariant(self.keep_alive_versionLineEdit.text()))
		QMessageBox.information(self, self.tr("提示"),self.tr("保存成功!"))

	def loadParaToView(self):
		self.settings = QSettings("QingFeng","Drcom")
		#确保保存一次之后才会加载数据，否则会得到空值
		if self.settings.value("loadParaFlag").toBool() == True:
			self.serverLineEdit.setText(self.settings.value("server").toString()) 
			self.controlcheckstatusLineEdit.setText(self.settings.value("controlcheckstatus").toString())
			self.adapternumLineEdit.setText(self.settings.value("adapternum").toString())
			self.ipdogLineEdit.setText(self.settings.value("ipdog").toString())
			self.host_nameLineEdit.setText(self.settings.value("host_name").toString())
			self.primary_dnsLineEdit.setText(self.settings.value("primary_dns").toString())
			self.dhcp_serverLineEdit.setText(self.settings.value("dhcp_server").toString())
			self.auth_versionLineEdit.setText(self.settings.value("auth_version").toString())
			self.macLineEdit.setText(self.settings.value("mac").toString())
			self.host_osLineEdit.setText(self.settings.value("host_os").toString())
			self.keep_alive_versionLineEdit.setText(self.settings.value("keep_alive_version").toString())

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
	app = QApplication(sys.argv)
	#关于对话框
	setupDialog = SetupDialog()
	setupDialog.show()
	app.exec_()	
if __name__ == '__main__':
	main()