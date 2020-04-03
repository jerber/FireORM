from fireorm.Fields import Field


class MapField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=MapField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) == dict:
			raise Exception(f'Value: {value} is not valid dict! It is type: {type(value)}')


if __name__ == '__main__':
	field = MapField()
	field.validate({})
	# field.validate({'hi': 'yess'})
	# field.validate(None)
	# field.validate('hi')
	pass
