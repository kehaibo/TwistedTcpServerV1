class DBCmd:

	def __init__(self,uuid):

		self.uuid=uuid

		self.read_power='FC12'+str(uuid).upper()+'B00100'

		self.read_addr ='FC12'+str(uuid).upper()+'B00300'

		self.openorclose='FC16'+str(uuid).upper()+'B00B01'


	def OpenorClose(self,open_or_close):

		return self.openorclose+str(open_or_close)

	def ReadPower(self):

		return self.read_power

	def ReadAddr(self):

		return self.read_addr

