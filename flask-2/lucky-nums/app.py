from flask import Flask, render_template, request, jsonify
import requests, random


app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route("/api/get-lucky-num", methods=["POST"])
def get_lucky_num():
    data = request.json
    name = data.get('name')
    
    print(f"name: {name}")
    email = data.get('email')
    year = data.get('year')
    color = data.get('color')

    errors = {}
    if not name:  
        errors["name"] = ["Name is required"]
    if not email:
        errors["email"] = ["Email is required"]
    if not year:
        errors["year"] = ["Year is required"]
    if not color:
        errors["color"] = ["Color is required"]
    if errors:
        return jsonify(errors = errors)
    else:
        num = random.randrange(0,100) 
        number_fact = requests.get('http://numbersapi.com/random').text
        year_fact = requests.get(f'http://numbersapi.com/{year}').text

        data={
            "num":{
                "fact":number_fact,
                "num":num
            },
            "year":{
                "fact":year_fact,
                "year":year
            }
        }
        return jsonify(data)
 
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8080, debug=True)
