from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question

satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])


app = Flask(__name__)
app.config['SECRET_KEY'] = "201-989-215"

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def render_homepage():
   return render_template('index.html', survey=satisfaction_survey)

@app.route('/questions/<value>')
def render_question_page(value):
   #determine if someone is putting a string in the URL
   try:
       number = int(value)
   except:
       number = value  #yep... they are

   if  number != len(responses):
      flash("You are attempting to answer an invalid question.")

   if len(responses) >= len(satisfaction_survey.questions):
      return render_template('thank_you.html', responses=responses) 
   return render_template('questions.html',question_num=len(responses), survey=satisfaction_survey)
 

@app.route('/answer', methods=["POST"])
def handle_answer():
    #grab the data we're sending from the question
    question_num = int(request.form['question_num'])
    choice = request.form['choice']
    
    #add the user's choice to responses
    responses.append(choice)

    #make sure we're not going to run off the end of the list of questions
    next_question = question_num + 1
    num_questions = len(satisfaction_survey.questions)

    if num_questions == next_question:
        return render_template('thank_you.html', responses=responses)
    else:
        return redirect(f"/questions/{next_question}")

@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    return response

if __name__ == '__main__':
    app.run()

