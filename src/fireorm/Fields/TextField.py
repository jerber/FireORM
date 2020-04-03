from fireorm.Fields import Field

class TextField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=TextField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) == str:
			raise Exception(f'Value: {value} is not valid string! It is type: {type(value)}')