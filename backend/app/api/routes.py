from ast import And
from operator import and_
from flask import Blueprint, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Relationship, Rule, Bucketlist, Kink, Fetish

api = Blueprint('api', __name__, url_prefix='/api')

ITEMS_PER_PAGE = 10

def paginate_items(request, selection):
	page = request.args.get('page', 1, type=int)
	start = (page - 1) * ITEMS_PER_PAGE
	end = start + ITEMS_PER_PAGE
	
	items = [item.format() for item in selection]
	current_items = items[start:end]
	
	return current_items

def format_name(name):
	for char in ['-', '+', '_', '/', ':', '!', '?', ',', '#', '*', '&']:
		name = name.replace(char, ' ')
	return name.replace(' ', '-').lower()

# GET Users
@api.route('/users', methods=['GET'])
def get_users():
	try:
		users = User.query.all()
		users_list = paginate_items(request, users)
		
		if len(users_list) == 0:
			abort(404)
		
		return jsonify({
			'success': True,
			'total_users': len(users),
			'current_users': len(users_list),
			'users': users_list
		}), 200
	except Exception as error:
		return jsonify({
			'success': False,
			'error': str(error)
		}), 500

# GET Single User
@api.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
	user = User.query.get_or_404(user_id)

	if user:
		try:
			data = {
				'id': user.id,
				'name': user.name,
				'username': user.username,
				'email': user.email,
				'phone': user.phone,
				'country': user.country,
				'city': user.city,
				'bio': user.bio,
				'sex': user.sex,
				'love_state': user.love_state,
				'auth_type': user.auth_type,
				'auth_perm': user.auth_perm,
				'date_of_creation': user.date_of_creation,
				'image': user.image,
				'active': user.active
			}
			return jsonify({
				'success': True,
				'user_ data': data,
				'user_id': user.id
			})
		except Exception as error:
			return jsonify({
				'success': False,
				'error': str(error)
			}), 200

#POST User
@api.route('/users', methods=['POST'])
def add_users():
	data = request.get_json()

	if data:

		name = data.get('name', None)
		username = data.get('username', None)
		email = data.get('email', None)
		password = data.get('password', None)
		phone = data.get('phone', None)
		country = data.get('country', None)
		city = data.get('city', None)
		bio = data.get('bio', None)
		sex = data.get('sex', None)
		love_state = data.get('love_state', None)

		if username:
			username_exist = User.query.filter(User.username == username).first()
			if username_exist is not None:
				response = {
					'success': False,
					'error': 'username already taken'
				}
				return jsonify(response), 403

		if email:
			email_exist = User.query.filter(User.email == email).first()
			if email_exist is not None:
				response = {
					'success': False,
					'error': 'email already exist'
				}
				return jsonify(response), 403
		
		if phone:
			phone_exist = User.query.filter(User.phone == phone).first()
			if phone_exist is not None:
				response = {
					'success': False,
					'error': 'phone already exist'
				}
				return jsonify(response), 403
		
		hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

		try:
			new_user = User(
				name=name,
				username=username,
				email=email,
				password=hashed_password,
				phone=phone,
				country=country,
				city=city,
				bio=bio,
				sex=sex,
				love_state=love_state,
				auth_type=None,
				auth_perm=None,
				date_of_creation=None,
				image=None,
				active=None
				)
			new_user.insert()
			return jsonify({
				'success': True,
				'created': new_user.id
			})
		except Exception as error:
			print(error)
			return jsonify({
				'success': False,
				'error': str(error)
			}), 200
	else:
		return jsonify({
			'success': False,
			'error': 'bad request body'
		}), 400

# DELETE User
@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
	user = User.query.get_or_404(user_id)

	if user:
		try:
			user.delete()
			return jsonify({
				'success': True,
				'deleted': user.id
			})
		except Exception as error:
			print(error)
			return jsonify({
				'success': False,
				'error': str(error)
			}), 200

# PATCH User
@api.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
	user = User.query.get_or_404(user_id)

	if user:
		data = request.get_json()
		if not data:
			abort(400)
		if data:
			name = data.get('name', None)
			username = data.get('username', None)
			email = data.get('email', None)
			password = data.get('password', None)
			phone = data.get('phone', None)
			country = data.get('country', None)
			city = data.get('city', None)
			bio = data.get('bio', None)
			sex = data.get('sex', None)
			love_state = data.get('love_state', None)
			image = data.get('image', None)
		
			try:
				if name:
					user.name = name
				if username:
					user.username = username
				if email:
					user.email = email
				if phone:
					user.phone = phone
				if password:
					hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
					user.password = hashed_password
				if country:
					user.country = country
				if city:
					user.city = city
				if bio:
					user.bio = bio
				if sex:
					user.sex = sex
				if love_state:
					user.love_state = love_state
				if image:
					user.image = image
				
				user.update()

				return jsonify({
					'success': True,
					'user': user.format()
				}), 200

			except Exception as error:
				print(error)
				return jsonify({
					'success': False,
					'error': str(error)
				}), 200

# GET Relatioships
@api.route('/relationships', methods=['GET'])
def get_relationships():
	try:
		relationships = Relationship.query.all()
		relationships_list = paginate_items(request, relationships)
		
		if len(relationships_list) == 0:
			abort(404)
		
		return jsonify({
			'success': True,
			'total': len(relationships),
			'current': len(relationships_list),
			'relationships': relationships_list
		}), 200
	except Exception as error:
		print(error)
		return jsonify({
			'success': False,
			'error': str(error)
		}), 500

# GET Single Relationship
@api.route('/relationships/<int:relationship_id>', methods=['GET'])
def get_single_relationship(relationship_id):
	relationship = Relationship.query.get_or_404(relationship_id)

	if relationship:
		try:
			data = {
				'id': relationship.id,
				'hubby': relationship.hubby,
				'wifey': relationship.modwifeyel,
				'date_of_creation': relationship.date_of_creation
			}
			return jsonify({
				'success': True,
				'relationship_ data': data,
				'relationship_id': relationship.id
			})
		except Exception as error:
			return jsonify({
				'success': False,
				'error': str(error)
			}), 200

#POST Relationship
@api.route('/relationships', methods=['POST'])
def add_relationships():
	data = request.get_json()

	if data['hubby'] and data['wifey']:
		hubby = data.get('hubby', None)
		wifey = data.get('wifey', None)

		rel_exist = Relationship.query.filter(Relationship.hubby == hubby).filter(Relationship.wifey == wifey)
		rel_status = Relationship.query(Relationship.status)

		if rel_exist is not None:
			if rel_status == 0:
				response = {
					'success': False,
					'error': 'relation already created, wait your partner to accept the request!'
				}
				return jsonify(response), 403
			if rel_status != 0:
				response = {
					'success': False,
					'error': 'relation already exists, do not cheat on your partner!'
				}
				return jsonify(response), 403
		try:
			make = data.get('make', None)
			model = data.get('model', None)
			year = data.get('year', None)
			mileage = data.get('mileage', None)

			new_relationship = Relationship(hubby=hubby, wifey=wifey, date_of_creation=None)
			new_relationship.insert()
			return jsonify({
				'success': True,
				'created': new_relationship.id
			})
		except Exception as error:
			print(error)
			return jsonify({
				'success': False,
				'error': str(error)
			}), 200
	else:
		return jsonify({
			'success': False,
			'error': 'bad request body'
		}), 400

# DELETE Relationship
@api.route('/relationships/<int:relationship_id>', methods=['DELETE'])
def delete_relationships(relationship_id):
	relationship = Relationship.query.get_or_404(relationship_id)

	if relationship:
		try:
			relationship.delete()
			return jsonify({
				'success': True,
				'deleted': relationship.id
			})
		except Exception as error:
			print(error)
			return jsonify({
				'success': False,
				'error': str(error)
			}), 200

# PATCH Relationships
@api.route('/relationships/<int:relationship_id>', methods=['PATCH'])
def update_relationships(relationship_id):
	relationship = Relationship.query.get_or_404(relationship_id)

	if relationship:
		data = request.get_json()
		if not data:
			abort(400)
		if data:
			hubby = data.get('hubby', None)
			wifey = data.get('wifey', None)
			status = data.get('status', None)
		
			try:
				if hubby:
					relationship.hubby = hubby
				if wifey:
					relationship.wifey = wifey
				if status:
					relationship.status = status

				relationship.update()

				return jsonify({
					'success': True,
					'relationship': relationship.format()
				}), 200

			except Exception as error:
				print(error)
				return jsonify({
					'success': False,
					'error': str(error)
				}), 200

# Error Handling
@api.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400

@api.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404

@api.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed'
    }), 405

@api.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unable to process request'
    }), 422

@api.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500
