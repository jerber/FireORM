import pytest
import os
from datetime import datetime, timedelta, timezone
import random
import string

from fireorm.Models import DateModel, Model
from fireorm.Fields import *
from fireorm import db

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/jeremyberman/Downloads/my-serv.json'

def gen_random_str(n=8):
	return ''.join(random.choice(string.ascii_letters) for _ in range(n))

class Pet(DateModel):
	type = TextField(required=True, default='Dog')
	age = NumberField()


class Teacher(DateModel):
	name = TextField(required=True)
	age = NumberField(required=True)
	pet = NestedModel(Pet, default=Pet())

	class Meta:
		collection_name = 'teacher-testing'
		fields_to_print = ['createdAt']


class Manager(Model):
	name = TextField(required=True)
	age = NumberField(required=True)
	company = TextField(required=True, default='Dunder Mifflin')
	startedWorkingAt = DateField()


class Student(Model):
	name = TextField()
	school = TextField(required=True, default='UPenn')

	class Meta:
		collection_name = 'students'
		fields_to_print = ['name']

def test_connection():
	assert db.conn.project == 'europe-tester'

def test_basic_model():
	manager = Manager(name='Jerry', age = 21)
	assert manager.name == 'Jerry'
	assert manager.age == 21
	assert manager.company == 'Dunder Mifflin'
	assert manager.startedWorkingAt == None
	manager.save()
	print(manager, manager)
	# now make sure it saved, and also that key and id are interchangable
	print("KEY FIRST", manager.key)
	print(Manager.collection.get(manager.key))
	assert Manager.collection.get(manager.id) == Manager.collection.get(manager.key)
	new_manager = Manager.collection.get(manager.id)
	assert new_manager.startedWorkingAt == None
	now = datetime.utcnow().replace(tzinfo=timezone.utc)
	new_manager.startedWorkingAt = now
	new_manager.save()
	third_man = Manager.collection.get(new_manager.id)
	assert third_man.startedWorkingAt == now

def test_querying_of_models():
	# first make sure meta is working
	s = Student()
	# test default
	s.school = 'UPenn'
	assert 'students' == s.key.split('/')[0]
	m = Manager()
	assert  'manager' == m.key.split('/')[0]

	starting_time = datetime.utcnow()
	c = Student(name=gen_random_str()).save()
	m = Student(name=gen_random_str()).save()

	arr_of_names = [c.name, m.name]

	students = Student.collection.where('name', 'in', arr_of_names).stream()
	print(students)
	assert len(students) == 2
	c.delete()
	m.delete()

	students = Student.collection.where('name', 'in', arr_of_names).stream()
	print(students)
	assert len(students) == 0

