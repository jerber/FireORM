import time
import os

import fireorm

from fireorm.Models import Model, DateModel

from fireorm.Fields import *


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

def test_teacher_model():
	t = Teacher()
	t.age = 20
	t.name = 'char'
	batch = fireorm.batch()
	t.save(batch=batch)
	batch.commit()
	print(t)


def test_queries():
	ts = Teacher.collection.order_by('createdAt', 'asc').limit(2).stream()
	print(ts)


def test_user_model():
	class Salesman(Model):
		name = TextField()
		company = TextField()

	s = Salesman()
	s.name = 'Jim'
	s.save()

	s = Salesman.collection.get(s.id)
	print(s.name)  # Jim


def test_student_model():
	class Student(Model):
		name = TextField()
		school = TextField(required=True, default='UPenn')

		class Meta:
			collection_name = 'students'
			fields_to_print = ['name']

	s = Student(name='Amy Gutman')
	s.save()  # creates a new document in the "students" collection
	print(s)  #

	class ExchangeStudent(Student):
		originalCountry = TextField(required=True)

		class Meta:
			collection_name = 'exchangeStudents'
			fields_to_print = None

	e = ExchangeStudent(originalCountry='UK')
	print(e.school)  # UPenn
	e.save()
	print(e)

def manager_example():
	m = Manager(name='Michael Scott')  # you can pass in fields or set them later
	m.age = 45
	m.save()  # Success! New doc in collection "manager" as: { name: Michael Scott, age: 45, company: Dunder Mifflin }

	m = Manager()
	m.name = 'Dwight Schrute'
	m.save()  # Exception since age is required but not given

def queries_example():
	managers = Manager.collection.where('name', '==', 'Michael Scott').limit(1).stream()
	print(managers)

	manager = Manager.collection.get('Z8S75KU2n7QQnIm2cExy')
	print(manager)
if __name__ == '__main__':
	# test_teacher_model()
	# print(fireorm.db.conn.__dict__)
	# test_queries()
	# test_student_model()
	queries_example()
	# manager_example()