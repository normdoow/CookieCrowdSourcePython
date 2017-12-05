from flask import Blueprint, request
from math import radians, cos, sin, asin, sqrt

database_api = Blueprint('database_api', __name__)


@database_api.route('/change_baker_availability', methods = ['GET'])
def changeBakerAvailability():
	bakerEmail = request.args.get('baker_email')
	isAvailable = request.args.get('is_available') == "Yes"
	#TODO: update the database
	return "successfully updated database"


@database_api.route('/login_baker', methods = ['GET'])
def loginBaker():
	email = request.args.get('email')
	pw = request.args.get('pw')
	#TODO: check the pw and email with the database to see if they match return if they do or not
	return "success"

@database_api.route('/cook_available', methods = ['GET'])
def cookAvailable():
	userLat = float(request.args.get('lat'))
	userLong = float(request.args.get('long'))
	# latitude = 39.670499		#is inside noah location
	# longitude = -84.145547
	# latitude = 39.621895		#is right outside noah location
	# longitude = -84.128147
	
	#TODO: grab this data from the database
	test_points = [{'lat': 39.691483 , 'lng': -84.101717, 'email': "noahbragg@cedarville.edu"}, {'lat': 39.673647, 'lng': -83.977037, 'email': "isaiahbragg@gmail.com"}]	#no and is locaitons
	#TODO: check to see that the baker is available currently as well

	radius = 3.5
	minDist = 50000
	bakerEmail = ""
	#go through the baker locations and get the closest one
	for point in test_points:
		dist = haversine(userLong, userLat, point['lng'], point['lat'])
	
		minDist = min(dist, minDist)
		if minDist == dist:
			bakerEmail = point['email']

	if minDist <= radius: 
		return "inside region, email: " + bakerEmail
	return "outside region"
	#either return a baker email because cookies are available or return the string why they are not available


"""
Calculate the great circle distance between two points 
on the earth (specified in decimal degrees)
"""
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles
    return c * r

