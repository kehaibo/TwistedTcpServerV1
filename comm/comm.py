#-*- coding:utf-8 -*-
class GlobalValue:

	dict={}

	def set(self,key,value):

		try:


			self.dict[key]=value

			#print('{}:{}'.format(self.dict.keys(),self.dict.values()))

		except BaseException  as msg :

			raise msg

	def del_map(self, key):
		
		try:

			del self.dict[key]
			return self.dict
		except KeyError:
			print("key:'" + str(key) + "'  不存在")

	def get(self,key):

		try:

			return self.dict[key]

		except KeyError:

			return

	def checkkeys(self):

		UUID = [key for key in self.dict.keys()]

		return UUID





