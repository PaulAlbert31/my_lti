# -*- coding: utf-8 -*-
from math import exp
import MySQLdb



def sigmoid(x):
    return 1/(1 + exp(-x))



def proba_juste(theta, d, facilite, Q):
    """Donne en fonction des paramètres la probabilité que la réponse soit juste"""
    K = len(theta)
    s = facilite
    for k in range(1,K):
        if not k==172:
            s += Q[k]*theta[k]*d[k]
    return sigmoid(s)


def proba_reponse(theta, d, facilite, Q, reponse):
    """Donne en fonction des paramètres la probabilité que la réponse corresponde à reponse (=0 ou 1)"""
    p = proba_juste(theta, d, facilite, Q)
    if reponse==1:
        return p
    else:
        return 1-p



def vraisemblance(questions, theta, matQ, reponses):
    L = 1
    # questions contient la liste des questions répondues
    for (i, q) in enumerate(questions):
        L = L*proba_reponse(theta, q.discriminations, q.facilite, matQ[i], reponses[i])
    return L


def esperanceVraisemblance(questions, questionsChoisies, theta, matQ, matQChoisies, reponses):
    ### à corriger
    L = 1
    # questions contient la liste des questions répondues
    for (i, q) in enumerate(questions):
        L = L*proba_reponse(theta, q.discriminations, q.facilite, matQ[i], reponses[i])
    for (i, qc) in enumerate(questionsChoisies):
        p = proba_juste(theta, qc.discriminations, qc.facilite, matQChoisies[i])
        L = L * (p*p + (1-p)*(1-p))
    return L
