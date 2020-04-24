import sqlite3
from flask import Flask, redirect, request

# Configure applicaton
app = Flask(__name__)

# Configure connection to database
db = sqlite3.connect('pathfinder2.db')

# Default route
@app.route('/')
def index():
    return 'index'
