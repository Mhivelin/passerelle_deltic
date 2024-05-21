
import datetime
import json

from app.models.ebp import EBP
from app.models.zeendoc import Zeendoc
from app.models import database


def routine():
    # on récupère la liste passrelles
    passrelles = database.get_client_passerelle()

    for passerelle in passrelles:
        if passerelle["IdPasserelle"] == 1:
            P_remonte_paiement(passerelle["IdClient"])




def P_remonte_paiement(IdClient):
    """ routine de la passerelle de remontée des paiements """

    clientZeendoc = Zeendoc(IdClient)
    clientEBP = EBP(IdClient)

    # on récupère les paiements dans EBP

    paiements = clientEBP.getPaidPurchaseDocument()

