import firebase_admin
from firebase_admin import credentials, auth, firestore

from fireorm.database import connect, db

def batch():
	return db.conn.batch()

def transaction(**kwargs):
	return db.conn.transaction(**kwargs)

ArrayUnion = firestore.firestore.ArrayUnion
ArrayRemove = firestore.firestore.ArrayRemove
DESCENDING = firestore.firestore.Query.DESCENDING
ASCENDING = firestore.firestore.Query.ASCENDING
Increment = firestore.firestore.Increment
SERVER_TIMESTAMP = firestore.firestore.SERVER_TIMESTAMP
DELETE_FIELD = firestore.firestore.DELETE_FIELD
