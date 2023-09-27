from flask import Flask, request, render_template
from stories import Story


app = Flask(__name__)

story_objects = {
   'dragons' : Story(["place", "noun", "verb", "adjective", "plural_noun"],
   """Once upon a time in a long-ago {place}, there lived a
   large {adjective} {noun}. It loved to {verb} {plural_noun}."""),

   'new_automobile' : Story(["place", "automobile", "verb", "noun", "plural_noun"],
    """My car was a complete wreck, so I went to {place} looking to buy a new {automobile}.
      I didn't have a {noun}. So I {verb} with {plural_noun}.""")
}

#my_story = None

@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    return response

@app.route('/')
def render_home():
   return render_template("index.html")

@app.route('/gather_input')
def render_gather_input_form():
   story_title = request.args.get('selection') #grab the story title from the URL

   global my_story #this needs to be global so other functions can use it
   my_story = story_objects.get(story_title) #get the Story object from the story_objects dict
   return render_template("gather_input.html", prompts=my_story.prompts) 

@app.route('/show_story')
def show_story():
   print(f"this is my_story*********: {my_story}")
   answers = {}
   for (key,value) in request.args.items():
        answers[key] = value
   return render_template("show_story.html", final_story=my_story.generate(answers))

if __name__ == '__main__':
    app.run()