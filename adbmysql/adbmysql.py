#_*_ coding : utf-8 _*_
from twisted.enterprise import adbapi
import pymysql
import logging

''' logging setting '''

sqllogging = logging.getLogger("login info")

class TwistedMysql(object):
	"""docstring for  TwistedMysql  异步使用mysql"""

	dbpooldict = {}

	def __init__(self):

		pass

	@classmethod		
	def connectsetting(cls,**kwargs):

		'''初始化mysql异步连接池'''

		cls.dbpooldict['dbpool'] = adbapi.ConnectionPool("pymysql",**kwargs) 

	@classmethod
	def interctionthread(cls,**kwargs):

		'''异步数据库操作初始化线程启动，以及注册方式错误回调函数'''
		try:
			query=cls.dbpooldict['dbpool'].runInteraction(cls.insterdata,**kwargs)
			#query=cls.dbpooldict['dbpool'].runInteraction(cls.insterdatatest)
			query.addErrback(cls.errorhanle)
		except Exception as e:

			sqllogging.info(e)

		
	@classmethod
	def errorhanle(cls):

		sqllogging.info('error')

	@classmethod
	def insterdatatest(cls,cursor):
		''' 插入数据'''
		inter_information = "INSERT INTO dbdevice (UUID,TOTAL_POWER,ONOFF) VALUES ('000000000002','222.44','OFF')"
		cursor.execute(inter_information)

	@classmethod
	def insterdata(cls,cursor,**kwargs):
		''' 插入数据'''
		try:
			data=[d for d in kwargs.keys()]

			inter_information =r"INSERT INTO {} ({},{},{},{}) VALUES ('{}','{}','{}','{}')\n"\
								.format(kwargs['table'],data[1],data[2],data[3],data[4],kwargs['UUID'],kwargs['TOTAL_POWER'],kwargs['ONOFF'],kwargs['TIMES'])
			cursor.execute(inter_information)
			sqllogging.info(inter_information)

		except Exception as e:

			logging.info('sql error:'+str(e))
		





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

			



		


