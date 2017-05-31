# -*- coding: utf-8 -*-
class Competence(object):
    """Compétence mathémathique
    comme par exemple 'Réduire une fraction'    """

    def __init__(self, nId, texte, theme, prerequis=[]):
        self.texte = texte
        self.theme = theme
        self.nId = nId
        self.prerequis = prerequis
        
    def getId(self):
        return self.nId

    def getPrerequis(self):
        return self.prerequis

