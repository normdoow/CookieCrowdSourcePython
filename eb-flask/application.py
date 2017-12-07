from flask import Flask, request, session, jsonify
import stripe
import smtplib
from email.mime.text import MIMEText
# from database import database_api
from flask_sqlalchemy import SQLAlchemy
from math import radians, cos, sin, asin, sqrt
# from pusher import Pusher
# from validate_email import validate_email
# from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
# app.register_blueprint(database_api)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Baker(db.Model):

    __tablename__ = "bakers"

    id = db.Column(db.Integer, primary_key=True)
    bakerEmail = db.Column(db.String(32))
    pw = db.Column(db.String(32))
    lon = db.Column(db.String(32))
    lat = db.Column(db.String(32))
    isAvailable = db.Column(db.Boolean(False))

stripe.api_key = 
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/ephemeral_keys', methods = ['POST'])
def issue_key():
    apiVersion = request.form['api_version']
    customerId = request.form['customer_id']
    if customerId == "":
        cutomerId = retrieveCustomerId()
                                                #TODO: this customerID needs to be changes
    key = stripe.EphemeralKey.create(customer = customerId, api_version = apiVersion)
    return jsonify(key)

@app.route('/email', methods = ['GET'])
def email():
    # sendCustomerEmail("cus_BNMtq7s2Ew0lyw", "blah@gmail.com")
    # sendCookEmail("cus_BjreuxjdxTnqNs", "blah@gmail.com", True)
    to = ["noahbragg@cedarville.edu", "melissajoybragg@gmail.com", "isaiahbragg2020@gmail.com"]
    sendEmail(to, "test message", "This is a test email to see if I can send it to multiple recipients.")
    return "successfully sent email"

@app.route('/send_new_baker_email', methods = ['GET'])
def sendNewBakerEmail():
    email = request.args.get('email')
    to = ["noahbragg@cedarville.edu"]
    sendEmail(to, "New Baker Interested!", "Hello Noah,\n\nThere is a new baker with email " + email + " who is interested in becoming a baker. Go ahead and give them some info and see if they would be a good fit to join the Crowd Cookie team!!!\n\nSincerely,\nCrowd Cookie Bot")
    return "success sending email"

@app.route('/send_rating_email', methods = ['GET'])
def sendRatingEmail():
    rating = request.args.get('rating')
    comments = request.args.get('comments')
    isWarm = request.args.get('isWarm')
    isRecommend = request.args.get('isRecommend')
    to = ["noahbragg@cedarville.edu"]
    sendEmail(to, "Crowd Cookie Rating", "Hello Noah,\n\nRating: " + rating + "\n\nWere the cookies warm? " + isWarm + "\n\nWould you recommend Crowd Cookie to a friend? " + isRecommend + "\n\nComments: " + comments + "\n\nHope it was a good review!\n\nSincerely,\nCrowd Cookie Bot")
    return "success sending email"


@app.route('/charge', methods = ['POST'])
def charge():
    amount = request.form['amount']
    source = request.form['source']
    customerId = request.form['customer_id']
    email = request.form['email']

    if customerId == "":
        cutomerId = retrieveCustomerId()

    if amount != "0":
        charge = stripe.Charge.create(
            amount = amount,
            currency = "usd",
            customer = customerId,
            description = "Testing out the charge",
            source = source)
            # shipping = shipping)

    # updateCustomerEmail(customerId, email)        #this didn't seem to do anything
    sendCookEmail(customerId, email, amount == "600")
    sendCustomerEmail(customerId, email)
    return "Charge successfully created"

@app.route('/charge_v2', methods = ['POST'])
def chargev2():
    amount = request.form['amount']
    source = request.form['source']
    customerId = request.form['customer_id']
    email = request.form['email']
    bakerEmail = request.form['baker_email']

    if customerId == "":
        cutomerId = retrieveCustomerId()

    if amount != "0":
        charge = stripe.Charge.create(
            amount = amount,
            currency = "usd",
            customer = customerId,
            description = "Testing out the charge",
            source = source)
            # shipping = shipping)

    # updateCustomerEmail(customerId, email)        #this didn't seem to do anything
    sendCookEmailV2(customerId, bakerEmail, email, amount == "600")
    sendCustomerEmail(customerId, email)
    return "Charge successfully created"


@app.route('/update_customer_address', methods = ['POST'])          #only used on Android right now
def updateCustomerAddress():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    city = request.form['city']
    state = request.form['state']
    customerId = request.form['customer_id']
    line1 = request.form['line_1']
    line2 = request.form['line_2']
    postalCode = request.form['postal_code']

    ship = {}
    ship['name'] = name
    ship['phone'] = phone
    address = {}
    address['city'] = city
    address['state'] = state
    address['line1'] = line1
    address['line2'] = line2
    address['postal_code'] = postalCode
    ship['address'] = address

    customer = stripe.Customer.retrieve(customerId)
    customer.email = email
    customer.shipping = ship
    customer.save()
    return "successful update"


def updateCustomerEmail(customerId, email):
    customer = stripe.Customer.retrieve(customerId)
    customer.email = email
    customer.save()

def retrieveCustomerId():
    if 'customerId' in session:
        return session['customerId']
    else:
        customer = stripe.Customer.create(description="test Customer")
        session['customerId'] = customer.id
        return customer.id

def sendCustomerEmail(customerId, email):       #pass in the customer email becasue the shipping one is empty
    customer = stripe.Customer.retrieve(customerId)
    subject = "Thank you for Purchasing Yummy Hot Cookies!"
    message = "Thank you for Purchasing Crowd Cookies!\n\nYou will receive a dozen warm, chocolate chip cookies delivered to you in around 40 minutes. If you have any issues, please contact us at noah@crowd-cookie.com or call (937)-901-6108.\n\nPlease share Crowd Cookie with your friends that live in the area! We are just trying out this cool idea to see if people like it. You can find the iOS app or Android app to share with them here: https://itunes.apple.com/us/app/crowd-cookie/id1301846845?mt=8 \n\nhttps://play.google.com/store/apps/details?id=shinzzerz.cookiecrowdsource\n\n Have a Great Day!\n\nNoah Bragg\nCrowd Cookie Team"
    # if validate_email(email, verify=True):      #this is to check to make sure it is a valid email before trying to send to it
    # try:
    #     v = validate_email(email) # validate and get info
    to = []
    to.append(email)
    sendEmail(to, subject, message)
    # except EmailNotValidError as e:
    #print("email wasn't valid")
        # email is not valid, exception message is human-readable


def sendCookEmail(customerId, customerEmail, isFree):
    customer = stripe.Customer.retrieve(customerId)

    to = ["noahbragg@cedarville.edu", "melissajoybragg@gmail.com", "isaiahbragg2020@gmail.com"]
    subject = "Someone Just Ordered Crowd Cookies!"
    customerName = str(customer.shipping.name)
    # customerEmail = str(customer.email)
    customerPhone = str(customer.shipping.phone)
    customerAddress = "      " + str(customer.shipping.address.line1) + " " + str(customer.shipping.address.line2) + "\n      " + str(customer.shipping.address.city) + ", " + str(customer.shipping.address.state) + "  " + str(customer.shipping.address.postal_code)
    freeText = ""
    if isFree:
        freeText = "This is a $6 Order!! They got a good deal!\n\n"

    message = freeText + "Customer Name: " + customerName + "\nCustomer Email: " + customerEmail + "\nCustomer Phone: " + customerPhone + "\nDelivery Address: \n" + customerAddress + "\n\nGet those 12 chocolate chip cookies made and shipped over to them in 40 minutes!\n\nSincerely,\nCrowd Cookie Bot"
    sendEmail(to, subject, message)

def sendCookEmailV2(customerId, bakerEmail, customerEmail, isFree):
    customer = stripe.Customer.retrieve(customerId)

    to = ["noahbragg@cedarville.edu", "melissajoybragg@gmail.com", "isaiahbragg2020@gmail.com", bakerEmail]
    subject = "Someone Just Ordered Crowd Cookies!"
    customerName = str(customer.shipping.name)
    # customerEmail = str(customer.email)
    customerPhone = str(customer.shipping.phone)
    customerAddress = "      " + str(customer.shipping.address.line1) + " " + str(customer.shipping.address.line2) + "\n      " + str(customer.shipping.address.city) + ", " + str(customer.shipping.address.state) + "  " + str(customer.shipping.address.postal_code)
    freeText = ""
    if isFree:
        freeText = "This is a $6 Order!! They got a good deal!\n\n"

    message = freeText + "Baker fulfilling order: " + bakerEmail + "\n\n" + "Customer Name: " + customerName + "\nCustomer Email: " + customerEmail + "\nCustomer Phone: " + customerPhone + "\nDelivery Address: \n" + customerAddress + "\n\nGet those 12 chocolate chip cookies made and shipped over to them in 40 minutes!\n\nSincerely,\nCrowd Cookie Bot"
    sendEmail(to, subject, message)

def sendEmail(to, subject, message):
    msg = MIMEText(message)

    sender = "noah@crowd-cookie.com"

    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join( to )

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(sender, to, msg.as_string())
    s.quit()

@app.route('/create_customer', methods = ['GET'])
def createCustomer():
    customer = stripe.Customer.create(description="test Customer2")
    return customer.id

@app.route('/is_cook_available', methods = ['GET'])
def isCookAvailable():
    return "False"

@app.route('/is_isaiah_available', methods = ['GET'])
def isIsaiahAvailable():
    return "False"

@app.route('/set_cook', methods = ['GET'])
def setIsCookAvailable():
    param = request.args.get('val')
    return "successfully updated cooks availability"

@app.route('/notify_users', methods = ['GET'])
def notifyUsers():
    pusher = Pusher(app_id=u'', key=u'd05669f4df7a1f96f929', secret=u'', cluster=u'us2')

    pusher.notify(['cook_available'], {
      'gcm': {
        'notification': {
          'title': 'Cookies are now available!',
          'icon': 'androidlogo'
        }
      }
    })
    return "Successfully pushed notification"


# database stuff
@app.route('/change_baker_availability', methods = ['GET'])
def changeBakerAvailability():
    bakerEmail = request.args.get('baker_email')
    isAvailable = request.args.get('is_available') == "Yes"

    baker = Baker.query.filter_by(bakerEmail=bakerEmail).first()
    baker.isAvailable = isAvailable
    db.session.commit()

    return "success"


@app.route('/login_baker', methods = ['GET'])
def loginBaker():
    email = request.args.get('email')
    pw = request.args.get('pw')
    bakers = Baker.query.all()
    isMatch = False
    for baker in bakers:
        if email == baker.bakerEmail and pw == baker.pw:
            isMatch = True

    if isMatch:
        return "success"
    return "failure"

@app.route('/cook_available', methods = ['GET'])
def cookAvailable():
    userLat = float(str(request.args.get('lat')))
    userLong = float(str(request.args.get('long')))
    # latitude = 39.670499      #is inside noah location
    # longitude = -84.145547
    # latitude = 39.621895      #is right outside noah location
    # longitude = -84.128147

    bakers = Baker.query.all()
    test_points = [{'lat': 39.691483 , 'lng': -84.101717, 'email': "noahbragg@cedarville.edu"}, {'lat': 39.673647, 'lng': -83.977037, 'email': "isaiahbragg@gmail.com"}]    #no and is locations

    radius = 3.5
    minDist = 50000
    bakerEmail = ""
    isCooksAvailable = False
    isRightLocation = False

    for baker in bakers:
        dist = haversine(userLong, userLat, float(baker.lon), float(baker.lat))
        if baker.isAvailable:
            minDist = min(dist, minDist)
            if minDist == dist:
                bakerEmail = baker.bakerEmail

        if dist <= radius:
            isRightLocation = True
            if baker.isAvailable:
                isCooksAvailable = True


    if minDist <= radius and bakerEmail != "":
        return bakerEmail

    # no cooks and wrong location
    if not isCooksAvailable and not isRightLocation:
        return "There are no cooks that are making cookies currently. Try again in the evening from 5pm to 9pm. There is more chance that we will be making cookies then! You also must be in a location that is in a 5 mile radius around the Greene to be able to order cookies. Thank you for your patience while we are getting this new business idea up and running!"

    # wrong location
    if not isRightLocation:
        return "You must be in a location that is in a 5 mile radius from the Greene for you to be able to order cookies. We will hopefully be coming to a location closer to you soon! Thank you for your patience while we are getting this new business idea up and running!"

    # no cooks
    return "There are no cooks that are making cookies currently. Try again in the evening from 5pm to 9pm. There is more chance that we will be making cookies then! Thank you for your patience while we are getting this new business idea up and running!"

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


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run(threaded=True)
    # app.run(host='0.0.0.0')