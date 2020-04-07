from datetime import datetime
from fireorm.Models import Model
from fireorm.Fields import DateField
from fireorm.utils import make_update_obj


class DateModel(Model):
	createdAt = DateField(required=True)
	lastUpdated = DateField(required=True)

	def save(self, lastUpdated=None, createdAt=None, **kwargs):
		self.lastUpdated = lastUpdated or datetime.utcnow()
		self.createdAt = createdAt
		if not createdAt and not self.createdAt and not self.ignore_class_fields: self.createdAt = datetime.utcnow()
		super().save(**kwargs)

	def update(self, lastUpdated=None, **kwargs):
		self.lastUpdated = lastUpdated or datetime.utcnow()
		super().update(**kwargs)

	def to_dict(self, nested=False):
		# if there was an update to the dict and this is nested, then update last updated
		current_d = super().to_dict()
		if not self._kwargs_from_db or not nested: return current_d
		update_d = make_update_obj(self._kwargs_from_db, current_d)
		if not update_d == {} or ('lastUpdate' in update_d and len(update_d) == 1):
			print('has changed in nested model, update d:', update_d)
			lastUpdated = update_d.get('lastUpdated', datetime.utcnow())
			self.lastUpdated = lastUpdated
			current_d['lastUpdated'] = lastUpdated
		return current_d
