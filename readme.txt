-----------------
|  CRM software |
-----------------
	
Software stack:
Backend  -------------------------- html,css,javascript,bootstrap
database : sqlite
frontend -------------------------- python using flask

requirements -modern browser, flask, and active internet connection

flask(Werkzeug) 2.0.3
python 3.9.1

Updates from the previous ER diagram and database schema:
--> used an extra table for service requests
--> removed the attributes no of interactions, no of units sold from the synergy table

steps to run the application:
run load.py (python load.py) : for having some base hardcoded data to start with
run app.py (python app.py)