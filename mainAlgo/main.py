# -*- coding: utf-8 -*- 
from fonctions_utiles import vraisemblance, esperanceVraisemblance
from scipy import optimize
import  theme, competence, etudiant, exercice



class Main(object):
    """Moteur de l'algorithme de recommendation 'Apprentissage adaptatif'    """

    #--------------------------------------------------------------------------
    
    def __init__(self, etudiants={}, themes={}, competences={}, exercices={}, questions={}):
        self.etudiants = etudiants
        self.themes = themes
        self.competences = competences
        self.exercices = exercices
        
    
    #--------------------------------------------------------------------------

        
    def actualiserNiveaux(self, idEtudiant):
        etudiant = self.etudiants[idEtudiant]
        questions = [self.questions[i] for i in etudiant.resultats if etudiant.resultats[i]!=-1]
        reponses = [etudiant.resultats[i] for i in etudiant.resultats if etudiant.resultats[i]!=-1]
        matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in questions]
        
        bnds = [[-10, 10]]*len(self.competences)
        f = lambda x : -vraisemblance(questions, x, matriceQ, reponses)
        opt = optimize.minimize(f, [0]*len(self.competences), bounds=bnds)
#        print(opt.x)
#        print(-opt.fun)
        etudiant.setNiveaux(opt.x)
        
        
    
    def genererFE(self, idEtudiant, idCompetences, nbExercices):
        """Génère une Feuille d'Exercices correspondant à un élève et à des compétences"""
        competences = [self.competences[i] for i in idCompetences]
        etudiant = self.etudiants[idEtudiant]
        resultats = [self.exercices[i] for i in etudiant.resultats if etudiant.resultats[i]!=-1]
        reponses = [etudiant.resultats[i] for i in etudiant.resultats if etudiant.resultats[i]!=-1]
        matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in resultats]
        niveauxPred = etudiant.niveauxCompetences
        choixExercices = []
        matQchoisies = []
        for n in range(nbExercices):
            maxProgres = float('-inf')
            choixCourant = None
            niveauxCourant = niveauxPred
            # On parcours tous les exercices possibles
            for exo in self.exercices.values():
                # Si l'exercice concerne les compétences concernées et n'est pas déjà choisi
                if (not exo in choixExercices) and ([k for k in exo.competences if k in competences] != []):
                    matQCourante = [1 if k in exo.competences else 0 for k in self.competences]
                    bnds = [[-10, 10]]*len(self.competences)
                    f = lambda x : -esperanceVraisemblance(resultats, choixExercices+[exo], x,  matriceQ, matQchoisies+[matQCourante], reponses)
                    opt = scipy.optimize.minimize(f, [0]*len(self.competences), bounds=bnds)
                    progres = sum([opt.x[c.nId]-niveauxPred[c.nId] for c in competences])
                    if progres >= maxProgres:
                        niveauxCourant = opt.x
                        maxProgres = progres
                        choixCourant = exo
            choixExercices.append(choixCourant)
            matQchoisies.append(matQCourante)
            # Une fois l'exo choisi on mets à jour le vecteur de compétences prédit
            niveauxPred = niveauxCourant
        return choixExercices
        
      
    
    def choisirExercice(self, idEtudiant, idCompetences, ):
        maxProgres = float('-inf')
        choixExercice = None
        competences = [self.competences[i] for i in idCompetences]
        etudiant = self.etudiants[idEtudiant]
        # On parcours tous les exercices possibles
        resultats = [self.exercices[i] for i in etudiant.resultats if etudiant.resultats[i]!=-1]
        reponses = [etudiant.resultats[i] for i in etudiant.resultats if etudiant.resultats[i]!=-1]
        matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in resultats]
        for exo in self.exercices.values():
            # Si l'exercice concerne les compétences concernées
            if [k for k in exo.competences if k in competences] != []:
                matQChoisie = [1 if k in exo.competences else 0 for k in self.competences]
                bnds = [[-10, 10]]*len(self.competences)
                f = lambda x : -esperanceVraisemblance(resultats, [exo], x,  matriceQ, [matQChoisie], reponses)
                opt = scipy.optimize.minimize(f, [0]*len(self.competences), bounds=bnds)
                progres = sum([opt.x[c.nId]-etudiant.niveauxCompetences[c.nId] for c in competences])
                if progres >= maxProgres:
                    maxProgres = progres
                    choixExercice = exo
        return choixExercice

    

    #--------------------------------------------------------------------------
        
    
    
    def ajouterTheme(self, idTheme, nom):
        self.themes[idTheme] = theme.Theme(idTheme, nom)
 
    def ajouterCompetence(self, idCompetence, nom, idTheme, idPrerequis):
        self.competences[idCompetence] = competence.Competence(idCompetence, nom, self.themes[idTheme], prerequis=[self.competences[i] for i in idPrerequis])

    def ajouterExercice(self, idExercice, enonce, reponse, idThemes, idCompetences, discriminations, facilite):
        for k in self.competences:
            if not k in discriminations:
                if k in idCompetences:
                    discriminations[k] = 1
                else:
                    discriminations[k] = -1                    
        self.exercices[idExercice] = exercice.Exercice(idExercice, enonce, reponse, themes=[self.themes[i] for i in idThemes], competences=[self.competences[i] for i in idCompetences], discriminations=discriminations, facilite=facilite)

    def ajouterEtudiant(self,  idEtudiant, prenom, nom, niveauxCompetences, resultats):
        for k in self.competences:
            if not k in resultats:
                resultats[k] = -1                  
        self.etudiants[idEtudiant] = etudiant.Etudiant(idEtudiant, prenom, nom, niveauxCompetences, resultats)



        
#==============================================================================

if __name__ == "__main__":


    main = Main()
    
    # Il faut respecter l'ordre d'import themes -> competences -> exercices, etudiants
    
    main.ajouterTheme(0, "Arithmétique")
    main.ajouterCompetence(0, "Addition", 0, [])
    main.ajouterCompetence(1, "Soustraction", 0, [0])
    main.ajouterCompetence(2, "Multiplication", 0, [0])


    # idExercice, enonce, reponse, idThemes, idCompetences, discriminations, facilite
    main.ajouterExercice(0, "texte", "", [0], [0], {}, 1)
    main.ajouterExercice(1, "texte", "", [0], [0, 1], {}, 1)
    main.ajouterExercice(2, "texte", "", [0], [0, 1], {}, 1)


    main.ajouterEtudiant(0, "Bob", "Smith", {}, {0:0, 1:1, 6:0})
    
    bob = main.etudiants[0]

    bob.resultats[5]=1
    
    
    main.actualiserNiveaux(0)
    print(main.choisirExercice(0, [0]).nId)
    print([exo.nId for exo in main.genererFE(0, [0], 3)])
        

