from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from extensions import mysql
import controllers

import os


# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SECURITY_URL_PREFIX'] = '/asdfj/pa1' 
# Initialize MySQL database connector
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = '485p3'
mysql.init_app(app)



# Register the controllers
app.register_blueprint(controllers.album, url_prefix='/b5340568bdcd46b4b5be/pa3')
app.register_blueprint(controllers.albums, url_prefix='/b5340568bdcd46b4b5be/pa3')
app.register_blueprint(controllers.pic, url_prefix='/b5340568bdcd46b4b5be/pa3')
app.register_blueprint(controllers.main, url_prefix='/b5340568bdcd46b4b5be/pa3')
app.register_blueprint(controllers.login, url_prefix='/b5340568bdcd46b4b5be/pa3')
app.register_blueprint(controllers.user, url_prefix='/b5340568bdcd46b4b5be/pa3')
app.register_blueprint(controllers.usr_logout, url_prefix='/b5340568bdcd46b4b5be/pa3')




# hahahahahah
app.secret_key = os.urandom(24)

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)