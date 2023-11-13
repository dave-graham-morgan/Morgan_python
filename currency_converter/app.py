from flask import Flask, render_template, request, session, jsonify, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import requests

API_KEY = "678793a7eb9438195c6a9d80d8a921d8"
base_url = "http://api.exchangerate.host/"

#set up Flask and secret key for encoding the session
app = Flask(__name__)
app.config['SECRET_KEY'] = "8675-d309-jfkfis-ffidks"

#enable debugToolbar 
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def render_homepage():
    #use the session data if we have it.  Otherwise initialize it.
    try:
        form_data = session['form_data']
    except:
        session['form_data'] = {
			'currency-from': '', 
			'currency-to': '', 
			'amount': ''
		}
        form_data = session['form_data']
       
    return render_template('index.html', data=session['form_data'])
   

@app.route('/convert', methods = ['POST'])
def calculate_conversion():
    #get data from the form and save it to the session
    form_data = request.form
    session['form_data'] = form_data

    #make sure the data entered is valid
    is_valid = validate_form(form_data)

    #if the data is good, move the user to results
    if is_valid:
        return render_template('/results.html', data=do_calculation()) 
    #if any of the data are bad, reload the form page. 
    else:
       return redirect('/')

@app.route('/cleanup')
def cleanup():
    session.clear()
    return redirect('/')

def do_calculation():
    form_data = session['form_data']
    currency_from = form_data.get('currency-from')
    currency_to = form_data.get('currency-to')
    amount = form_data.get('amount')

    URL = base_url + 'convert?'
    PARAMS = {'from':currency_from,
              'to': currency_to,
              'amount': amount,
              'access_key': API_KEY}
    res = requests.get(url = URL, params = PARAMS).json()
    try:
        #convert the result into a two decimal float... safely
        result = round(float(res.get('result')),2)
    except:
        print("something went wrong, not possible to convert response to int")

    return {'from': res.get('query').get('from'),
            'to': res.get('query').get('to'),
            'amount': res.get('query').get('amount'),
            'result': result
            }
    
def validate_form(form_data):
    currency_from = request.form['currency-from'].upper()
    currency_to = request.form['currency-to'].upper()
    amount = request.form['amount']

    if amount == '' or currency_from == '' or currency_to == '':
       flash('all fields are required', 'error')
       return False
    try:
       qty = int(amount)
    except:
       flash('amount must be an integer')
       return False
   
    valid_currencies = get_valid_currencies()

    if currency_from not in valid_currencies:
       flash(f'{currency_from} is not a valid currency! Try again')
       return False
    if currency_to not in valid_currencies:
      flash(f'{currency_to} is not a valid currency! Try again')
      return False
    return True


def get_valid_currencies():
    URL = base_url + 'list?'
    PARAMS = {'access_key':API_KEY}
    res = requests.get(url = URL, params = PARAMS).json()
    return res.get('currencies')

if __name__ == '__main__':
    app.run(port=8080)