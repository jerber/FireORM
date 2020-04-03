from fireorm.Fields import Field


class BooleanField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=BooleanField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) == bool:
			raise Exception(f'Value: {value} is not valid boolean! It is type: {type(value)}')


if __name__ == '__main__':
	b = BooleanField()
	# b.validate(True)
	b.validate(False)
	# b.validate(None)
	# b.validate('hi')