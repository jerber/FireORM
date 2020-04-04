import pprint
import copy

from datetime import datetime

from fireorm.Fields import Field, NullField, NestedModel

from fireorm import db

from fireorm.Queries import Query

from fireorm.utils import make_update_obj


class ModelMeta(type):
	"""https://stackoverflow.com/questions/128573/using-property-on-classmethods"""

	@property
	def collection(cls):
		return Query(cls)

	@property
	def collection_group(cls):
		return Query(cls).collection_group()


class Model(metaclass=ModelMeta):

	def init_variables(self):
		self._key = None
		self._id = None
		self._ref = None
		"""_class_fields are all the Field objects as a dict, w the key as what their variables are called"""
		self._class_fields = {}
		self._parent = None
		self._kwargs_from_db = {}
		self._og_kwargs = {}
		self.nested = False

	def __init__(self, id=None, key=None, parent=None, from_db=False, ignore_defaults=False, ignore_class_fields=False, **kwargs):
		self._init_done = False
		self.ignore_class_fields = ignore_class_fields
		if not self.ignore_class_fields: self.ignore_class_fields = ignore_defaults

		if id and '/' in id and not key: key = id

		self.init_variables()

		if from_db: self._kwargs_from_db = copy.deepcopy(kwargs)

		self._og_kwargs = copy.deepcopy(kwargs)

		self._parent = parent

		self.make_ref_from_key_or_id(key, id)

		# add all of the db class fields
		self._class_fields = self.get_class_fields()

		# now set all the fields to None so that user is not confused
		self.set_class_field_values_in_self_to_none()

		# add all the default fields to the dict first, to be overwritten w kwargs
		if not self.ignore_class_fields: self.add_defaults_to_self_first()

		# now add the given fields to the obj
		self.from_dict(kwargs)

		self._init_done = True

	@classmethod
	def get_subclasses(cls):
		all_subs = []
		for sub in cls.__subclasses__():
			all_subs.append(sub)
			all_subs += sub.get_subclasses()
		return list(set(all_subs))

	@staticmethod
	def get_all_subclasses_of_model():
		all_subs = []
		for sub in list(Model.__subclasses__()):
			all_subs.append(sub)
			all_subs += sub.get_subclasses()
		return list(set(all_subs))

	def make_ref_from_key_or_id(self, key, id=None):
		if not key: return self.make_from_id(id)
		self._key = key
		self._ref = db.conn.document(self._key)
		self._id = self._key[self._key.rindex('/') + 1:]

	def make_from_id(self, id):
		collection_name = self.get_collection_name()
		collection_ref = db.conn.collection(collection_name) if not self._parent else self._parent._ref.collection(
			collection_name)
		self._ref = collection_ref.document() if not id else collection_ref.document(id)
		self._key = self.key_from_ref(self._ref)
		self._id = self.id_from_key(self._key)

	@staticmethod
	def key_from_ref(ref):
		return '/'.join(ref._path)

	@staticmethod
	def id_from_key(key):
		return key[key.rindex('/') + 1:]

	@property
	def key(self):
		return self._key

	@key.setter
	def key(self, key):
		self._key = key
		self.make_ref_from_key_or_id(key=key)

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
		self._id = id
		self.make_from_id(id=id)

	@property
	def parent(self):
		return self._parent

	@parent.setter
	def parent(self, parent):
		"""Does not currently reset id... if you want to just feed id=None"""
		self._parent = parent
		self.make_from_id(id=self._id)

	def get_datetime_from_firebase(self, value):
		if 'DatetimeWithNanoseconds' in str(type(value)):
			return datetime.fromtimestamp(value.timestamp(), tz=value.tzinfo)
		return value

	def from_dict(self, kwargs):
		for key, value in kwargs.items():
			value = self.get_datetime_from_firebase(value)
			# check for nested collections
			if isinstance(self._class_fields.get(key, None), NestedModel):
				value = self._class_fields[key].cls(from_db=True, **value)
			setattr(self, key, value)

	def add_defaults_to_self_first(self):
		for field, value in self._class_fields.items():
			if value.default is None and isinstance(self, NullField):
				setattr(self, field, value.value)
			elif value.default is not None:
				setattr(self, field, value.value)

	def validate_db_fields(self):
		for field, value in self._class_fields.items():
			current_value = self.__dict__.get(field, None)
			if current_value is None and not isinstance(value, NullField) and value.required:
				# if not field in self.__dict__ and value.required:
				raise Exception(f'Field: {field} is required but does not exist in self.')
			# should the fields be None or just not exist?
			if current_value is not None: value.validate(self.__dict__[field])

	def to_dict(self, nested=False):
		# what about the ID field... will tackle this later
		self.nested = nested
		d = {}
		for field in self._class_fields.keys():
			if field in self.__dict__:
				d[field] = self.__dict__[field]
				if isinstance(d[field], Model):
					d[field] = d[field].to_dict(nested=True)
				# make sure its not just a default field that is supposed to be none
				if d[field] is None and not isinstance(self._class_fields[field], NullField):
					del d[field]
		return d

	def get_class_fields(self):
		"""Get class fields from dir(self) and save the ones that are of type Field"""
		return {field: getattr(self, field) for field in dir(self) if isinstance(getattr(self, field), Field)}

	def set_class_field_values_in_self_to_none(self):
		for field in self._class_fields.keys():
			setattr(self, field, None)

	@classmethod
	def get_class_name(cls):
		return cls.__name__

	@classmethod
	def get_printable_fields(cls):
		return getattr(getattr(cls, 'Meta', {}), 'fields_to_print', None)

	def get_printable_fields_str(self):
		"""Will only print fields that are in _db_fields. If not specified, print all. If [], print nothing"""
		printable_fields = self.get_printable_fields()
		if printable_fields is None: printable_fields = self._class_fields.keys()
		strings = [f'{field}: {getattr(self, field, "does not exist")}' for field in printable_fields if
		           field in self._class_fields]
		return ', '.join(strings)

	def __repr__(self):
		default_print = f'<*{self.__class__.__name__}* key: {self._key}, id: {self._id}>'
		printable_strings = self.get_printable_fields_str()
		if printable_strings: default_print = f"{default_print[:-1]}, {printable_strings}>"
		return default_print

	####FIRESTORE STUFF HERE######

	@classmethod
	def get_collection_name(cls):
		return getattr(getattr(cls, 'Meta', {}), 'collection_name', None) or cls.__name__.lower()

	@classmethod
	def get(cls, id=None, key=None):
		path = f'{cls.get_collection_name()}/{id}' if not key else key
		print("PATH", path)
		d = db.conn.document(path).get().to_dict()
		if not d:
			raise Exception('Id does not exist.')
		return cls(key=path, from_db=True, **d)

	@classmethod
	def get_collection(cls):
		return cls.collection

	def get_subcollections(self):
		return self.get_collection().document(self.id).get_subcollections()

	def update(self, batch=None, create=False, return_result=False):
		if not self.ignore_class_fields: self.validate_db_fields()
		new = self.to_dict()
		update_d = new if not self._kwargs_from_db else make_update_obj(original=self._kwargs_from_db, new=new)
		print("update_d", update_d)
		try:
			res = self._ref.update(update_d) if not batch else batch.update(self._ref, update_d)
			# TODO if there are other fields in the DB this will not kill them
			if self._kwargs_from_db: self._kwargs_from_db = copy.deepcopy(new)
			return self if not return_result else res
		except Exception as e:
			if hasattr(e, 'message') and 'No document to update:' in e.message:
				if create:
					print('Creating since it did not exist')
					return self.save(batch=batch)
				else:
					raise (e)

	def delete(self, batch=None):
		print("DELETING....")
		return self._ref.delete() if not batch else batch.delete(self._ref)


	def __eq__(self, other):
		return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

	# TODO should I make merge true default?
	def save(self, batch=None, merge=False, return_result=False):
		if not self.ignore_class_fields: self.validate_db_fields()
		new = self.to_dict()
		res = self._ref.set(new, merge=merge) if not batch else batch.set(self._ref, new, merge=merge)
		if not merge: self._kwargs_from_db = copy.deepcopy(new)
		return self if not return_result else res
