from flask import Blueprint, request

database_api = Blueprint('database_api', __name__)


@database_api.route('/change_baker_availability', methods = ['GET'])
def changeBakerAvailability():
	isAvailable = request.args.get('is_available') == "Yes"
	#TODO: update the database
	return "successfully updated database"


@database_api.route('/login_baker', methods = ['GET'])
def loginBaker():
	email = request.args.get('email')
	pw = request.args.get('pw')
	return "success"

@database_api.route('/cook_available', methods = ['GET'])
def cookAvailable():
	latitude = request.args.get('lat')
	longitude = request.args.get('long')
	return "success"