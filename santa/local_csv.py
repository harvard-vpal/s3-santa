import csv
from config import config


class LocalCSV:
	def __init__(self):
		self.file = config.LOCAL_CSV


	def is_blank(self):
		with open(self.file, 'rb') as f:
			reader = csv.reader(f)
			if len(list(reader))>1:
				return False
			else:
				return True


	def append_row(self,row):
		with open(self.file, 'ab') as f:
			writer = csv.writer(f)
			writer.writerow(row)


	def initialize_columns(self):
		"""
		Add column headers to blank spreadsheet, only needs to be done once
		"""
		if not self.is_blank():
			raise Exception('Spreadsheet not blank')

		self.append_row([
			'Name',
			'Access Key ID',
			'Secret Access Key',
			'Description'
		])
		print "Initialized columns in local csv file"

		
	def add_user(self,user):
		"""
		Add row for new user
		"""
		self.append_row([
			user.name, 
			user.access_key_id, 
			user.secret_access_key,
			user.description,
		])
		print "Added record for user"


if __name__=='__main__':
	c = LocalCSV()
	print c.initialize_columns()
