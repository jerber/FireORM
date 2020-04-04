import os
from fireorm.Models import DateModel
from fireorm.Fields import TextField

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/jeremyberman/Downloads/my-serv.json'

class User(DateModel):
	name = TextField(required=True, default='Jon')

def test_date_model():
	user = User()
	print(user)
	user.save()
	print(user)