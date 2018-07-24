def get(hw, thisuser):
	complete = hw.query.filter_by(userid=thisuser.id).filter_by(complete=True).filter_by(field=0).all()
	incom = hw.query.filter_by(userid=thisuser.id).filter_by(complete=False).filter_by(field=0).all()
	todos = hw.query.filter_by(userid=thisuser.id).filter_by(field=1).all()
	notes = hw.query.filter_by(userid=thisuser.id).filter_by(field=2).all()
	return complete, incom, todos, notes

def additem(thisuser, tex, f, hw,  db):
	td = hw(userid=thisuser.id, text=tex, complete=False, field=f)
	db.session.add(td)
	db.session.commit()

def rm(id, obj, db):
		std = hw.query.filter_by(id=int(id)).first()
		db.session.delete(std)
		db.session.commit()