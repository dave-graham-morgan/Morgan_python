from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# Disable Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    def setUp(self):
        """create session data"""
        self.client = app.test_client()
        with self.client.session_transaction() as change_session:
                change_session['game_board'] = [['P', 'Y', 'S', 'T'], ['E', 'V', 'O', 'G'], ['S', 'T', 'I', 'A'], ['Z', 'O', 'I', 'R']]
                change_session['user_guesses'] = ['jit', 'wit', 'kole']

    def test_render_game_board(self):
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-1">BOGGLE</h1>', html)
            self.assertEqual(len(session['game_board']), 4)
            self.assertEqual(len(session['game_board'][0]), 4)
            self.assertEqual(len(session['game_board'][1]), 4)
            self.assertEqual(len(session['game_board'][2]), 4)
            self.assertEqual(len(session['game_board'][3]), 4)
    
    def test_check_not_on_board(self):
        with self.client:
            res = self.client.get('/handle-response?guess=road')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), '"not-on-board"\n')

    def test_check_not_word(self):        
        with self.client:
            res = self.client.get('/handle-response?guess=faladaba')
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), '"not-word"\n')

    def test_check_ok(self):        
        with self.client:
            res = self.client.get('/handle-response?guess=sot')
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), '"ok"\n')
    
    def test_check_previous(self):        
        with self.client:
            res = self.client.get('/handle-response?guess=wit')
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), '"previous"\n')

    


        