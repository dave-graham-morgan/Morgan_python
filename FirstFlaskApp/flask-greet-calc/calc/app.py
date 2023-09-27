from flask import Flask, request

app = Flask(__name__)

@app.route('/add')
def add_them():
   a = int(request.args.get("a"))
   b = int(request.args.get("b"))
   return str(a+b)

@app.route('/sub')
def sub_them():
   a = int(request.args.get("a"))
   b = int(request.args.get("b"))
   return str(a-b)

@app.route('/multi')
def multiply_them():
   a = int(request.args.get("a"))
   b = int(request.args.get("b"))
   return str(a*b)

@app.route('/divide')
def devide_them():
   a = int(request.args.get("a"))
   b = int(request.args.get("b"))
   return str(a/b)