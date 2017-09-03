from flask import Flask, request
import stripe

app = Flask(__name__)

stripe.api_key = "sk_test_L9QHJxvNGB737iSYHqkNxR5p"

# token = request.form['stripeToken'] # Using Flask


@app.route('/ephemeral_keys', methods = ['GET'])
def issue_key():
    api_version = request.args['api_version']
    customerId = 12345 #session['customerId']
    key = stripe.EphemeralKey.create(customer = customerId, api_version = "2017-05-25")
    return jsonify(key)

@app.route('/charge', methods = ['POST'])
def charge():
    amount = request.args['amount']
    source = request.args['source']
    shipping = request.args['shipping']

    charge = stripe.Charge.create(
        amount = amount,
        currency = "usd",
        customer = '12345',
        description = "Testing out the charge",
        source = 123,
        shipping = shipping)

    return "Charge successfully created"

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()