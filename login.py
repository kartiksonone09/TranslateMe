from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
#from flask_mysqldb import MySQL
import mysql.connector


login_blueprint = Blueprint('login', __name__)


login = Flask(__name__)

# Configure MySQL
#login.config['MYSQL_HOST'] = 'your_mysql_host'
#login.config['MYSQL_USER'] = 'your_mysql_user'
#login.config['MYSQL_PASSWORD'] = 'your_mysql_password'
#login.config['MYSQL_DB'] = 'your_database_name'
#login.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#mysql = MySQL(login)

"""mydb = mysql.connector.connect(
  host="ttransdb.mysql.database.azure.com",
  user="t2sadmin",
  password="Test@123",
  database="t2sdb",
  charset='utf8mb4'
)"""
mydb = mysql.connector.connect(
  host="t2sdb.mysql.database.azure.com",
  user="t2sadmin",
  password="Test@123",
  database="t2sdb",
  charset='utf8mb4'
)

mycursor = mydb.cursor()
#login.secret_key = 'your_secret_key'

"""@login.route('/')
def index():
    return render_template('admin_login.html')"""

@login.route('/admin_login', methods=['POST'])
def admin_login():
    #print("hello")
    """if request.method == 'POST':
        print ("hello")
        username = request.form['username']
        password = request.form['password']



        # Check if the username and password match a record in the database
        mycursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        print(mycursor)
        user = mycursor.fetchone()
        if user:
            # If the user is found, store user data in session and redirect to the admin dashboard
            session['user'] = user
            return redirect(url_for('admin_dashboard'))
        else:
            # If user is not found, redirect back to login with an error message
            return render_template('admin_login.html', error='Invalid credentials')"""


"""@login.route('/logout')
def logout():
    # Clear the session data to logout the user
    session.pop('user', None)
    return redirect(url_for('index'))"""
@login.route('/admin_dashboard')
def admin_dashboard():
    # Perform any necessary logic before redirection
    # For example, you can check some conditions and decide where to redirect
    # In this example, it always redirects to the 'redirected.html' page
    return render_template('admin_dashboard.html')



