class Field:

	def __init__(self, validate, value=None, required=False, default=None, call=False):
		self.validate = validate
		self.value = value
		self.required = required
		self.default = default
		self.call = call
		self.used_default = False

		if self.value is None and self.default is not None:
			self.value = self.default if not self.call else self.default()
			self.used_default

		if self.value is not None:
			self.validate(self.value)

	def __repr__(self):
		return f'<*{self.get_class_name()}* value: {self.value}, required: {self.required}, default: {self.default}>'

	@classmethod
	def get_class_name(cls):
		return cls.__name__
