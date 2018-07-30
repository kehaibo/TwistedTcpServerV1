#TCPSerever
#-*_ coding:utf-8 -*-
import os
'''if os.name !='nt':
    from twisted.internet import epollreator
	epollreator.install()
else:
	from twisted.internet import iocpreactor
	iocpreactor.install()'''
from twisted.internet import reactor,protocol
from twisted.python import log
from sys import argv
from cmd import cmd
from CRC16 import CRC16
from comm import comm
from debug import debug 
import time
import binascii
import pymysql
import struct

ConnectNum=0
ConnetNum_MAX=0
ConnetLost_Num=0


class Echo(protocol.Protocol):#处理事件程序

	def __init__(self):

		self.globalv=comm.GlobalValue()
		self.client_datastr=''
		self.databuf=list()
		self.datalen=int()
	
	def dataReceived(self,data):

		#cliend_data=binascii.b2a_hex(data) #ASIIC码转16字符

		cliend_data=list(map(lambda s:s,data))#字符串转list

		#mydebug.PrintLogger(cliend_data)		
		
	#	try:

	#		with open('/home/tmp/tcp server/log/log.txt','a') as Logmsg:
	
	#			Logmsg.write("undisposed data:{}\n ".format(data))

	#	except :

	#		mydebug.PrintLogger("信息无法写入日志或路径问题at{}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime()))) 			
							

		mydebug.PrintLogger("Revice INFO from :{} data:{} at {}\n".format(self.transport.getPeer(),data,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())))	
		
		self.datalen=len(data)

		#mydebug.PrintLogger(self.datalen)
	
		while self.datalen:

			
			if cliend_data[1]==0xFF: #判断是否为固定长度指令数据

				self.dataanalysis(cliend_data)			
					
			elif cliend_data[1]==0xFE: #判断是否为不定长度指令数据，透传等..
				
				mydebug.PrintLogger("variable len!!!")
		
			else: #不是正确的指令	         

				mydebug.PrintLogger("cmd error,cuting down connection!!!")
				self.transport.abortConnection()
				break
			

	def SEND(self,uuid,databody):

		try :

			datapack[data[4:]]

			self.globalv.get(b'0000000099000000000700').write(bytes(struct.pack('B',1)))#uuid+data{uuid:data}

		except AttributeError:

			mydebug.PrintLogger('ERROR :Django client not login\n')

	def connectionLost(self, reason):
		"""
		Called when the connection is shut down.

		Clear any circular references here, and any external references
		to this Pr  otocol.  The connection has been closed.

		@type reason: L{twisted.python.failure.Failure}
		"""

		global ConnectNum

		ConnectNum = ConnectNum - 1
		
		mydebug.PrintLogger("{} device disconnected \n ConnectNum: {}\n".format(self.transport.getPeer(),ConnectNum))
            
		try:

			with open('/home/tmp/tcp server/log/log.txt','a') as Logmsg:

				Logmsg.write("{} disconnected,ConnectNum is {} at {} \n ".format(self.transport.getPeer(),ConnectNum,time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))

		except :

			print("信息无法写入日志或路径问题 at {}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))
		
	     

	def connectionMade(self):

		#self.globalv.set()

		global ConnectNum,ConnectNum_MAX,ConnectLost_Num

		ConnectNum = ConnectNum + 1

     #   if ConnectNum_MAX < ConnectNum:

            
   #          ConnectNum_MAX = ConnectNum

    #    else :
            
     #       ConnectLost_Num = ConnectNum_MAX-ConnectNum
     #       try :
     #           with open('/home/tmp/tcp server/log/lost.txt','a') as f:
     #               f.write("{} Connect Lost,ConnectLostNum:{} at {}\n ".format(self.transport.getPeer(),ConnectLost_Num,time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime()))) 
     
		try:

			with open('/home/tmp/tcp server/log/log.txt','a') as Logmsg:

				Logmsg.write("{} login success,ConnectNum is {} at {}\n ".format(self.transport.getPeer(),ConnectNum,time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))

		except :

			print("信息无法写入日志或路径问题 at {}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))
		mydebug.PrintLogger("{} login success,ConnectNum is {} \n ".format(self.transport.getPeer(),ConnectNum))
		
	def dataanalysis(self,cliend_data):

		mydebug.PrintLogger("fix len data")
				
		if cliend_data[2]==0x01:#电表设备
		
			markindex = int(cliend_data.index(0x15))
					
			self.databuf=cliend_data[markindex:cliend_data[0]]#数据体切割

			CRCL,CRCH=CRC16.CRC16_1(self.databuf[:-2],len(self.databuf[:-2]))#crc校验

			if CRCL==self.databuf[-2] and CRCH==self.databuf[-1]:

				mydebug.PrintLogger("data:{}".format(self.databuf))

				try:

					with open('/home/tmp/tcp server/log/log.txt','a') as Logmsg:

						Logmsg.write(" disposed data :{} at {}\n ".format(self.databuf,time.strftime("%Y-%m_%d %H:%M:%S",time.localtime())))

				except :

					mydebug.PrintLogger("信息无法写入日志或路径问题at{}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime()))) 			
				
				del cliend_data[markindex:markindex+int(cliend_data[0])]#删除数据体已经截取的部分
	
				self.datalen=self.datalen-0x15
					
			else : #数据错误

				with open('/home/tmp/tcp server/log/log.txt','a') as logmsg:

					logmsg.write("error data :{}".format(self.databuf))			
	
				mydebug.PrintLogger("crc not pass!")
				
				self.datalen=self.datalen-0x15
			
				if self.datalen<=0:
				
					self.datalen=0								

		elif cliend_data[2]==0x02:#空调设备

			mydebug.PrintLogger("KT device")					

		else: #不是正确的指令
					
			mydebug.PrintLogger("NO this type device")
					
						
	def datahandle(self,cliend_data):

		if cliend_data[0:2]==b'fb':#设备登录

			#print(str(cliend_data[4:25])+str(data[4:25]))

			if cliend_data[2:4]==b'0b'and cliend_data[27:]==b'':

				uuid =struct.pack('22s',cliend_data[4:27])

				if uuid not in self.globalv.checkkeys():

					self.globalv.set(uuid,self.transport)

				else:

					mydebug.PrintLogger('ERROR :device existed')

			if  cliend_data[26:30]== b'b002':#设备数据

				datalen= str(len(cliend_data)-26)+'s'

				databody=struct.pack(datalen,cliend_data[26:])

				print(databody)

						
	
class EchoFactory(protocol.Factory):

	def buildProtocol(self, addr):  #重写该函数，该函数返回protocol的实例

		return Echo()


if __name__ == '__main__':

	if os.name!='nt':

		mydebug=debug.Debug(argv[1])
	else:
		mydebug=debug.Debug(True)

	Devfactory=EchoFactory()

	reactor.listenTCP(8001,Devfactory)

	print("Listening....\n")

#	with open('E:\\Python-L\\twisted_file\\tcp server\\log\\log.txt','a') as Logmsg:

#			Logmsg.write("{} login success\n".format(self.transport.getPeer()))

	reactor.run()
