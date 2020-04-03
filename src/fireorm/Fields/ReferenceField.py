from fireorm.Fields import Field


class ReferenceField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=ReferenceField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not 'DocumentReference' in str(type(value)):
			raise Exception(f'Value: {value} is not valid reference! It is type: {type(value)}')


if __name__ == '__main__':
	b = ReferenceField()
	# b.validate(True)
	# b.validate(False)
	# b.validate(None)
	# b.validate('hi')