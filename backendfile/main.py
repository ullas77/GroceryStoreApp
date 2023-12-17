import os
from flask import Flask, render_template_string
from application import config
from flask_restful import Resource,Api
from application.config import LocalDevelopmentConfig
from application.database import db
from celery_worker import make_celery
from application.models import product,category,purchased
from application.models import user
import requests
from celery.result import AsyncResult
import time
import csv
from httplib2 import Http
from celery.schedules import crontab
from json import dumps
from datetime import timedelta
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_cors import CORS
# from application.security import user_datastore,secu
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity,unset_jwt_cookies

from jinja2 import Template

from api.resource import user, api
from werkzeug.security import generate_password_hash, check_password_hash



app = None
# cache=None
def create_app():
    app = Flask(__name__, template_folder="templates")
    
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    app.app_context().push()
    

    return app




app = create_app()
api.init_app(app)

    
    



app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    

)


celery = make_celery(app)

@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b

@celery.on_after_configure.connect
def setup_monthly_report(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=11, minute=30, day_of_month='27'),
        send_monthly_purchasing_report.s(),
    )


@celery.on_after_configure.connect
def setup_daily_reminder(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=11, minute=30),
        send_remainder.s(),
        name='daily-remainder-chat'
    )

# @celery.on_after_configure.connect
# def setup_periodic_task(sender, **kwargs):
#     sender.add_periodic_task(10.0, send_remainder.s(),name='daily-remainder-chat')


CORS(app, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response



@celery.task()
def generate_csv(updated_product_names=None):
    time.sleep(6)
    fields = ['Name', 'Rate per item','Stock Remaining(in units)']

    products = product.query.all()

    rows = []
    for pro in products:
        rows.append([pro.productname,pro.rateperunit,pro.maxquantity])

    with open("static/productsdata.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    return "CSV generation completed"

from application.controllers import *
@app.route("/trigger_celery_job", methods=["GET", "POST"])
@jwt_required()

def trigger_celery_job():
    updated_product_names = {
        "product1": "Updated Name 1",
        "product2": "Updated Name 2",
        "product3": "Updated Name 3",
        "product4": "Updated Name 4",
        "product5": "Updated Name 5",
        "product6": "Updated Name 6"
    }
    
    generate_csv.delay(updated_product_names)
    
    
    
    response = '''
        <script>
            alert("CSV generated successfully");
            window.location.href = "http://localhost:8080/#/storemanagerlogin"; 
        </script>
    '''
    return response, 200    
@app.route("/status/<id>")
def check_status(id):
    res = AsyncResult(id)
    
    return {
        "Task ID": res.id,
        "Task State": res.state,
        "Task Result": res.result
    }

import requests
import json

@celery.task()


def send_remainder():
    
    #users = user.query.all
    current_time = datetime.now()
    users = user.query.all()

    for use in users:
        if use.role != "admin" and use.role != "storemanager" and use.timestamp <= (datetime.now() - timedelta(hours=24)):
            url =  "https://chat.googleapis.com/v1/spaces/AAAARb8O3AU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=C8eoGkvciq3IK0T31MgffhDULXxUo_8QzXlBWXat6zo"
            bot_message = {
                'text': f"Hello {use.username}, you have not logged in for 24 hours!. Please visit our app and buy something with huge discounts and offers like never before!!"
            }
            message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            http_obj = Http()
            response = http_obj.request(
                uri=url,
                method='POST',
                headers=message_headers,
                body=dumps(bot_message),
            )
            print(response)



SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS= "email@grocerystoreadmin.com"
SENDER_PASSWORD =""
def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
                msg.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part=MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
        msg.attach(part)
    S= smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    S.login(SENDER_ADDRESS, SENDER_PASSWORD)
    S.send_message(msg)
    S.quit()
    return True






@celery.task
def send_monthly_purchasing_report():
    today = datetime.now()
    last_day_of_current_month = today
    first_day_of_previous_month = last_day_of_current_month.replace(day=1)
    user_purchased_items = {}
    purchased_items = purchased.query.filter(
        purchased.timestamp >= first_day_of_previous_month,
        purchased.timestamp <= last_day_of_current_month
    ).all()
    for item in purchased_items:
        use = user.query.get(item.userid)
        if use.userid not in user_purchased_items:
            user_purchased_items[use.userid] = []
        user_purchased_items[use.userid].append(item)
    for user_id, items in user_purchased_items.items():
        use = user.query.get(user_id)
        sub = "Your Monthly Purchasing Report"
        email_mess = f"<html><body>"
        email_mess += f"<p style='font-size: 20px; color: #007bff;'>Hi {use.username},</p>"
        email_mess += f"<p style='font-size: 18px; margin: 20px 0; color: #333;'>Here is your monthly purchasing report for the previous month:</p>"

        for item in items:
            email_mess += f"<div style='background-color: #f5f5f5; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); padding: 20px; margin-top: 20px;'>"
            email_mess += f"<p style='font-size: 16px; margin: 0; color: #333;'>Purchasing ID: {item.purchasingid}</p>"
            email_mess += f"<p style='font-size: 16px; margin: 0; color: #333;'>Product Name: {item.productname}</p>"
            email_mess += f"<p style='font-size: 16px; margin: 0; color: #333;'>Quantity Purchased: {item.quantity} units</p>"
            email_mess += f"<p style='font-size: 16px; margin: 0; color: #333;'>Purchase Date and Time: {item.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>"
            email_mess += "</div>"

        email_mess += "</body></html>"
        send_email(
            to_address=use.useremail,
            subject=sub,
            message=email_mess,
            content="html",  
        )
    return "Monthly reports sent successfully"




#celery -A main.celery worker -l info
#celery -A main.celery beat --max-interval 2 -l info
#pip install flask flask-sqlalchemy celery[redis]
#source .env/bin/activate
#virtualenv .env
#sudo apt install python3-virtualenv
#cd "/mnt/c/Users/ullas/Desktop/mad2/ticket"
#http://localhost:8025/#
#Mailhog
#cd "/mnt/c/Users/ullas/Desktop/mad2/ticket final mad2"
















if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=5000)


