import firebase_admin
from firebase_admin import credentials, firestore


class Database:

	def __init__(self):
		self._conn = None

	def connect(self, creds=None, from_file=None):
		if not creds and not from_file:
			raise Exception("Credentials or service account json file path required to connect with firestore")
		if not creds:
			creds = credentials.Certificate(from_file)
		try:
			firebase_admin.initialize_app(creds)
		except Exception as e:
			if 'The default Firebase app already exists' in str(e):
				raise Exception(
					'If you want to connect to Firestore from_file, make sure fireorm.connect(from_file=<YOUR FILE>) '
					'comes directly after importing FireORM for the first time.')
		self._conn = firestore.client()

	@property
	def conn(self):
		if self._conn is None:
			firebase_admin.initialize_app()
			self._conn = firestore.client()
		return self._conn
