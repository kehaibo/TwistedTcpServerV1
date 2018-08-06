#TCPSerever
#-*_ coding:utf-8 -*-
import os
if os.name =='nt':
	from twisted.internet import iocpreactor
	iocpreactor.install()

from twisted.internet import reactor,protocol
from twisted.python import log
from cmdanalysis  import analysiscmd
from adbmysql import adbmysql
from twisted.enterprise import adbapi
from sys import argv
from cmd import cmd
from CRC16 import CRC16
from comm import comm
import time
import binascii
import pymysql
import pymysql.cursors
import struct
import logging


class Echo(protocol.Protocol):#处理事件程序

	def __init__(self):

		global loglocal
		self.globalv=comm.GlobalValue()
		self.client_datastr=''
		self.databuf=list()
		self.datalen=int()
		self.uuid = ''
		self.temp = ''
		self.loglocal = loglocal
		self.mylogger=logging.getLogger()
		stdprintf = logging.StreamHandler()
		if os.name !='nt':
			if argv[1]=='True':
				self.mylogger.addHandler(stdprintf)
		else:
			self.mylogger.addHandler(stdprintf)
		
	def dataReceived(self,data):

		#cliend_data=binascii.b2a_hex(data) #ASIIC码转16字符

		cliend_data=list(map(lambda s:s,data))#字符串转list		
		
		self.datalen=len(data)

		while self.datalen:

			if  cliend_data[0]==0x15 and cliend_data[1]==0xFF: #判断是否为固定长度指令数据

				if cliend_data[2]==0x01:#电表设备

					dbobj=analysiscmd.DBcmdanalysic(cliend_data,self.datalen,self.transport.getPeer())
					#adbmysql.TwistedMysql.connectsetting(**db_settings)
					self.datalen=dbobj.getdata(adbmysql.TwistedMysql.interctionthread,**dbdatamodel)

				elif cliend_data[2]==0x02:#空调设备

					self.mylogger.info("KT device")					

				else: #不是正确的指令
							
					self.mylogger.info("NO this type device")
					
			elif cliend_data[1]==0xFE and cliend_data[0]==0x15: #判断是否为不定长度指令数据，透传等..
				
				self.mylogger.info("variable len!!!")
		
			else: #不是正确的指令	         

				self.mylogger.info("{} cmd error,cuting down connection!!! \n".format(self.transport.getPeer()))
				self.transport.abortConnection()
				break
			
	def SEND(self,uuid,databody):

		try :

			datapack[data[4:]]

			self.globalv.get(b'0000000099000000000700').write(bytes(struct.pack('B',1)))#uuid+data{uuid:data}

		except AttributeError:

			self.mylogger.info('ERROR :Django client not login\n')

	def connectionLost(self, reason):
		"""
		Called when the connection is shut down.

		Clear any circular references here, and any external references
		to this Pr  otocol.  The connection has been closed.

		@type reason: L{twisted.python.failure.Failure}
		"""

		global ConnectNum,ConnetNum_Max

		ConnectNum = ConnectNum - 1

		logging.info("{} device disconnected,the ConnectNum: {}, the max ConnectNum {}\n"
					.format(self.transport.getPeer(),ConnectNum,ConnetNum_Max))    
	
	def connectionMade(self):

		#self.globalv.set()

		global ConnectNum
		global ConnetNum_Max
		global ConnectLost_Num

		ConnectNum = ConnectNum + 1

		if ConnetNum_Max < ConnectNum:

			ConnetNum_Max = ConnectNum
		else:
			ConnectLost_Num = ConnetNum_Max - ConnectNum
#		try:
#			with open(self.loglocal,'a') as Logmsg
#				Logmsg.write("{} login success,the ConnectNum is {} ,the max connectNum is {} at {}\n "
#					.format(self.transport.getPeer(),ConnectNum,ConnetNum_Max,time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))
#		except :
#			print("信息无法写入日志或路径问题 at {}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))	
		logging.info("{} login success,the ConnectNum is {} ,the max connectNum is {}\n "
					.format(self.transport.getPeer(),ConnectNum,ConnetNum_Max))	
						
	
class EchoFactory(protocol.Factory):

	def buildProtocol(self, addr):  #重写该函数，该函数返回protocol的实例

		return Echo()


if __name__ == '__main__':

	ConnectNum=0
	ConnetNum_Max=0
	ConnetLost_Num=0

	mysqlsetting =	{   'host':'localhost',
						'port':3306,
						'user':'root',
						'passwd':'',
						'db':'device',
						'use_unicode':True,
						'charset':'utf8'
					} 
	dbdatamodel = {	
					'table':'dbdevice',
					'UUID':'',
					'TOTAL_POWER':'',
					'ONOFF':'OFF',
					'TIMES':''
				}

	if os.name =='nt':
		loglocal = 'E:\Python-L\TwistedTcpServerV3-addadbapi\log\log.txt'
	else:
		loglocal='/home/Iotserver/TwistedTcpServerV3-addadbapi/log/log.txt'

	adbmysql.TwistedMysql.connectsetting(**mysqlsetting)
	#TwistedMysql.interctionthread(**data)

	logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
								datefmt='%a,%d %b %Y %H:%M:%S',
                				filename=loglocal,
                				filemode='a')																																																																																																																																																																																																																																		

	Devfactory=EchoFactory()

	reactor.listenTCP(8001,Devfactory)

	print("Listening....\n")
 
	reactor.run()
