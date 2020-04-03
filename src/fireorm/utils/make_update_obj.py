from fireorm import DELETE_FIELD


def make_update_obj_rec(original, new, current_path, update_d):
	# first get all the deletions of fields
	del_fields = original.keys() - new.keys()
	for field in del_fields:
		update_d['.'.join([*current_path, field])] = DELETE_FIELD

	# now get all the object and value changes
	for field, new_value in new.items():
		if not field in original:
			update_d['.'.join([*current_path, field])] = new_value
			continue
		original_value = original[field]
		if new_value == original_value:
			continue
		# this is the case where they are different...
		if type(new_value) != type(original_value) or not type(new_value) == dict:
			update_d['.'.join([*current_path, field])] = new_value
			continue
		# now you know this is a dict and it's different
		make_update_obj_rec(original_value, new_value, [*current_path, field], update_d)


def make_update_obj(original, new):
	update_d = {}
	make_update_obj_rec(original=original, new=new, current_path=[], update_d=update_d)
	return update_d
