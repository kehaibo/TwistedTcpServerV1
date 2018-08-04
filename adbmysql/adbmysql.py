#-*- coding : utf-8 -*-
from twisted.enterprise import adbapi
import pymysql

class TwistedMysql(object):
	"""docstring for  TwistedMysql  异步使用mysql"""

	dbpooldict = {}

	def __init__(self):

		pass

	@classmethod		
	def connectsetting(cls,**kwargs):

		'''初始化mysql异步连接池'''

		cls.dbpooldict['dbpool'] = adbapi.ConnectionPool("pymysql",kwargs) 

	@classmethod
	def interctionthread(cls,**kwargs):

		'''异步数据库操作初始化线程启动，以及注册方式错误回调函数'''

		print(cls.dbpooldict)
		print('interctionthread'+str(kwargs))

		#query=self.connectsetting().runInteraction(self.insterdata,**kwargs)
		query=cls.dbpooldict['dbpool'].runInteraction(cls.insterdatatest)

		print ("end"+str(query))

		query.addErrback(cls.errorhanle)

		query.addCallback(cls.errorhanle)

		
	@classmethod
	def errorhanle(cls):

		print ('error')

	@classmethod
	def insterdatatest(cls,cursor):
		''' 插入数据'''
		data=[d for d in kwargs.keys()]

		inter_information = "INSERT INTO dbdevice (UUID,TOTAL_POWER,ONOFF) VALUES ('000000000002','222.44','OFF')"
		cursor.execute(inter_information)

	def insterdata(self,cursor,**kwargs):
		''' 插入数据'''
		print (inter_information)
		data=[d for d in kwargs.keys()]

		inter_information = 'INSERT INTO {} ({},{},{}) VALUES ({},{},{})'\
							.format(kwargs['table'],data[1],data[2],data[3],kwargs['UUID'],kwargs['TOTAL_POWER'],kwargs['ONOFF'])
		print (inter_information)
		cursor.execute(inter_information)

		





if __name__ == '__main__':

	kw ={	'host':'127.0.0.1',
			'port':3306,
			'user':'root',
			'passwd':'',
			'db':'device',
			'use_unicode':True,
			'charset':'utf8'
		}
	data = {'table':'dbdevice',
			'UUID':'0000000000000000000001',
			'TOTAL_POWER':'8776',
			'ONOFF':'OFF'
			}

	TwistedMysql.interctionthread(**data).addCallback(TwistedMysql.errorhanle)
'''	keys = (UUID,TOTAL_POWER,ONOFF)
	values = {}
	
	TwistedMysql.connectsetting(**kw)
	TwistedMysql.interctionthread(kw['db'],)'''

			



		


