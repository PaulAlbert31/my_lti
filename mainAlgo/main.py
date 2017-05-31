from fonctions_utiles import vraisemblance, esperanceVraisemblance
import scipy
import jsonpickle
import question, theme, competence, etudiant, exercice



class Main(object):
    """Moteur de l'algorithme de recommendation 'Apprentissage adaptatif'    """

    #--------------------------------------------------------------------------
    
    def __init__(self, etudiants={}, themes={}, competences={}, exercices={}, questions={}):
        self.etudiants = etudiants
        self.themes = themes
        self.competences = competences
        self.exercices = exercices
        self.questions = questions

 
        
    
    #--------------------------------------------------------------------------

    def genererFE(self, eleve, competencesTestees):
        """Génère une Feuille d'Exercices correspondant à un élève et à des compétences"""
        return []
        
        
    #--------------------------------------------------------------------------


    def actualiserNiveaux(self, etudiant):
        questions = [self.questions[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
        reponses = [etudiant.questionsRepondues[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
        matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in questions]
        
        bnds = [[-10, 10]]*len(self.competences)
        f = lambda x : -vraisemblance(questions, x, matriceQ, reponses)
        opt = scipy.optimize.minimize(f, [0]*len(self.competences), bounds=bnds)
#        print(opt.x)
#        print(-opt.fun)
        etudiant.setNiveaux(opt.x)
        
        
    
#    def choisirQuestion(self, etudiant, competences):
#        maxProgres = float('-inf')
#        choixQuestion = None
#        # On parcours toutes les questions possibles
#        for questionChoisie in self.questions:
#            # Si la question concerne les compétences concernées
#            if [k for k in questionChoisie.competences if k in competences] != []:
#                questionsRepondues = [self.questions[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
#                reponses = [etudiant.questionsRepondues[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
#                matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in questionsRepondues]
#                matQChoisie = [1 if k in questionChoisie.competences else 0 for k in self.competences]
#                bnds = [[-10, 10]]*len(self.competences)
#                f = lambda x : -esperanceVraisemblance(questionsRepondues, [questionChoisie], x,  matriceQ, [matQChoisie], reponses)
#                opt = scipy.optimize.minimize(f, [0]*len(self.competences), bounds=bnds)
#                progres = sum([opt.x[c.nId]-etudiant.niveauxCompetences[c.nId] for c in competences])
#                if progres >= maxProgres:
#                    maxProgres = progres
#                    choixQuestion = questionChoisie
#        return choixQuestion

    def choisirExercice(self, etudiant, idCompetences):
        maxProgres = float('-inf')
        choixExercice = None
        competences = [self.competences[i] for i in idCompetences]
        # On parcours les exerices possibles
        for exercice in self.exercices.values():
            # Si l'exercice concerne les bonnes competences
            if [k for k in exercice.competences if k in competences] != []:
                questionsRepondues = [self.questions[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
                reponses = [etudiant.questionsRepondues[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
                matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in questionsRepondues]
                matQChoisies = [[1 if k in q.competences else 0 for k in self.competences] for q in exercice.questions]
                bnds = [[-10, 10]]*len(self.competences)
                f = lambda x : -esperanceVraisemblance(questionsRepondues, exercice.questions, x,  matriceQ, matQChoisies, reponses)
                opt = scipy.optimize.minimize(f, [0]*len(self.competences), bounds=bnds)
                progres = sum([opt.x[c.nId]-etudiant.niveauxCompetences[c.nId] for c in competences])
                if progres >= maxProgres:
                    maxProgres = progres
                    choixExercice = exercice
        # Renoie l'id de l'exercice choisi
        return choixExercice
    

    #--------------------------------------------------------------------------
        
    
    
    def ajouterTheme(self, idTheme, nom):
        self.themes[idTheme] = theme.Theme(idTheme, nom)
 
    def ajouterCompetence(self, idCompetence, nom, idTheme, idPrerequis):
        self.competences[idCompetence] = competence.Competence(idCompetence, nom, self.themes[idTheme], prerequis=[self.competences[i] for i in idPrerequis])

    def ajouterQuestion(self,  idQuestion, enonce, reponse, idThemes, idCompetences, discriminations, facilite):
        for k in self.competences:
            if not k in discriminations:
                if k in idCompetences:
                    discriminations[k] = 1
                else:
                    discriminations[k] = -1                    
        self.questions[idQuestion] = question.Question(idQuestion, enonce, reponse, themes=[self.themes[i] for i in idThemes], competences=[self.competences[i] for i in idCompetences], discriminations=discriminations, facilite=facilite)

    def ajouterExercice(self,  idExercice, enonce, idQuestions, idThemes, idCompetences):
        self.exercices[idExercice] = exercice.Exercice(idExercice, enonce, questions=[self.questions[i] for i in idQuestions], themes=[self.themes[i] for i in idThemes], competences=[self.competences[i] for i in idCompetences])

    def ajouterEtudiant(self,  idEtudiant, prenom, nom, niveauxCompetences, resultats):
        for k in self.competences:
            if not k in resultats:
                resultats[k] = -1                  
        self.etudiants[idEtudiant] = etudiant.Etudiant(idEtudiant, prenom, nom, niveauxCompetences, resultats)



        
#==============================================================================

if __name__ == "__main__":


    main = Main()
    
    # Il faut respecter l'ordre d'import themes -> competences -> questions -> exercices, etudiants
    
    main.ajouterTheme(0, "Arithmétique")
    main.ajouterCompetence(0, "Addition", 0, [])
    main.ajouterCompetence(1, "Soustraction", 0, [0])
    main.ajouterCompetence(2, "Multiplication", 0, [0])

    main.ajouterQuestion(0, "3 + 4 =", "7", [0], [0], {}, 1)
    main.ajouterQuestion(1, "2 + 5 =", "7", [0], [0], {}, 1)
    main.ajouterQuestion(2, "", "", [0], [0, 1], {}, 1)
    main.ajouterQuestion(3, "", "", [0], [0], {}, 1)
    main.ajouterQuestion(4, "", "", [0], [0], {}, 1)
    main.ajouterQuestion(5, "", "", [0], [0], {}, 1)
    main.ajouterQuestion(6, "", "", [0], [1], {}, 1)
    
    main.ajouterExercice(0, "texte", [0, 1], [0], [0])
    main.ajouterExercice(1, "texte", [2, 3, 4], [0], [0, 1])
    main.ajouterExercice(2, "texte", [5, 6], [0], [0, 1])

    main.ajouterEtudiant(0, "Bob", "Smith", {}, {0:0, 1:1, 6:0})
    
    bob = main.etudiants[0]

    bob.resultats[5]=1
    
    main.actualiserNiveaux(bob)
    print("?")
    print(main.choisirExercice(bob, [0]).nId)
        

