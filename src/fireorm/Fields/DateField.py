from datetime import datetime
from fireorm.Fields import Field
from fireorm import SERVER_TIMESTAMP


class DateField(Field):

	def __init__(self, **kwargs):
		super().__init__(validate=DateField.validate, **kwargs)

	@staticmethod
	def validate(value):
		if not type(value) == datetime and not (
				type(value) == type(SERVER_TIMESTAMP) and 'server timestamp' in value.description):
			raise Exception(f'Value: {value} is not valid Date! It is type: {type(value)}')


if __name__ == '__main__':
	date = datetime.utcnow()
	d = DateField()
	d.validate(date)
