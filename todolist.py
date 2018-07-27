def additem(thisuser, tex, f, obj,  db):
	td = obj(userid=thisuser.id, text=tex, complete=False, field=f)
	db.session.add(td)
	db.session.commit()

def remove(id, obj, db):
		std = obj.query.filter_by(id=int(id)).first()
		db.session.delete(std)
		db.session.commit()