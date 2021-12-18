from flask import Flask, render_template, url_for, request, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = "Don't Care"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-data-colletion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(50),nullable=False)
	role=db.Column(db.String(50),nullable=False)

db.create_all()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=10)
    session.modified = True
    g.user = current_user

@app.route("/",methods=["GET","POST"])
def home_page():
	if current_user.is_authenticated:
		return redirect(f'{current_user.role}-dashboard')
	else:
		if request.method == "POST":
			username = request.form['username']
			password = request.form['password']
			user = User.query.filter_by(username=username).first()
			if user is not None:
				if password == user.password:
					role = user.role
					login_user(user)
					return redirect(f"/{role}-dashboard")
			return render_template('home.html')
		return render_template('home.html')

@app.route("/admin-dashboard")
def admin_page():
	if current_user.is_authenticated:
		if current_user.role == "admin":
			return render_template('admin-page.html')
		return redirect(f"{current_user.role}-dashboard")
	return redirect(url_for('home_page'))

@app.route("/facaulty-dashboard")
def facaulty_page():
	if current_user.is_authenticated:
		if current_user.role == "facaulty":
			return render_template('fac-dashboard.html')
		return redirect(f"{current_user.role}-dashboard") 
	return redirect(url_for('home_page'))

@app.route("/student-dashboard")
def student_page():
	if current_user.is_authenticated:
		if current_user.role == "student":
			return render_template('student-dashboard.html')
		return redirect(f"{current_user.role}-dashboard")
	return redirect(url_for('home_page'))

@app.route("/logout",methods=["POST","GET"])
def logout_page():
	if current_user.is_authenticated:
		if request.method == "POST":
			logout_user()
			return redirect(url_for('home_page'))
		return redirect(f"{current_user.role}-dashboard")
	else:
		return redirect(url_for('home_page'))

@app.route("/register", methods=["POST","GET"])
def register_page():
	if current_user.is_authenticated:
		if current_user.role == "admin":
			if request.method == "POST":
				username = request.form['username']
				password = request.form['password']
				role = request.form['role']
				new_user = User(username = username, password = password, role=role)
				db.session.add(new_user)
				db.session.commit()
				return redirect(url_for('admin_page'))
			return redirect(url_for('admin_page'))
		return redirect(url_for('home_page'))
	return redirect(url_for('home_page'))

if __name__ == "__main__":
	app.run(debug=True)
