from flask import Blueprint, jsonify
from business import matchBusiness

matchBp = Blueprint('matches', __name__, url_prefix='/matches')

@matchBp.route('/getMatches/<panel>', methods=['GET'])
def get_matches(panel):
    return jsonify(matchBusiness.get_matches(int(panel))), 200

@matchBp.route('/generate/<cat>', methods=['POST'])
def generate(cat):
    return jsonify(matchBusiness.generate(int(cat))), 200

@matchBp.route('/ungenerate/<cat>', methods=['POST'])
def ungenerate(cat):
    return jsonify(matchBusiness.ungenerate(int(cat))), 200

@matchBp.route('/launchMatches/<panel>', methods=['POST'])
def launch_matches(panel):
    return jsonify(matchBusiness.launch_matches(int(panel))), 200

@matchBp.route('/changeStatus/<match_id>', methods=['POST'])
def change_status(match_id):
    return jsonify(matchBusiness.change_status(int(match_id))), 200

@matchBp.route('/setWinner/<match_id>/<winner>', methods=['POST'])
def set_winner(match_id, winner):
    if int(winner) == 0:
        status = matchBusiness.unset_winner(int(match_id))
    else:
        status = matchBusiness.set_winner(int(match_id), int(winner))
    return jsonify(status), status

@matchBp.route('/createMatch/<panel>/<team_number1>/<team_number2>', methods=['POST'])
def create_match(panel, team_number1, team_number2):
    match, status = matchBusiness.create_match(int(panel), int(team_number1), int(team_number2))
    return jsonify({'match': match}), status

@matchBp.route('/deleteMatch/<match_id>', methods=['POST'])
def delete_match(match_id):
    status = matchBusiness.delete_match(int(match_id))
    return jsonify(status), status