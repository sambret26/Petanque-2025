from flask import Blueprint, jsonify, request
from business import printBusiness

printBp = Blueprint('print', __name__, url_prefix='/print')

@printBp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    
    # Récupération des paramètres avec valeurs par défaut
    round_number = data.get('round')
    scope = data.get('scope', 'current')  # 'current' ou 'all'
    match_status = data.get('matchStatus', 'all')  # 'all' ou 'started'
    
    # Validation des paramètres
    if round_number is None:
        return jsonify({'error': 'Le paramètre round est requis'}), 400
    if scope not in ['current', 'all']:
        return jsonify({'error': 'Le paramètre scope doit être "current" ou "all"'}), 400
    if match_status not in ['all', 'started']:
        return jsonify({'error': 'Le paramètre matchStatus doit être "all" ou "started"'}), 400
    
    try:
        # Appel à la couche métier avec les paramètres
        result = printBusiness.generate(
            round_number=round_number,
            scope=scope,
            match_status=match_status
        )
        if result is None:
            return '', 201
        return result, 200, {'Content-Type': 'application/pdf'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
