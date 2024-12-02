# import libraries
import os
from Flask import Flask, redirect, url_for, session, request, jsonify
from Flask_oauthlib.client import OAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# create the application
app = Flask(__name__)
app.secret_key = "key"  # add the key

GOOGLE_CLIENT_SECRETS_FILE = "path_to_your_credentials.json"  # add the client id
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# define the endpoints
@app.route('/')

def home(): 
    return "Welcome to your surgery follow up booking client"

@app.route('/authorize')

def authorize():

