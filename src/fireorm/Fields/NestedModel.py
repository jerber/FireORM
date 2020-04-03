from fireorm.Fields import Field

class NestedModel(Field):

	def __init__(self, cls, **kwargs):
		self.cls = cls
		super().__init__(validate=self.validate, **kwargs)

	def validate(self, value):
		#validate each field here
		if not isinstance(value, self.cls):
			raise Exception(f'Value: {value} is not an instance of {self.cls.__name__}!')
		value.validate_db_fields()