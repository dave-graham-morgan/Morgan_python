from flask import Flask,render_template, session, request, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

#set up Flask and debug toolbar
app = Flask(__name__)
app.config['SECRET_KEY'] = "201-989-215-4145-4433"

#debug = DebugToolbarExtension(app)

#initialize the gameboard
boggle_game = Boggle()
board = boggle_game.make_board()


@app.route('/')
def render_game_board():
   session['game_board'] = board
   session['user_guesses'] = []
   return render_template('index.html', board=session['game_board'])

@app.route('/handle-response')
def check_user_response():
    curr_guess = request.args.get('guess')
    if curr_guess in session.get('user_guesses'):
        return jsonify('previous')
    
    #add the current guess to the list of guesses and store in the session
    all_guesses = session.get('user_guesses')
    all_guesses.append(curr_guess)
    session['user_guesses'] = all_guesses

    #check to see if the current guess is valid
    is_it_valid = boggle_game.check_valid_word(session['game_board'], curr_guess)
    return jsonify(is_it_valid) 

@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    return response

if __name__ == '__main__':
    app.run()