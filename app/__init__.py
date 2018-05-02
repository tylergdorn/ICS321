from flask import Flask
from config import Config
from app.db import db
import click


app = Flask(__name__)
app.config.from_object(Config)

@app.cli.command()
def initdb():
    """Initialize the database."""
    db.init()
    click.echo('Initializing the db')

from app import routes
