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


if __name__ == '__main__':
	# test_teacher_model()
	# print(fireorm.db.conn.__dict__)
	# test_queries()
	test_student_model()