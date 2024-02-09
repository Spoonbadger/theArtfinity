import csv
import datetime
import pytz
import re
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def slugify(text):
    # Replace non-word characters with hyphens and lower the case
    return re.sub(r'\W+', '-', text).lower()


art_scene_options = {
    '2': {'scene_city_name': 'Amsterdam'},
    '3': {'scene_city_name': 'Bruges'},
    '4': {'scene_city_name': 'Chicago'},
    '5': {'scene_city_name': 'Denver'},
    '6': {'scene_city_name': 'Florence'},
    '7': {'scene_city_name': 'Houston'},
    '8': {'scene_city_name': 'Los Angeles'},
    '9': {'scene_city_name': 'Miami'},
    '1': {'scene_city_name': 'New York'},
    '10': {'scene_city_name': 'Paris'},
    '11': {'scene_city_name': 'Philadelphia'},
    '12': {'scene_city_name': 'Portland'},
    '13': {'scene_city_name': 'San Francisco'},
    '14': {'scene_city_name': 'Seattle'},
    '15': {'scene_city_name': 'Vienna'},
}


state_options = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District Of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    '': '...',
    'AS': 'American Samoa',
    'GU': 'Guam',
    'MP': 'Northern Mariana Islands',
    'PR': 'Puerto Rico',
    'UM': 'United States Minor Outlying Islands',
    'VI': 'Virgin Islands'
}

