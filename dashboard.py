from flask import Flask, redirect, url_for, request, render_template, session, Blueprint
import requests, os, uuid, json
from dotenv import load_dotenv
import mysql.connector

dashboard_blueprint = Blueprint('dashboard', __name__)

load_dotenv()

dashboard = Flask(__name__)

"""mydb = mysql.connector.connect(
  host="t2sdb.mysql.database.azure.com",
  user="t2sadmin",
  password="Test@123",
  database="t2sdb",
  charset='utf8mb4'
)

mycursor = mydb.cursor()


@dashboard.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    mycursor.execute("SELECT * FROM history")

    myresult = mycursor.fetchall()

    return render_template('dashboard.html', myresult=myresult)"""


