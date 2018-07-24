from main import db

class hw (db.Model) :
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(200))
	complete = db.Column(db.Boolean)
	field = db.Column(db.Integer)
	userid = db.Column(db.Integer)
	db.session.commit()

class user (db.Model) :
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	password = db.Column(db.String(100))
	db.session.commit()

def get(hw, thisuser):
	complete = hw.query.filter_by(userid=thisuser.id).filter_by(complete=True).filter_by(field=0).all()
	incom = hw.query.filter_by(userid=thisuser.id).filter_by(complete=False).filter_by(field=0).all()
	todos = hw.query.filter_by(userid=thisuser.id).filter_by(field=1).all()
	notes = hw.query.filter_by(userid=thisuser.id).filter_by(field=2).all()
	return session['user'], complete, incom, todos, notes

def add(thisuser, tex, f,  db):
	td = hw(userid=thisuser.id, text=tex, complete=False, field=f)
	db.session.add(td)
	db.session.commit()

def rm(id, obj, db):
		std = hw.query.filter_by(id=int(id)).first()
		db.session.delete(std)
		db.session.commit()