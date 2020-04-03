from fireorm.Fields import Field
from fireorm import Increment


class NumberField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=NumberField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) in [int, float] and not type(value) == Increment:
			raise Exception(f'<{NumberField.get_class_name()}> Value: {value} is not valid number! It is type: {type(value)}')

	@classmethod
	def get_class_name(cls):
		return cls.__name__