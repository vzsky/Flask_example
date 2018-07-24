from data_port import check, scan
import json
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from todolist import  add, rm, get


# App config ##################################################################################################


app = Flask(__name__)
app.secret_key = '1qaz@WSX3edc$RFV5tgb^YHN'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/talay/dev_root/todo.db'

db = SQLAlchemy(app)


#This is for TODOLIST ##########################################################################################

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

@app.before_request
def be4req():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route('/login', methods=['POST', 'GET'])
def login():
	if g.user :
		return redirect(url_for('todolist'))
	if request.method == 'POST':
		thisuser = user.query.filter_by(username=request.form['username']).first()
		if thisuser :
			if request.form['password'] == thisuser.password:
				session['user'] = request.form['username']
				return redirect(url_for('todolist'))
			else : 
				mes = 'Wrong password / Used username'
				return render_template('login.html', mes=mes)
		else :
			if request.form['username'] and request.form['password']:
				adduser = user(username=request.form['username'], password=request.form['password'])
				db.session.add(adduser)
				db.session.commit()
				session['user'] = request.form['username']
				return redirect(url_for('todolist'))
			else :
				mes = 'Input username and password to sign up'
				return render_template('login.html', mes=mes)
	return render_template('login.html')
	

@app.route('/todolist/admin/rmuser/<id>')
def rmuser(id):
	rm(id, user, db)
	return redirect(url_for('todolist'))

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('todolist'))

@app.route('/todolist')
def todolist():
	if g.user:
		thisuser = user.query.filter_by(username=session['user']).first()
		if thisuser.username == 'admin':
			alluser = user.query.all()
			return render_template('admin.html', alluser=alluser)
		complete, incom, todos, notes = get(hw, thisuser)
		return render_template('todo.html',user=session['user'], complete=complete, incom=incom, todos=todos, notes=notes)
	return redirect(url_for('login'))

@app.route('/todolist/add', methods=['POST'])
def add():
	if g.user :
		thisuser = user.query.filter_by(username=session['user']).first()
		add(thisuser, request.form['add'], 0, db)
	return redirect(url_for('todolist'))

@app.route('/todolist/addt', methods=['POST'])
def addt():
	if g.user :
		thisuser = user.query.filter_by(username=session['user']).first()
		add(thisuser, request.form['addt'], 1, db)
	return redirect(url_for('todolist'))

@app.route('/todolist/addn', methods=['POST'])
def addn():
	if g.user :
		thisuser = user.query.filter_by(username=session['user']).first()
		add(thisuser, request.form['addn'], 2, db)
	return redirect(url_for('todolist'))

@app.route('/todolist/c/<id>')
def complete(id):
	if g.user :
		ctd = hw.query.filter_by(id=int(id)).first()
		ctd.complete = True
		db.session.commit()
	return redirect(url_for('todolist'))

@app.route('/todolist/rm/<id>')
def rm(id):
	if g.user :
		rm(id, hw, db)
	return redirect(url_for('todolist'))



#This is for PORTCHECKER #####################################################################################


def get_remote_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route('/port', methods=['GET' , 'POST'])
def portcheck():
    _ip = get_remote_ip()
    num = []
    for x in range (9):
        num.append(x)
    return render_template('portcheck.html', ip=_ip, nums=num)

@app.route('/port/scan', methods=['POST'])
def toscan():
    _ip = get_remote_ip()
    ar, p, c, s = scan(_ip)
    return jsonify({'result' : ar, 'ports' : p, 'color' : c, 'services' : s})

@app.route('/port/update', methods=['POST'])
def update():
    _ip = get_remote_ip()
    port = int(request.form['port'])
    res, c = check(_ip, port)
    return jsonify({'result' : res, 'color' : c })


############################################################################################################


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=7000)
