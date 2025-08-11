from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from repositories.MatchsRepository import MatchsRepository

matchs_repository = MatchsRepository()

def generate(round_number, scope, match_status):
    print("Business")
    """
    Génère un PDF des matchs selon les critères spécifiés
    
    Args:
        round_number (int): Numéro du round
        scope (str): 'current' pour le round actuel, 'all' pour tous les rounds
        match_status (str): 'all' pour tous les matchs, 'started' pour les matchs commencés uniquement
        
    Returns:
        BytesIO: Flux binaire du PDF généré
    """
    # Options
    rounds = [round_number]
    round = 0
    if round_number == 1:
        round = 1
    elif round_number in [2, 3]:
        round = 2
        if scope == 'all':
            rounds = [2, 3]
    elif round_number in [4, 5, 6]:
        round = 3
        if scope == 'all':
            rounds = [4, 5, 6]
    else:
        round = round_number -3

    if match_status == 'started':
        status = [1]
    else:
        status = [0, 1, 2]

    # Configuration du document PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title=f"Feuilles de match - Manche {round}",
        author="Système de gestion de tournoi"
    )
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Contenu du document
    elements = []

    # Titre
    title = f"Feuilles de match - Manche {round}"
    elements.append(Paragraph(title, title_style))

    matches = matchs_repository.get_to_print(rounds, status)

    middle = len(matches)/2
    
    if not matches:
        return None
    # Pour chaque match, créer une section
    table_data_1 = [['Équipe 1 ', 'Équipe 2']]
    table_data_2 = [['Équipe 1 ', 'Équipe 2']]
    for i, match in enumerate (matches):
        if i < middle:
            table_data_1.append([match.team1, match.team2])
        else:
            table_data_2.append([match.team1, match.team2])
        
    # Style du tableau
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ])
    
    # Création des deux tables
    table1 = Table(table_data_1, colWidths=[doc.width/4.5]*2)
    table1.setStyle(table_style)
    
    table2 = Table(table_data_2, colWidths=[doc.width/4.5]*2)
    table2.setStyle(table_style)
    
    # Création d'un conteneur pour les deux tables côte à côte
    container_data = [[table1, table2]]
    container = Table(container_data, colWidths=[doc.width/2.0]*2)
    container_style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (1, 0), 0),
        ('RIGHTPADDING', (0, 0), (1, 0), 0),
        ('BOTTOMPADDING', (0, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (1, 0), 0)
    ])
    container.setStyle(container_style)
    
    elements.append(container)
    
    # Génération du PDF
    doc.build(elements)
    
    # Retourner le contenu du buffer
    buffer.seek(0)
    return buffer.getvalue()