# -*- coding: utf-8 -*-
class Etudiant(object):
    """Représentation d'un étudiant et de ses capacités    """

    def __init__(self, nId, prenom, nom, niveauxCompetences={}, resultats={}):
        self.nId = nId
        self.prenom = prenom
        self.nom = nom
        self.niveauxCompetences = {} ## {1:theta_1, 2:theta_2, ...}

        self.resultats = resultats ## {ex.idNb: -1 non repondue, 0 faux ou 1 juste}
        
    def getNiveau(self, competenceId):
        return self.niveauxCompetences[competenceId]
        
    def setNiveaux(self, niveaux):
        self.niveauxCompetences = niveaux
 
    def getCompetences(self):
        return self.niveauxCompetences
        
    def majResultat(self, dict):
        self.resultats.update(dict)
    
