import os
if os.name != 'nt':
	import sys
	sys.path.append(r'/home/Iotserver/TwistedTcpServerV1')
else:
	import sys
	sys.path.append(r'E:\Python-L\TwistedTcpServerV1')
from CRC16 import CRC16
from cmdanalysis  import analysiscmd
import logging
import time




class CmdAnalysic(object):
	"""docstring for CmdAnalysic 命令解析的父类"""
	def __init__(self,data,datalen,device_ip):

		self.data = data 
		self.device_ip=device_ip
		self.uuid = ''
		self.datalen=datalen
		self.mylogger=logging.getLogger('device data')
		self.mylogger.setLevel
		stdprintf = logging.StreamHandler()
		if os.name !='nt':
			outputfile = logging.FileHandler('/home/Iotserver/TwistedTcpServerV1/log/data.txt')
			self.mylogger.addHandler(outputfile)
			if argv[1]=='True':
				self.mylogger.addHandler(stdprintf)
		else:
			outputfile = logging.FileHandler('E:\Python-L\TwistedTcpServerV1\log\data.txt')
			self.mylogger.addHandler(outputfile)


	def getuuid(self):

		pass

	def getdata(self):

		pass 

	def intersql(self):

		pass
	



class DBcmdanalysic(CmdAnalysic):
	"""docstring for DBcmdanalysic 电表设备"""
	def __init__(self,data,datalen,device_ip):

		super(DBcmdanalysic,self).__init__(data,datalen,device_ip)
		self.temp=''
		self.power=''
		self.switchstatus='' #开关状态


	def getuuid(self):
		''' get uuid from data ,as device unique identification '''
		self.uuid = [str(uuid) for uuid in self.data[3:14]]
		self.uuid = ''.join(self.uuid)
		return self.uuid

	def gettotalpower(self):
		'''获取总电量数据'''
		power = 0

		power = self.data[15]<<32|self.data[16]<<8|self.data[17]

		print(power)

		self.power = str(power)+'.'+str(self.data[18])
		
		return self.power


	def getdata(self,function,**kwagrs):
		''' get device data '''

		datadict=dict()

		try:

			markindex = int(self.data.index(0x15))
		
		except ValueError:

			self.transport.abortConnection()

		try:
		
			databuf=self.data[markindex:0x15]#数据体切割

		except UnboundLocalError:

			self.transport.abortConnection()

		try:

			CRCL,CRCH=CRC16.CRC16_1(databuf[:-2],len(databuf[:-2]))#crc校验

			if CRCL==databuf[-2] and CRCH==databuf[-1]:

				if databuf[14] == 0x01 : #电量数据类型

					kwagrs['UUID']=self.getuuid()
					kwagrs['TOTAL_POWER']=self.gettotalpower()
					function(**kwagrs)
				else:

					raise Exception('data type error')

				self.mylogger.info("Recive data :{} from {}\n ".format(databuf,self.device_ip))				
				
				del self.data[markindex:markindex+int(self.data[0])]#删除数据体已经截取的部分
				
				self.datalen=self.datalen-0x15
					
			else : #数据错误

				self.mylogger.info("CRC ERROR :Recive error data :{} from {} at {}\n ".format(databuf,self.device_ip,time.strftime("%Y-%m_%d %H:%M:%S",time.localtime())))				
				
				self.datalen=self.datalen-0x15
			
				if self.datalen<=0:
				
					self.datalen=0

		except 	IndexError :

			self.transport.abortConnection()

		return self.datalen




'''if __name__ == '__main__':
	
	obj = DBcmdanalysic(b'15FF01000000000000000000000101000000004042',len(b'15FF01000000000000000000000101000000004042'),12)
	print(obj.getdata())
	print(obj.getuuid())
'''

		
		
