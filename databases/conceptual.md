### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
postgreSQL is an open-source production quality database that follows SQL closely.  

- What is the difference between SQL and PostgreSQL? SQL is a 'language' for querying databases and PostgreSQL is a database that uses SQL.

- In `psql`, how do you connect to a database? \c <database_name>

- What is the difference between `HAVING` and `WHERE`? 
Where clause you use to filter your select statement, a having clause you use to filter an aggregrate function like count(1)

- What is the difference between an `INNER` and `OUTER` join? inner join selects the elements that both tables have in common. an 
outer joint selects all elements from one of the tables (left or right) and common elements from the other table. 

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?  Left outer selects all elements from the first table in the join statement, right selects all elements from the second table mentioned

- What is an ORM? What do they do?  ORM is like SQLAlchmey it allows users to interact with databses using features of a software language instead of writing sql.  Developers can interact with database objects in python witht he example of sqlalchmey. 

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?  making an ajax call allows the page to render dynamic content on the fly without having to reload the page. ajax uses javascript whereas requests use python-flask. server requests are typically used for one server to communicate with other servers

- What is CSRF? What is the purpose of the CSRF token?  Cross site request forgery.  its a way to hack a form from a site that didn't present the form. The CSRF token is a unique token that the server uses to verify the post request was from the page that it rendered. 

- What is the purpose of `form.hidden_tag()`? taht is the csrf token and is used to verify that the form was posted from the site that rendered the form.
