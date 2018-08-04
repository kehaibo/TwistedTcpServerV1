
class DBCmd:

	def __init__(self,uuid):

		self.uuid=uuid

		self.read_power=b'15FF01000000000000000000000101000000004042'

		self.read_addr =''

		self.openorclose=''


	def OpenorClose(self,open_or_close):

		return self.openorclose+str(open_or_close)

	def ReadPower(self):

		return self.read_power

	def ReadAddr(self):

		return self.read_addr

