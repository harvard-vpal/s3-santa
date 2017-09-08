import os
from abc import ABCMeta, abstractmethod


class UserStore(object):
	"""
	Class to handle interface with external user store 
		(for storing credentials/description)
	"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def add_user(self, user):
		"""
		Required method
		Arguments:
			user (s3santa.User): User object instance
		"""
		pass


class GoogleSpreadsheet(UserStore):
	"""
	Uses gspread library to interface with a google spreadsheet
	Uses the first worksheet in the doc
	"""
	def __init__(self, spreadsheet_id=None, google_keyfile=None):
		"""
		Arguments:
			spreadsheet_id (str): spreadsheet id from url
			credentials (str): path to credential file
		"""
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials

		if not spreadsheet_id and google_keyfile:
			raise Exception("Specify spreadsheet id and keyfile location")

		scope = ['https://spreadsheets.google.com/feeds']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(
			os.path.expanduser(google_keyfile), scope
		)
		client = gspread.authorize(credentials)
		self.spreadsheet = client.open_by_key(spreadsheet_id).sheet1


	def is_blank(self):
		return bool(self.spreadsheet.get_all_values())


	def append_row(self, row):
		"""
		Generic function to add row to spreadsheet
		"""
		self.spreadsheet.append_row(row)


	def initialize(self):
		"""
		Clear (resize) spreadsheet and apply column headers
		only needs to be done once
		"""
		self.spreadsheet.insert_row([
			'Name',
			'Access Key ID',
			'Secret Access Key',
			'Description'
		],index=1)
		print "Initialized columns on Google spreadsheet"

		self.spreadsheet.resize(rows=1,cols=4)


	def add_user(self, user):
		"""
		Add row for new user, takes as input a user object
		"""
		self.append_row([
			user.name, 
			user.access_key_id, 
			user.secret_access_key,
			user.description,
		])
		print "Added user to google spreadsheet"


class LocalCSV:
	def __init__(self, file):
		"""
		Arguments:
			file (str): path to csv file
		"""
		import csv

		self.file = file


	def is_blank(self):
		"""
		Check if file is empty
		"""
		with open(self.file, 'rb') as f:
			reader = csv.reader(f)
			if len(list(reader))>1:
				return False
			else:
				return True


	def append_row(self, row):
		"""
		Append a row of data to the spreadsheet
		"""
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

		
	def add_user(self, user):
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

