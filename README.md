# Customer Relationship Management
This software basically connects a client to its customer base. These are the basic functionalities of this software : Store customer contact information Record service issues Manage feedback of the customer base of a particular client. Analyze the feedback of a particular client and suggests some areas where the client has to improve in order to improve its relationship with its user Help a client target potential user base based on the information stored on the users activity


Software stack:
Backend  : html,css,javascript,bootstrap
database : sqlite
frontend : python using flask

requirements -modern browser, flask, and active internet connection

flask(Werkzeug) 2.0.3
python 3.9.1

Updates from the previous ER diagram and database schema:
--> used an extra table for service requests
--> removed the attributes no of interactions, no of units sold from the synergy table

steps to run the application:
run load.py (python load.py) : for having some base hardcoded data to start with
run app.py (python app.py)
