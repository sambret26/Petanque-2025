from flask import Blueprint, jsonify
from business import teamBusiness

teamBp = Blueprint('teams', __name__, url_prefix='/teams')

@teamBp.route('/getNumber', methods=['GET'])
def get_teams_number():
    return jsonify(teamBusiness.count()), 200

@teamBp.route('/getWaiting/<panel>', methods=['GET'])
def get_waiting(panel):
    return jsonify(teamBusiness.get_waitings(int(panel))), 200

@teamBp.route('/register/<number>', methods=['POST'])
def register(number):
    return jsonify(teamBusiness.register(int(number))), 200

@teamBp.route('/unregister/<number>', methods=['POST'])
def unregister(number):
    if teamBusiness.unregister(int(number)):
        return jsonify(number), 200
    return jsonify(number), 201

@teamBp.route('/luckyLoser/<panel>/<team>', methods=['POST'])
def lucky_loser(panel, team):
    status = teamBusiness.lucky_loser(int(panel), int(team))
    return jsonify(status), status