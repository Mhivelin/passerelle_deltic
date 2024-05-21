"""
Controlleur pour les routes des vue liées à l'interface
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.models import database


# Création d'un Blueprint pour le interface controller
v_interface_bp = Blueprint("v_interface", __name__)
@v_interface_bp.route("/")
@login_required
def home():
    try:
        clients_data = database.get_clients_with_passerelles_and_champs()

        clients_dict = {}
        for row in clients_data:
            client_id = row['IdClient']
            if client_id not in clients_dict:
                clients_dict[client_id] = {
                    'IdClient': client_id,
                    'Username': row['Username'],
                    'passerellesClient': [],
                    'all_champs': []  # Add this line to store all champs for the client
                }
            if row['IdPasserelle']:
                passerelle = next((p for p in clients_dict[client_id]['passerellesClient'] if p['IdPasserelle'] == row['IdPasserelle']), None)
                if not passerelle:
                    passerelle = {
                        'IdPasserelle': row['IdPasserelle'],
                        'LibPasserelle': row['LibPasserelle'],
                        'champs': []
                    }
                    clients_dict[client_id]['passerellesClient'].append(passerelle)
                if row['IdChamp']:
                    champ = {
                        'IdChamp': row['IdChamp'],
                        'LibChamp': row['LibChamp'],
                        'Valeur': row['Valeur']
                    }
                    passerelle['champs'].append(champ)
                    clients_dict[client_id]['all_champs'].append(champ)  # Add this line to collect all champs

        clients = list(clients_dict.values())
        return render_template("clients.html", clients=clients)
    except Exception as e:
        return str(e)



@v_interface_bp.route("/documentation")
def documentation():
    return render_template("documentation.html")