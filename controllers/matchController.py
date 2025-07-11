from flask import Blueprint, jsonify
from business import matchBusiness

matchBp = Blueprint('matches', __name__, url_prefix='/matches')

@matchBp.route('/getMatches/<panel>', methods=['GET'])
def getMatches(panel):
    return jsonify(matchBusiness.getMatches(int(panel))), 200

@matchBp.route('/generate/<cat>', methods=['POST'])
def generate(cat):
    return jsonify(matchBusiness.generate(int(cat))), 200

@matchBp.route('/ungenerate/<cat>', methods=['POST'])
def ungenerate(cat):
    return jsonify(matchBusiness.ungenerate(int(cat))), 200

@matchBp.route('/launchMatches/<panel>', methods=['POST'])
def launchMatches(panel):
    return jsonify(matchBusiness.launchMatches(int(panel))), 200

@matchBp.route('/changeStatus/<matchId>', methods=['POST'])
def changeStatus(matchId):
    return jsonify(matchBusiness.changeStatus(int(matchId))), 200

@matchBp.route('/setWinner/<matchId>/<winner>', methods=['POST'])
def setWinner(matchId, winner):
    if int(winner) == 0:
        status = matchBusiness.unsetWinner(int(matchId))
    else:
        status = matchBusiness.setWinner(int(matchId), int(winner))
    return jsonify(status), status

@matchBp.route('/createMatch/<panel>/<teamNumber1>/<teamNumber2>', methods=['POST'])
def createMatch(panel, teamNumber1, teamNumber2):
    match, status = matchBusiness.createMatch(int(panel), int(teamNumber1), int(teamNumber2))
    return jsonify({'match': match}), status

@matchBp.route('/deleteMatch/<matchId>', methods=['POST'])
def deleteMatch(matchId):
    status = matchBusiness.deleteMatch(int(matchId))
    return jsonify(status), status


