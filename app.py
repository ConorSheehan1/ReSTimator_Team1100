from flask import Flask, render_template, request, g, url_for
import sqlite3

# Application object (set different path for static files on the web)
app = Flask(__name__, static_url_path="/static")
# Enable debugging of app
app.debug = True

# Decorator used to register a view function for the url rule parameter
# (Listens for only GET by default)

@app.route("/")
def HTML():
    '''Render html template'''
    return render_template("APredictor.html")

# Define a route for the action of the form, for example '/NAMETHIS/'
@app.route('/NAMETHIS/', methods=['POST'])
def NAMETHIS():
    name = request.form['yourname']
    email = request.form['youremail']
    return render_template('form_action.html', name=name, email=email)

if __name__ == "__main__":
    # Start server with run method
    app.run()
