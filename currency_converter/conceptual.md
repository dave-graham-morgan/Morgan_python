### Conceptual Exercise

Answer the following questions below:

- What are important differences between Python and JavaScript?
  * Syntax is different
  * javascript is primarily used to provide front end functionality (although I understand)  
  that Node.js now enables backend support. 
  * javascript runs natively in browsers whereas you need to do something fancy to get Python to do that. 
  * javascript debbugger is within the browser
  * javascript is 'managed' by a committee and they publish how the language should evolve  
    but its up to each browser to support the new features whereas Python features come out with a release
  * both are dynamically typed but Python is a little more strict than Javascript.

- Given a dictionary like ``{"a": 1, "b": 2}``: , list two ways you
  can try to get a missing key (like "c") *without* your programming
  crashing.
  * myDict.get('c') wont crash the program but it will return None which just needs to be handled
  * you could put the attempt to access 'c' behind a try except block

- What is a unit test?
  * a unit test is a test designed to validate a single function.

- What is an integration test?
  * integration tests will test how components work together,  
  so you're testing the interaction between functions/classes etc.

- What is the role of web application framework, like Flask?
  * to **greatly** improve the lives of developers.  It magically handles  
  a lot of the heavy lifting that would otherwise be manual and repetitive in  
  building web applications. Like building http requests and sending headers and omg. 

- You can pass information to Flask either as a parameter in a route URL
  (like '/foods/pretzel') or using a URL query param (like
  'foods?type=pretzel'). How might you choose which one is a better fit
  for an application?
  * not sure, both should work.  There is an upper URL size limit which when using query  
  parameters could more easily be met.  I think query parameters are a little more flexible  
  which I think would make them easier to scale/expand if your application needs it.  I think  
  route URLs might be easier to read for humans.  Route URLs might be better if your data element  
  is required.  For example if not having /foods/pretzel will break the app then use route URL.  
  the converse of that is you can easily use a default with a query param. 

- How do you collect data from a URL placeholder parameter using Flask?
  * you first decalre it in your route decorator like <stuff>, then in the method you  
  pass in that variable spelled exactly the same way like def do_some(stuff):, then you  
  will have access to that variable in your function. 

- How do you collect data from the query string using Flask?
  * you have to first import 'request' from flask, then you can use request.args.get('your_key')  
  which will return the value of 'your_key' if it exists   

- How do you collect data from the body of the request using Flask?
  * you can still use 'request' but instead of args use the keyword form. so: request.form.get('your_key')

- What is a cookie and what kinds of things are they commonly used for?
  * a cookie is a small bit of text that is stored locally.  The cookies are returned automaticlaly  
  to the server by the browser as part of the html header.  They are used to persist information  
  since the browser is stateless.  They can be used to show that a user is logged in, for example or has  
  selected certain preferences in the app, or to collect information about a user etc. 

- What is the session object in Flask?
  * it is an easy way to securely persist data across sessions in cookies.  
  The cookies are encrypted and they have a checksum so that the system will know if they have been tampered with. 

- What does Flask's `jsonify()` do?
  * it kinda does what it says it does.  It takes a bit of data and puts it in json safe format. which is key  
  value pairs that are all strings.  It ends up looking similar to a python dict but where everything is a  
  string.  
