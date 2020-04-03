from fireorm.Fields import Field
from fireorm import ArrayUnion, ArrayRemove

class ListField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=ListField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) == list and not type(value) in [ArrayUnion, ArrayRemove]:
			raise Exception(f'Value: {value} is not valid list! It is type: {type(value)}')


if __name__ == '__main__':
	field = ListField()
	# field.validate([])
	field.validate(['hi','yas'])
	# field.validate(None)
	# field.validate('hi')