from email.policy import default
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

def setup_db(app):
	db.app = app
	db.init_app(app)
	
	with app.app_context():
		db.create_all()

'''
Users
'''
class User(db.Model):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(30), nullable=False)
	username = Column(String(30), nullable=False, unique=True)
	email = Column(String(255), nullable=False, unique=True)
	password = Column(String(255), nullable=False)
	phone = Column(String(50), nullable=False, unique=True)
	country = Column(String(50), nullable=False)
	city = Column(String(50), nullable=False)
	bio = Column(String(255), nullable=False, default='')
	sex = Column(String(10), nullable=False)
	love_state = Column(String(50), nullable=False, default='single')
	auth_type = Column(String(10), nullable=False, default='level_1')
	auth_perm = Column(String(255), nullable=False, default='get:tasks, get:cars')
	date_of_creation = Column(DateTime, nullable=False, default=datetime.today)
	image = Column(String(30), nullable=False, default='user.png')
	active = Column(Boolean, nullable=False, default=False)
	rules = db.relationship('Rule', backref="users", cascade="all,delete", lazy=True)
	bucketlists = db.relationship('Bucketlist', backref="users", cascade="all,delete", lazy=True)
	kinks = db.relationship('Kink', backref="users", cascade="all,delete", lazy=True)
	fetishes = db.relationship('Fetish', backref="users", cascade="all,delete", lazy=True)
	
	def __repr__(self):
		return f'<User.ID: {self.id}>'
	
	def __init__(self, name, username, email, password, phone, country, city, bio, sex, love_state, auth_type, auth_perm, date_of_creation, image, active):
		self.name = name
		self.username = username
		self.email = email
		self.password = password
		self.phone = phone
		self.country = country
		self.city = city
		self.bio = bio
		self.sex = sex
		self.love_state = love_state
		self.auth_type = auth_type
		self.auth_perm = auth_perm
		self.date_of_creation = date_of_creation
		self.image = image
		self.active = active
	
	def insert(self):
		#try:
		db.session.add(self)
		db.session.commit()
		#except:
		#	db.session.rollback()
	
	def update(self):
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'username': self.username,
    		'email': self.email,
    		'password': self.password,
			'phone': self.phone,
			'country': self.country,
			'city': self.city,
			'bio': self.bio,
			'sex': self.sex,
			'love_state': self.love_state,
    		'auth_type': self.auth_type,
    		'auth_perm': self.auth_perm,
    		'date_of_creation': self.date_of_creation,
    		'image': self.image,
    		'active': self.active
		}

'''
Relationship
'''
class Relationship(db.Model):
	__tablename__ = 'relationships'
	
	id = Column(Integer, primary_key=True)
	hubby = Column(Integer, ForeignKey('users.id'), nullable=False)
	wifey = Column(Integer, ForeignKey('users.id'), nullable=False)
	status = Column(String(50), nullable=False, default='requested')
	date_of_creation = Column(DateTime, nullable=False, default=datetime.today)
	
	def __repr__(self):
		return f'<Relationship.ID: {self.id}>'
	
	def __init__(self, hubby, wifey, status, date_of_creation):
		self.hubby = hubby
		self.wifey = wifey
		self.status = status
		self.date_of_creation = date_of_creation
	
	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()
	
	def update(self):
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'hubby': self.hubby,
			'wifey': self.wifey,
			'status': self.status,
			'date_of_creation': self.date_of_creation
		}


'''
Rules
'''
class Rule(db.Model):
	__tablename__ = 'rules'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	description = Column(String(255), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	#relationship_id = Column(Integer, ForeignKey('relationships.id'), nullable=False)
	
	def __repr__(self):
		return f'<Rule.ID: {self.id}>'
	
	def __init__(self, name, description):
		self.name = name
		self.description = description
	
	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()
	
	def update(self):
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description
		}

'''
Bucketlist
'''
class Bucketlist(db.Model):
	__tablename__ = 'bucketlists'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	description = Column(String(255), nullable=False)
	status = Column(String(50), nullable=False, default='listed')
	date_of_creation = Column(DateTime, nullable=False, default=datetime.today)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	#relationship_id = Column(Integer, ForeignKey('relationships.id'), nullable=False)
	
	def __repr__(self):
		return f'<Bucketlist.ID: {self.id}>'
	
	def __init__(self, name, description, status, date_of_creation):
		self.name = name
		self.description = description
		self.status = status
		self.date_of_creation = date_of_creation
	
	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()
	
	def update(self):
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'status': self.status
		}

'''
Kinks
'''
class Kink(db.Model):
	__tablename__ = 'kinks'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	description = Column(String(255), nullable=False)
	status = Column(String(50), nullable=False, default='listed')
	date_of_creation = Column(DateTime, nullable=False, default=datetime.today)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	#relationship_id = Column(Integer, ForeignKey('relationships.id'), nullable=False)
	
	def __repr__(self):
		return f'<Kink.ID: {self.id}>'
	
	def __init__(self, name, description, status, date_of_creation):
		self.name = name
		self.description = description
		self.status = status
		self.date_of_creation = date_of_creation
	
	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()
	
	def update(self):
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'status': self.status
		}

'''
Fetish
'''
class Fetish(db.Model):
	__tablename__ = 'fetish'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	description = Column(String(255), nullable=False)
	status = Column(String(50), nullable=False, default='listed')
	date_of_creation = Column(DateTime, nullable=False, default=datetime.today)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	#relationship_id = Column(Integer, ForeignKey('relationships.id'), nullable=False)
	
	def __repr__(self):
		return f'<Fetish.ID: {self.id}>'
	
	def __init__(self, name, description, status, date_of_creation):
		self.name = name
		self.description = description
		self.status = status
		self.date_of_creation = date_of_creation
	
	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()
	
	def update(self):
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'status': self.status
		}
