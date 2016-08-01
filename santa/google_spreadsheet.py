from oauth2client.service_account import ServiceAccountCredentials
import gspread
from config import config
import os


class GoogleSpreadsheet:
	def __init__(self):
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.expanduser(config.GOOGLE_KEYFILE), scope)
		client = gspread.authorize(credentials)

		if config.GOOGLE_SPREADSHEET_ID:
			self.spreadsheet = client.open_by_key(config.GOOGLE_SPREADSHEET_ID).sheet1
		elif config.GOOGLE_SPREADSHEET_NAME:
			self.spreadsheet = client.open(config.GOOGLE_SPREADSHEET_NAME).sheet1
		else:
			raise Exception("Google spreadsheet not specified in config")


	def is_blank(self):
		return bool(self.spreadsheet.get_all_values())


	def append_row(self,row):
		'''
		Generic function to add row to spreadsheet
		'''
		self.spreadsheet.append_row(row)


	def initialize(self):
		'''
		Clear (resize) spreadsheet and apply column headers
		only needs to be done once
		'''
		self.spreadsheet.insert_row([
			'Name',
			'Access Key ID',
			'Secret Access Key',
			'Description'
		],index=1)
		print "Initialized columns on Google spreadsheet"

		self.spreadsheet.resize(rows=1,cols=4)

	def add_user(self,user):
		'''
		Add row for new user, takes as input a user object
		'''
		self.append_row([
			user.name, 
			user.access_key_id, 
			user.secret_access_key,
			user.description,
		])
		print "Added user to google spreadsheet"


if __name__=='__main__':
	gs = GoogleSpreadsheet()
	gs.initialize()

