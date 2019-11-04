from flask import request, Blueprint
from flask_api import status
from flask_jsontools import jsonapi


mod = Blueprint('endpoints', __name__)

@mod.route('/', methods=['GET'])
@jsonapi
def home():
    return status.HTTP_200_OK