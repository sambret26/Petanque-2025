from flask import Blueprint, jsonify
from business import tournamentBusiness

tournamentBp = Blueprint('tournament', __name__, url_prefix='/tournament')

@tournamentBp.route('/init', methods=['POST'])
def init():
    return jsonify(tournamentBusiness.init()), 200