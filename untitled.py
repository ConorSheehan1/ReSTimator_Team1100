# from flask import Flask, render_template, request, g, url_for
# import sqlite3

# # Application object (set different path for static files on the web)
# app = Flask(__name__, static_url_path="/static")
# # Enable debugging of app
# app.debug = True

# # Decorator used to register a view function for the url rule parameter
# # (Listens for only GET by default)

# @app.route("/")
# def HTML():
#     '''Render html template'''
#     return render_template("APredictor.html")

# # Define a route for the action of the form, for example '/NAMETHIS/'
# @app.route('/NAMETHIS/', methods=['POST'])
# def NAMETHIS():
#     name = request.form['yourname']
#     email = request.form['youremail']
#     return render_template('form_action.html', name=name, email=email)

# if __name__ == "__main__":
#     # Start server with run method
#     app.run()


# <!DOCTYPE html>
# <html>
# <head>
# 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
# 	<meta charset="UTF-8">
# 	<!-- SUPPORT FOR IE6-8 OF HTML5 ELEMENTS -->
# 	<!--[if lt IE 9]>
# 	<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
# 	<![endif]-->
# 	<title>APredictor</title>   
# 	<!-- style sheets -->
# 	<link rel="stylesheet" type="text/css" href="/static/css/reset.css">
# 	<link rel="stylesheet" type="text/css" href="/static/css/style.css">
# </head>
# <body>
# 	<div id="page" data-role="page">
		
# 		<header>

# 			<h1>APredictor<h1>

# 		</header>
		
# 		<div id="navigation">

# 			<ul>
# 				<li><a href="#">Login</a></li>
# 				<li><a href="#">Upload</a></li>
# 				<li><a href="#">Application</a></li>
# 			</ul>

# 		</div>

# 		<div id="content">

# <!-- 			<div id="input">
# 				<form method="post" action="{{ url_for('NAMETHIS') }}">
# 					<label for="yourname">Please enter your name:</label>
#                   	<input type="text" name="yourname" /><br />
#                   	<label for="youremail">Please enter your email:</label>
#                   	<input type="text" name="youremail" /><br />
#                   	<input type="submit" />
# 				</form>
# 			</div> -->

# 			<div id="analysis">
			
# 			</div>

# 		</div>
		
# 		<footer>
		
# 		</footer>
# 	</div>
# 	<!-- Main script -->
# 	<script type="text/javascript" src="/static/scripts/main.js"></script>
# </body>
# </html>

# <!DOCTYPE html>
# <html lang="en">
# <head>
# 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
# 	<meta charset="UTF-8">
# 	<!-- SUPPORT FOR IE6-8 OF HTML5 ELEMENTS -->
# 	<!--[if lt IE 9]>
# 	<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
# 	<![endif]-->

# 	<title>ReSTimator - {{ username }} </title>

# 	<!-- style sheets -->
# 	<!-- <link rel="stylesheet" type="text/css" href="/static/css/reset.css"> -->
# 	<!-- <link rel="stylesheet" type="text/css" href="/static/css/style.css"> -->
# 	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
	
# 	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
# 	<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
# </head>
# <body>
# 	<!-- <div id="page" data-role="page"> -->
# 	<div class="container">
		
# 		<header>

# 			<h1>ReSTimator Image Goes Here<h1>

# 		</header>
		
# 		<div id="navigation">

# 			<ul>
# 				<li><a href="#">Login</a></li>
# 				<li><a href="#">Upload</a></li>
# 				<li><a href="#">Application</a></li>
# 			</ul>

# 		</div>

# 		<div id="content">
# 			{% block content %}{% endblock %} <!-- Block control statement: where other templates can insert themselves -->
# 		</div>
		
# 		<footer>
		
# 		</footer>
# 	</div>
# 	<!-- Main script -->
# 	<script type="text/javascript" src="/static/scripts/main.js"></script>
# </body>
# </html>