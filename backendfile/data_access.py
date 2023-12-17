from application.models import show
from application.models import venue
from main import cache
from flask import Flask
from flask import request,jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from flask import current_app as app
from application.models import show,venue,booking,user,admin

from flask import redirect, url_for
from flask import flash
from sqlalchemy.orm import query
from datetime import datetime
@app.route('/allvenues', methods=['GET', 'POST'])
@cache.cached(timeout=50, key_prefix='get all venues') 
def allvenues():
    venues= venue.query.all()
    return render_template('venuelist.html',venues=venues)
@cache.memoize(50)
def get_venues_by_venuename(venuename):
    venues = venue.query.filter(venue.any(venuename=venuename)) 
    return venues.all()