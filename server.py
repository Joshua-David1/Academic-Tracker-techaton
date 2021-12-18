from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-data-colletion.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(50),nullable=False)
	role=db.Column(db.String(50),nullable=False)

db.create_all()

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/admin-panel")
def admin_page():
	return render_template('admin-page.html')

if __name__ == "__main__":
	app.run(debug=True)
