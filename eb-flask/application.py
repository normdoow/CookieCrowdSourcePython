from flask import Flask, request, session, jsonify
import stripe
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

stripe.api_key = "sk_test_L9QHJxvNGB737iSYHqkNxR5p"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

token = 123#request.form['stripeToken'] # Using Flask


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
    sendCustomerEmail("cus_BNMtq7s2Ew0lyw")
    sendCookEmail("cus_BNMtq7s2Ew0lyw")
    return "successfully sent email"

@app.route('/charge', methods = ['POST'])
def charge():
    amount = request.form['amount']
    source = request.form['source']
    # shipping = request.form['shipping']
    customerId = request.form['customer_id']
    if customerId == "":
        cutomerId = retrieveCustomerId()
    #shipping is the one that is messed up
    #needs to be the same customer
    # customerId = "cus_BNMtq7s2Ew0lyw"
    charge = stripe.Charge.create(
        amount = amount,
        currency = "usd",
        customer = customerId,
        description = "Testing out the charge",
        source = source)
        # shipping = shipping)

    sendCookEmail(customerId)
    sendCustomerEmail(customerId)
    return "Charge successfully created"


def retrieveCustomerId():
    if 'customerId' in session:
        return session['customerId']
    else:
        customer = stripe.Customer.create(
                                            #source=token,
                                            description="test Customer")
        session['customerId'] = customer.id
        return customer.id

def sendCustomerEmail(customerId):
    customer = stripe.Customer.retrieve(customerId)
    subject = "Thank you for Purchasing Yummy Hot Cookies!"
    message = "Thank you for Purchasing Crowd Cookies!\n\nYou will recieve a dozen warm, choclate chip cookies delivered to you in 20 to 30 minutes. If you have any issues, please contact us at noahbragg@cedarville.edu or call (937)-901-6108.\n\n Please share Crowd Cookie with your friends that live in the area! We are just trying out this cool idea to see if people like it. Have them download the app here:\n\n Have a Great Day!\n\nNoah Bragg\nCrowd Cookie Team"
    sendEmail(customer.email, subject, message)

def sendCookEmail(customerId):
    customer = stripe.Customer.retrieve(customerId)
    to = "noahbragg@cedarville.edu,melissajoybragg@gmail.com"
    subject = "Someone Just Ordered Crowd Cookies!"
    customerName = str(customer.shipping.name)
    customerEmail = str(customer.email)
    customerPhone = str(customer.shipping.phone)
    customerAddress = "      " + str(customer.shipping.address.line1) + " " + str(customer.shipping.address.line2) + "\n      " + str(customer.shipping.address.city) + ", " + str(customer.shipping.address.state) + "  " + str(customer.shipping.address.postal_code)
    message = "Customer Name: " + customerName + "\nCustomer Email: " + customerEmail + "\nCustomer Phone: " + customerPhone + "\nDelivery Address: \n" + customerAddress + "\n\nGet those 12 choclate chip cookies made and shipped over to them in 20 to 30 minutes!\n\nSincerely,\nCrowd Cookie Bot"
    sendEmail(to, subject, message)

def sendEmail(to, subject, message):
    msg = MIMEText(message)

    sender = "noahbragg@cedarville.edu"

    EMAIL_HOST_USER = "AKIAIME6LLTOUKFDG2IA"
    EMAIL_HOST_PASSWORD = "AqU75pwvORi2GnG2THYNq5KBbDKMiTCnrI3plq+YRCkw"

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
    customer = stripe.Customer.create(
                                        #source=token,
                                        description="test Customer2")
    return customer.id

@app.route('/is_cook_available', methods = ['GET'])
def isCookAvailable():
    return "True"             #this just returns true of false for if the cook is available to sell cookies


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run(host='0.0.0.0')