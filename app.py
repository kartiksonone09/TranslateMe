from flask import Flask, redirect, url_for, request, render_template, session, Blueprint
from dashboard import dashboard_blueprint
from login import login_blueprint
import requests, os, uuid, json
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"


app.register_blueprint(login_blueprint)
app.register_blueprint(dashboard_blueprint)

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


@app.route('/', methods=['GET'])
def index():
    mycursor.execute("SELECT * FROM history")

    myresult = mycursor.fetchall()

    return render_template('index.html', myresult=myresult)


@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']
    print(target_language)
    selected_option = request.form.get('langid')
    print(selected_option)

    # Load the values from .env
    #key = os.environ['KEY']
    #endpoint = os.environ['ENDPOINT']
    #location = os.environ['LOCATION']
    key="00024ab1c3c54be0aa3e5bf48346d945"
    endpoint="https://api.cognitive.microsofttranslator.com/"
    location="eastus"


    # Indicate that we want to translate and the API version (3.0) and the target language
    path = 'translate/?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']
    
    # store in the Database
    sql = "INSERT INTO history (transated_text, original_text, target_language) VALUES (%s, %s, %s)"
    val = (translated_text, original_text, target_language)
    mycursor.execute(sql, val)

    mydb.commit()

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
    
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    # Perform any necessary logic before redirection
    # For example, you can check some conditions and decide where to redirect
    # In this example, it always redirects to the 'redirected.html' page
    if request.method == 'POST':
        print ("hello")
        """sql = "INSERT INTO t2sdb.admin (username, password) VALUES (%s, %s)"
        val = ("ninad", "Test@123")
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")"""
        username = request.form['username']
        password = request.form['password']

        cursor = mycursor
        
        # Check if the username and password match a record in the database
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        #cursor.execute("SELECT * FROM t2sdb.admin")
        user = cursor.fetchone()
        if user:
            # If the user is found, store user data in session and redirect to the admin dashboard
            session['user'] = user
            return redirect(url_for('admin_dashboard'))
        else:
            # If user is not found, redirect back to login with an error message
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    # Perform any necessary logic before redirection
    # For example, you can check some conditions and decide where to redirect
    # In this example, it always redirects to the 'redirected.html' page
    mycursor.execute("SELECT * FROM history")
    myresult = mycursor.fetchall()
    return render_template('admin_dashboard.html', myresult=myresult)
