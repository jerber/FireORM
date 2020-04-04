from fireorm import db, ASCENDING, DESCENDING


class Query:

	def __init__(self, cls):
		print('init in query')
		self.cls = cls
		self.collection_path = self.cls.get_collection_name()
		self.create_query()

	def create_query(self):
		self.firebase_query = db.conn.collection(self.collection_path)

	def add_parent(self, parent_key):
		if not parent_key: return
		self.collection_path = parent_key + '/' + self.collection_path
		print('collection_path with parent now', self.collection_path)
		self.create_query()

	def parent(self, parent_key):
		self.add_parent(parent_key)
		return self

	def document(self, doc_path):
		self.firebase_query = self.firebase_query.document(doc_path)
		return self

	def collection_group(self):
		self.firebase_query = db.conn.collection_group(self.cls.get_collection_name())
		return self

	def collection(self, collection_path):
		self.firebase_query = self.firebase_query.collection(collection_path)
		return self

	def where(self, field, action, value):
		self.firebase_query = self.firebase_query.where(field, action, value)
		return self

	def order_by(self, field, direction=None, **kwargs):
		if direction: kwargs['direction'] = direction
		if kwargs.get('direction', None) == 'asc':
			kwargs['direction'] = ASCENDING
		if kwargs.get('direction', None) == 'desc':
			kwargs['direction'] = DESCENDING
		self.firebase_query = self.firebase_query.order_by(field, **kwargs)
		return self

	def start_at(self, fields):
		self.firebase_query = self.firebase_query.start_at(fields)
		return self

	def start_after(self, fields):
		self.firebase_query = self.firebase_query.start_after(fields)
		return self

	def end_at(self, fields):
		self.firebase_query = self.firebase_query.end_at(fields)
		return self

	def end_before(self, fields):
		self.firebase_query = self.firebase_query.end_before(fields)
		return self

	def limit(self, limit):
		self.firebase_query = self.firebase_query.limit(limit)
		return self

	def stream(self, **kwargs):
		docs = list(self.firebase_query.stream(**kwargs))
		return [self.cls(from_db=True, key=self.key_from_ref(doc.reference), **doc.to_dict()) for doc in docs]

	def get(self, id=None, **kwargs):
		paths = id.split('/')
		if len(paths) == 2: id = paths[-1]
		doc = self.firebase_query.get(**kwargs) if not id else self.firebase_query.document(id).get(**kwargs)
		if not 'DocumentSnapshot' in (str(type(doc))): return None
		d = doc.to_dict()
		if not d: return None
		return self.cls(from_db=True, key=self.key_from_ref(doc.reference), **doc.to_dict())

	def get_all(self, ids, **kwargs):
		doc_refs = [db.conn.collection(self.collection_path).document(id) for id in ids]
		docs = db.conn.get_all(doc_refs, **kwargs)
		return [self.cls(from_db=True, key=self.key_from_ref(doc.reference), **doc.to_dict()) for doc in docs]

	@staticmethod
	def key_from_ref(ref):
		return '/'.join(ref._path)

	def collections(self):
		return self.firebase_query.collections()

	def collections_names(self):
		return [coll.id for coll in self.firebase_query.collections()]

	def get_subcollections(self, id=None):
		# if this is not a doc ref then return
		if id: self.firebase_query = self.firebase_query.document(id)
		if 'DocumentReference' not in str(type(self.firebase_query)):
			raise Exception(
				f'You cannot get subcollections of a CollectionRefernce. This query is type: {type(self.firebase_query)}')

		collection_names_d = {cls.get_collection_name(): cls for cls in self.cls.get_all_subclasses_of_model()}
		queries = []
		for collection in self.firebase_query.collections():
			collection_name = collection._path[-1]
			if collection_name in collection_names_d:
				q = Query(collection_names_d[collection_name])
				q.parent(Query.key_from_ref(self.firebase_query))
				queries.append(q)
		return queries

	def __repr__(self):
		return f'<*Query* cls: {self.cls.__name__}>'
