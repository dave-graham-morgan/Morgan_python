from unittest import TestCase
from flask import session
from app import app, validate_form, get_valid_currencies

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# Disable Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        # with self.client.session_transaction() as change_session:
        #         change_session['game_board'] = [['P', 'Y', 'S', 'T'], ['E', 'V', 'O', 'G'], ['S', 'T', 'I', 'A'], ['Z', 'O', 'I', 'R']]
        #         change_session['user_guesses'] = ['jit', 'wit', 'kole']
    
    def test_render_homepage(self):
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)
            test_string = '<label for="currency-from" class="form-label">Converting From:</label>'

            #verify we're getting a good response and that the correct page is being rendered
            self.assertEqual(res.status_code, 200)
            self.assertIn(test_string, html)
            #test that Jinja is working:
            self.assertIn('<title>Currency Converter</title>', html)
    
    def test_session_data(self):
        with self.client:
            res = self.client.get('/')
            with self.client.session_transaction() as session:
                
                #assert the route is setting session data appropriately.
                self.assertIn('currency-from', session.get('form_data'))
                self.assertIn('currency-to', session.get('form_data'))
                self.assertIn('amount', session.get('form_data'))
    
    def test_convertpage(self):
        with self.client:
            form_data = {
                'currency-from': 'USD', 
                'currency-to': 'CHF', 
                'amount': '1000'
                }
            res = self.client.post('/convert', data=form_data)
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('USD', html)
            self.assertIn('CHF', html)
            self.assertIn('1000', html)


    def test_validate_form(self):
        form_data = {
                'currency-from': 'USD', 
                'currency-to': 'CHF', 
                'amount': '1000'
                }
        #set up a dummy request context so we can test
        with app.test_request_context('/dummy', data=form_data):
            res = validate_form(form_data)
            self.assertTrue(res)

    def test_validate_form_errors(self):
        #check we fail on bad amounts (non-integer)
        form_data = {
                'currency-from': 'USD', 
                'currency-to': 'CHF', 
                'amount': 'a'
                }
        with app.test_request_context('/dummy', data=form_data):
            res = validate_form(form_data)
            self.assertFalse(res)

        #check we fail on bad currency-from
        form_data['amount'] = '1000'
        form_data['currency-from'] = 'XXX'
        with app.test_request_context('/dummy', data=form_data):
            res = validate_form(form_data)
            self.assertFalse(res)

        #check we fail on bad currency-to
        form_data['currency-from'] = 'USD'
        form_data['currency-to'] = 'XXX' 
        with app.test_request_context('/dummy', data=form_data):
            res = validate_form(form_data)
            self.assertFalse(res)

    def test_get_valid_currencies(self):
        res = get_valid_currencies()
        self.assertIn('USD', res)
        self.assertIn('AUD', res)
        self.assertIn('SEK', res)

        self.assertNotIn('XXX', res)
