#TCPSerever
import os
if os.name !='nt':
	from twisted.internet import epollreator
	epollreator.install()
else:
	from twisted.internet import iocpreactor
	iocpreactor.install()
from twisted.internet import reactor,protocol
from CRC16 import CRC16
from comm import comm
import time
import binascii
from twisted.python import log



ConnectNum=0

class Echo(protocol.Protocol):#处理事件程序

	def __init__(self):

		self.globalv=comm.GlobalValue()
	
	def dataReceived(self,data):

		#print(str(self.transport.getPeer())+'Client data:'+str(data,encoding='utf-8'))

		d=binascii.b2a_hex(data) #字符转16

		print(d[0:2])

		if d[0:2]==b'fb':

			print(d[2:4])

		#print(d)

		print("Revice INFO from :{} data :{}".format(self.transport.getPeer(),data))

		self.transport.write(data)	


	def connectionLost(self, reason):
		"""
		Called when the connection is shut down.

		Clear any circular references here, and any external references
		to this Protocol.  The connection has been closed.

		@type reason: L{twisted.python.failure.Failure}
		"""
		global ConnectNum

		ConnectNum = ConnectNum - 1
		
		print("{} device disconnected , the time ConnectNum: {}\n".format(self.transport.getPeer(),ConnectNum))

	def connectionMade(self):

		global ConnectNum

		self.globalv.set()

		ConnectNum = ConnectNum + 1

		#try:

		#	with open('E:\\Python-L\\twisted_file\\tcp server\\log\\log.txt','a') as Logmsg:

		#		Logmsg.write("{} login success,ConnectNum is {} \n ".format(self.transport.getPeer(),ConnectNum))

		#except :

			#print("信息无法写入日志或路径问题 at {}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))
		print("{} login success,ConnectNum is {} \n ".format(self.transport.getPeer(),ConnectNum))
		
class EchoFactory(protocol.Factory):

	def buildProtocol(self, addr):  #重写该函数，该函数返回protocol的实例

		return Echo()

if __name__ == '__main__':

	Devfactory=EchoFactory()

	reactor.listenTCP(8001,Devfactory)

	print("Listening....\n")

#	with open('E:\\Python-L\\twisted_file\\tcp server\\log\\log.txt','a') as Logmsg:

#			Logmsg.write("{} login success\n".format(self.transport.getPeer()))

	reactor.run()
