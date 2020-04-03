from datetime import datetime
from fireorm.Models import Model
from fireorm.Fields import DateField
from fireorm.utils import make_update_obj


class DateModel(Model):
	createdAt = DateField(required=True, default=datetime.utcnow, call=True)
	lastUpdated = DateField(required=True, default=datetime.utcnow, call=True)

	def save(self, lastUpdated=None, **kwargs):
		if not lastUpdated: self.lastUpdated = datetime.utcnow()
		super().save(**kwargs)

	def update(self, lastUpdated=None, **kwargs):
		if not lastUpdated: self.lastUpdated = datetime.utcnow()
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
