### Conceptual Exercise

Answer the following questions below:

- What is RESTful routing? Restful resposes are those that follow the restful pattern for CRUD, i'm sure there's more to RESTful but that's the main takeaway for me.  The pattern is 
GET  /stuff #returns all stuff resources from the db (safe, idempotent)
GET /stuff/<id> #returns details about one stuff resource (safe, idempotent)
POST /stuff #creates a new stuff resource (not safe, not idempotent)
PUT /stuff/<id> #updates an entire stuff resource (not safe, idempotent)
PATCH /stuff/<id> #updates an part of a stuff resource (not safe, usually idempotent but I read it doesn't have to be but cannot envision a use case where it is not)
DELETE /stuff/<id> #removes a particular resource from the db  (not safe, idempotent)

- What is a resource? broad question, to me a resource is everything you need to build the website, Database, data in the database, forms, routes etc.

- When building a JSON API why do you not include routes to render a form that when submitted creates a new user? well I wouldn't use JSON to build a form but instead use it to transfer data in a standardized way from the client to the server.  maybe I'm miss interpreting the question. 

- What does idempotent mean? Which HTTP verbs are idempotent? idempotent means you can make the request repedetedly and the server will always be in the same state.  For example a GET request is idempotent... you can make the same request 100x times and nothing will be different on the server. See above for which verbs are idempotent

- What is the difference between PUT and PATCH?  PUT is typically used as a full update to a resource whereas a PATCH updates only part of the resource.  both PUT and PATCH are not safe but are idempotent. 

- What is one way encryption? One way encryption means you can't get back to the encrypted word.  The system takes an input, usually a password or something equally secret, and encrypts it using a random salt.  The resulting string cannot be decrypted back to the original string, at least not without a lot of processing and time. 

- What is the purpose of a `salt` when hashing a password? it is to increase randomness of the encrypted string.  It is used so that systems cannot reverse engineer say common passwords for example.  Without salt the password "letmein" would appear as the same encrypted string dozens of times in a user database because people are stupid. It would allow hackers the ability to brute force these common passwords and eventually compromise dozens of idiot's accounts. With a salt, identical passwords that are encrypted would no longer appear identical. 

- What is the purpose of the Bcrypt module? Bcrypt offers an easy way to encrypt strings (e.g. passwords) with a random salt that is repeatable so the user can enter the same password and get the same encrypted string so you can say "yep, you know the password" but then also say "I don't know the password".  Also its slow, takes a couple seconds at the default setting to encrypt which is a good thing because it makes brute force more difficult. 

- What is the difference between authorization and authentication? Authentication is the act of verifing that you are who you say you are, authorization is the system permitting you to do what you have permissions to do.  
