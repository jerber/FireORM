from fireorm.Fields import Field


class NullField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=NullField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) is type(None):
			raise Exception(f'Value: {value} is not None! It is type: {type(value)}')


if __name__ == '__main__':
	field = NullField()
	# field.validate([])

	# field.validate(['hi','yas'])
	field.validate(None)
	# field.validate('hi')
	pass
