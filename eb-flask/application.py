from flask import Flask, request, session, jsonify
# import boto3
import stripe
import smtplib
from email.mime.text import MIMEText
from pusher import Pusher
from validate_email import validate_email

app = Flask(__name__)

stripe.api_key = "sk_test_L9QHJxvNGB737iSYHqkNxR5p"
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
    # sendCustomerEmail("cus_BNMtq7s2Ew0lyw")
    # sendCookEmail("cus_BNMtq7s2Ew0lyw")
    return "successfully sent email"

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
    sendCookEmail(customerId, email, amount == "0")
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
    message = "Thank you for Purchasing Crowd Cookies!\n\nYou will receive a dozen warm, chocolate chip cookies delivered to you in 30 minutes. If you have any issues, please contact us at noahbragg@cedarville.edu or call (937)-901-6108.\n\n Please share Crowd Cookie with your friends that live in the area! We are just trying out this cool idea to see if people like it. Have them download the app here:\n\n Have a Great Day!\n\nNoah Bragg\nCrowd Cookie Team"
    if validate_email(email, verify=True):      #this is to check to make sure it is a valid email before trying to send to it
        sendEmail(email, subject, message)
        

def sendCookEmail(customerId, customerEmail, isFree):
    customer = stripe.Customer.retrieve(customerId)
    to = "noahbragg@cedarville.edu,melissajoybragg@gmail.com"
    subject = "Someone Just Ordered Crowd Cookies!"
    customerName = str(customer.shipping.name)
    # customerEmail = str(customer.email)
    customerPhone = str(customer.shipping.phone)
    customerAddress = "      " + str(customer.shipping.address.line1) + " " + str(customer.shipping.address.line2) + "\n      " + str(customer.shipping.address.city) + ", " + str(customer.shipping.address.state) + "  " + str(customer.shipping.address.postal_code)
    freeText = ""
    if isFree:
        freeText = "This is a Free Order!! They got a good deal!\n\n"

    message = freeText + "Customer Name: " + customerName + "\nCustomer Email: " + customerEmail + "\nCustomer Phone: " + customerPhone + "\nDelivery Address: \n" + customerAddress + "\n\nGet those 12 chocolate chip cookies made and shipped over to them in 30 minutes!\n\nSincerely,\nCrowd Cookie Bot"
    sendEmail(to, subject, message)

def sendEmail(to, subject, message):
    msg = MIMEText(message)

    sender = "noahbragg@cedarville.edu"

    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    
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
    return "True"
    # sqs = boto3.resource('sqs')
    # queue = sqs.get_queue_by_name(QueueName='data')
    # return queue.attributes.get('is_cook_available')
    # return "True"        #this just returns true of false for if the cook is available to sell cookie

@app.route('/set_cook', methods = ['GET'])
def setIsCookAvailable():
    param = request.args.get('val')
    # queue = sqs.create_queue(QueueName='data', Attributes={'is_cook_available': 'True'})
    # sqs = boto3.resource('sqs')
    # queue = sqs.get_queue_by_name(QueueName='data')

    # if param == "True":
    #     response = queue.set_attributes(Attributes={'is_cook_available': 'True'})
    # else:
    #     response = queue.set_attributes(Attributes={'is_cook_available': 'False'})
    return "successfully updated cooks availability"

@app.route('/notify_users', methods = ['GET'])
def notifyUsers():
    pusher = Pusher(app_id=u'', key=u'', secret=u'', cluster=u'')

    pusher.notify(['cook_available'], {
      'gcm': {
        'notification': {
          'title': 'Cooks are now available in your area. You can order Cookies!',
          'icon': 'androidlogo'
        }
      }
    })
    return "Successfully pushed notification"

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    # app.run(threaded=True)
    app.run(host='0.0.0.0')