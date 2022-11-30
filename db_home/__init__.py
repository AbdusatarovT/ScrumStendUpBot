from flask import Blueprint

home_route = Blueprint('home',__name__) # static_folder='../static'

from .view import *
