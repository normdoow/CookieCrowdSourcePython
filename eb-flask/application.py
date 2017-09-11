from flask import Flask, request, session, jsonify
import stripe

app = Flask(__name__)

stripe.api_key = "sk_test_L9QHJxvNGB737iSYHqkNxR5p"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

token = 123#request.form['stripeToken'] # Using Flask


@app.route('/ephemeral_keys', methods = ['POST', 'GET'])
def issue_key():
    api_version = request.args['api_version']
    customerId = request.args['customer_id']
    if customerId == "":
        cutomerId = retrieveCustomerId()

    key = stripe.EphemeralKey.create(customer = "cus_BNMtq7s2Ew0lyw", api_version = api_version)
    return jsonify(key)

@app.route('/charge', methods = ['POST', 'GET'])            #TODO: should be a post eventually
def charge():
    amount = request.args['amount']
    source = request.args['source']
    shipping = request.args['shipping']
    customerId = request.args['customerId']
    if customerId == "":
        cutomerId = retrieveCustomerId()

    charge = stripe.Charge.create(
        amount = amount,
        currency = "usd",
        customer = customerId,
        description = "Testing out the charge",
        source = source,
        shipping = shipping)

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
                                        description="test Customer")
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