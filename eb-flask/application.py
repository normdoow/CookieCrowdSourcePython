from flask import Flask, request, session, jsonify
import stripe

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
    customer = stripe.Customer.retrieve("cus_BNMtq7s2Ew0lyw")
    msg = MIMEText("This is a test email from Noah")

    me = "noahbragg@cedarville.edu"
    you = customer.email

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Test Subject'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    return customer.email

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