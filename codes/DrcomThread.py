#coding=UTF-8

import socket, struct, time,random,re,sys,os
from hashlib import md5
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings
#config
server = '202.202.0.180'
CONTROLCHECKSTATUS = '\x20'
ADAPTERNUM = '\x05'
host_ip = '172.24.30.34' #172.24.30.x
IPDOG = '\x01'
host_name = 'DRCOMFUCKER'
PRIMARY_DNS = '202.202.0.34'
dhcp_server = '202.202.2.50'
AUTH_VERSION = '\x25\x00'
mac = 0xf0761cbd01b3
host_os = 'WINDIAOS'
KEEP_ALIVE_VERSION = '\xdc\x02'
#config_end

succeedFlag = False
username=''    #your student number
password=''      #your password
stopFlag = False
#继承 QThread 类
class LoginThread(QtCore.QThread):
	finishSignal = QtCore.pyqtSignal(list)
	def __init__(self, parent=None):
		
		super(LoginThread, self).__init__(parent)

	#重写 run() 函数
	def run(self):
		connectNetwork(self.finishSignal, self.username, self.password)

	def setUsernamePassword(self, username, password):
		self.username = username
		self.password = password

	#传递一个参数作为辅助
	def setSucceedFlag(self, flag):
		global succeedFlag 
		succeedFlag = flag

	def setStopFlag(self, flag):
		global stopFlag
		stopFlag = flag

	def setHostIp(self,temp_host_ip):
		global host_ip
		host_ip = temp_host_ip

	def loadParaToThread(self):
		global server, host_ip, CONTROLCHECKSTATUS, ADAPTERNUM,  IPDOG, host_name, PRIMARY_DNS, dhcp_server, AUTH_VERSION, mac, host_os, KEEP_ALIVE_VERSION 
		self.settings = QSettings("QingFeng","Drcom")
		#确保保存一次之后才会加载数据，否则会得到空值
		if self.settings.value("loadParaFlag").toBool() == True:
			server = str(self.settings.value("server").toString())
			CONTROLCHECKSTATUS = str(self.settings.value("controlcheckstatus").toString())
			ADAPTERNUM = str(self.settings.value("adapternum").toString())
			IPDOG = str(self.settings.value("ipdog").toString())
			host_name = str(self.settings.value("host_name").toString())
			PRIMARY_DNS = str(self.settings.value("primary_dns").toString())
			dhcp_server = str(self.settings.value("dhcp_server").toString())
			AUTH_VERSION = str(self.settings.value("auth_version").toString())
			macStr = str(self.settings.value("mac").toString())
			mac = int(macStr, 16)  #16进制字符串转16进制数字
			host_os = str(self.settings.value("host_os").toString())
			KEEP_ALIVE_VERSION = str(self.settings.value("keep_alive_version").toString())

#检查是否登陆成功的进程
class LoginedFlagThread(QtCore.QThread):
	failedSignal = QtCore.pyqtSignal(bool)
	def __init__(self, parent=None):
		self.redoFlag = False
		super(LoginedFlagThread, self).__init__(parent)

	#重写 run() 函数
	def run(self):
		global succeedFlag, stopFlag
		time.sleep(10)
		exit_code = os.system('ping www.baidu.com >NUL 2>NUL')
		if exit_code:
			stopFlag = True 
			self.failedSignal.emit(True) 
			
	#传递一个参数作为辅助
	def setRedoFlag(self, flag):
		self.redoflag = flag

class ChallengeException (Exception):
  def __init__(self):
	pass

class loginException (Exception):
  def __init__(self):
	pass
	
def try_socket(signal):
#sometimes cannot get the port
	global s,salt
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(("0.0.0.0", 61440))
		s.settimeout(3)
		main(signal)
	except:
		time.sleep(0.5)
		time.sleep(0.5)
		time.sleep(0.5)
		#time.sleep(10)
		main(signal)
	else:
		SALT= ''

UNLIMITED_RETRY = True
EXCEPTION = False
	
def get_randmac():
	mac = [ 0x00, 0x16, 0x3e,random.randint(0x00, 0x7f),random.randint(0x00, 0xff),random.randint(0x00, 0xff) ]
	return ''.join(map(lambda x: "%02x" % x, mac))
	#print randomMAC()
	
	
def challenge(svr,ran):
	while not stopFlag:
	  t = struct.pack("<H", int(ran)%(0xFFFF))
	  s.sendto("\x01\x02"+t+"\x09"+"\x00"*15, (svr, 61440))
	  try:
		data, address = s.recvfrom(1024)
		#print('[challenge] recv',data.encode('hex'))
	  except:
		continue
		
	  if address == (svr, 61440):
		break
	  else:
		continue
	#print('[DEBUG] challenge:\n' + data.encode('hex'))
	if data[0] != '\x02':
	  raise ChallengeException
	return data[4:8]

def md5sum(s):
	m = md5()
	m.update(s)
	return m.digest()

def dump(n):
	s = '%x' % n
	if len(s) & 1:
		s = '0' + s
	return s.decode('hex')

def ror(md5, pwd):
	ret = ''
	for i in range(len(pwd)):
		x = ord(md5[i]) ^ ord(pwd[i])
		ret += chr(((x<<3)&0xFF) + (x>>5))
	return ret

def keep_alive_package_builder(number,random,tail,type=1,first=False):
	data = '\x07'+ chr(number) + '\x28\x00\x0b' + chr(type)
	data += KEEP_ALIVE_VERSION+'\x2f\x12' + '\x00' * 6
	data += tail
	data += '\x00' * 4
	#data += struct.pack("!H",0xdc02)
	if type == 3:
	  foo = ''.join([chr(int(i)) for i in host_ip.split('.')]) # host_ip
	#use double keep in main to keep online .Ice
	  crc = '\x00' * 4
	  #data += struct.pack("!I",crc) + foo + '\x00' * 8
	  data += crc + foo + '\x00' * 8
	else: #packet type = 1
	  data += '\x00' * 16
	return data

def packet_CRC(s):
	ret = 0
	for i in re.findall('..', s):
		ret ^= struct.unpack('>h', i)[0]
		ret &= 0xFFFF
	ret = ret * 0x2c7
	return ret



def keep_alive2(*args):
	global stopFlag
	tail = ''
	packet = ''
	svr = server
	ran = random.randint(0,0xFFFF)
	ran += random.randint(1,10)   
	
	packet = keep_alive_package_builder(0,dump(ran),'\x00'*4,1,True)
	#packet = keep_alive_package_builder(0,dump(ran),dump(ran)+'\x22\x06',1,True)
	while True:
		s.sendto(packet, (svr, 61440))
		data, address = s.recvfrom(1024)
		if data.startswith('\x07'):
			break
		else:
			continue
	ran += random.randint(1,10)   
	packet = keep_alive_package_builder(1,dump(ran),'\x00'*4,1,False)
	#print '[keep-alive2] send2',packet.encode('hex')
	s.sendto(packet, (svr, 61440))
	while True:
		data, address = s.recvfrom(1024)
		if data[0] == '\x07':
			break
	#print '[keep-alive2] recv2',data.encode('hex')
	tail = data[16:20]
	

	ran += random.randint(1,10)   
	packet = keep_alive_package_builder(2,dump(ran),tail,3,False)
	#print '[keep-alive2] send3',packet.encode('hex')
	s.sendto(packet, (svr, 61440))
	while True:
		data, address = s.recvfrom(1024)
		if data[0] == '\x07':
			break
	#print '[keep-alive2] recv3',data.encode('hex')
	tail = data[16:20]
	i = 3

	while not stopFlag :
	  try:
		keep_alive1(SALT,package_tail,password,server)
		ran += random.randint(1,10)   
		packet = keep_alive_package_builder(i,dump(ran),tail,1,False)
		#print('DEBUG: keep_alive2,packet 4\n',packet.encode('hex'))
		#print '[keep_alive2] send',str(i),packet.encode('hex')
		s.sendto(packet, (svr, 61440))
		data, address = s.recvfrom(1024)
		#print '[keep_alive2] recv',data.encode('hex')
		tail = data[16:20]
		#print('DEBUG: keep_alive2,packet 4 return\n',data.encode('hex'))
		
		ran += random.randint(1,10)   
		packet = keep_alive_package_builder(i+1,dump(ran),tail,3,False)
		#print('DEBUG: keep_alive2,packet 5\n',packet.encode('hex'))
		s.sendto(packet, (svr, 61440))
		#print('[keep_alive2] send',str(i+1),packet.encode('hex'))
		data, address = s.recvfrom(1024)
		#print('[keep_alive2] recv',data.encode('hex'))
		tail = data[16:20]
		#print('DEBUG: keep_alive2,packet 5 return\n',data.encode('hex'))
		i = (i+2) % 0xFF
		time.sleep(20)
	  except:
		pass

def checksum(s):
	ret = 1234
	for i in re.findall('....', s):
		ret ^= int(i[::-1].encode('hex'), 16)
	ret = (1968 * ret) & 0xffffffff
	return struct.pack('<I', ret)


def mkpkt(salt, usr, pwd, mac):
	data = '\x03\x01\x00'+chr(len(usr)+20)
	data += md5sum('\x03\x01'+salt+pwd)
	data += usr.ljust(36, '\x00')
	data += '\x20' #fixed unknow 1
	data += '\x02' #unknow 2
	data += dump(int(data[4:10].encode('hex'),16)^mac).rjust(6,'\x00') #mac xor md51
	data += md5sum("\x01" + pwd + salt + '\x00'*4) #md52
	data += '\x01' #NIC count
	data += hexip #your ip address1 
	data += '\00'*4 #your ipaddress 2
	data += '\00'*4 #your ipaddress 3
	data += '\00'*4 #your ipaddress 4
	data += md5sum(data + '\x14\x00\x07\x0b')[:8] #md53
	data += '\x01' #ipdog
	data += '\x00'*4 #delimeter
	data += host_name.ljust(32, '\x00')
	data += '\x72\x72\x72\x72' #primary dns: 114.114.114.114
	data += '\x0a\xff\x00\xc5' #DHCP server
	data += '\x08\x08\x08\x08' #secondary dns:8.8.8.8
	data += '\x00' * 8 #delimeter
	data += '\x94\x00\x00\x00' # unknow
	data += '\x05\x00\x00\x00' #os major
	data += '\x01\x00\x00\x00' # os minor
	data += '\x28\x0a\x00\x00' # OS build
	data += '\x02\x00\x00\x00' #os unknown
	data += host_os.ljust(32,'\x00')
	data += '\x00' * 96
	#data += '\x01' + host_os.ljust(128, '\x00')
	#data += '\x0a\x00\x00'+chr(len(pwd)) # \0x0a represents version of client, algorithm: DRCOM_VER + 100
	#data += ror(md5sum('\x03\x01'+salt+pwd), pwd)
	data += AUTH_VERSION
	data += '\x02\x0c'
	data += checksum(data+'\x01\x26\x07\x11\x00\x00'+dump(mac))
	data += '\x00\x00' #delimeter
	data += dump(mac)
	data += '\x00' # auto logout / default: False
	data += '\x00' # broadcast mode / default : False
	data += '\xc2\x66' #unknown
	
	
	return data

def login(signal, usr, pwd, svr):
	global SALT, succeedFlag, host_ip, server
	i = 0
	while True:
		salt = challenge(svr,time.time()+random.randint(0xF,0xFF))
		SALT = salt
		packet = mkpkt(salt, usr, pwd, mac)
		#print('[login] send',packet.encode('hex'))
		s.sendto(packet, (svr, 61440))
		data, address = s.recvfrom(1024)
		#print('[login] recv',data.encode('hex'))
		if address == (svr, 61440):
			if data[0] == '\x04':
			  break
			else:
			  continue
		else:
			if i >= 5 and UNLIMITED_RETRY == False :
			  sys.exit(1)
			else:
			  continue
			

	succeedFlag = True
	sendList = [True, host_ip, server, dhcp_server]
	if succeedFlag == True:
		signal.emit(sendList)
	return data[23:39]
	#return data[-22:-6]

def keep_alive1(salt,tail,pwd,svr):
	foo = struct.pack('!H',int(time.time())%0xFFFF)
	data = '\xff' + md5sum('\x03\x01'+salt+pwd) + '\x00\x00\x00'
	data += tail
	data += foo + '\x00\x00\x00\x00'

	s.sendto(data, (svr, 61440))
	while True:
		data, address = s.recvfrom(1024)
		if data[0] == '\x07':
			break
		else:
			pass
	#print('[keep-alive1] recv',data.encode('hex'))

def empty_socket_buffer():
#empty buffer
	try:
		while True:
			data, address = s.recvfrom(1024)
			#print 'recived sth unexcepted',data.encode('hex')
			if s == '':
				break
	except:
		# get exception means it has done.
		pass


		
def main(signal):
	global server,username,password,host_name,host_os,dhcp_server,mac,hexip,host_ip
	while True:
		try:
			hexip=socket.inet_aton(host_ip)
			break
		except :
			pass
	
	#host_ip=ip
	#host_name = "est-pc"
	#host_os = "8089D"   #default is 8089D
	#dhcp_server = "0.0.0.0"
	#mac = 0xE0DB55BAE012 
	#it is a mac in programme and it may crush with other users so I use randMAC to avoid it
	loginpart(signal)
	
def loginpart(signal):
	global package_tail
	while not stopFlag:
		try:
			package_tail = login(signal, username, password, server)
		except loginException:
			continue

		keeppart()
		
def keeppart():
	keep_alive2(SALT,package_tail,password,server)

def connectNetwork(signal, temp_username, temp_password):
	global username, password
	username = temp_username
	password =  temp_password
	try_socket(signal)
	#main(signal)
		
if __name__ == "__main__":
	connectNetwork('*', '*')

