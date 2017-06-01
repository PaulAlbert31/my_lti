 # coding=utf-8
def get_exo(num_exo):
    num_exo=int(num_exo)
    num_exo1=num_exo
    data=open('./exos/exos.tex').read()
    if num_exo == -1:
        return data
    if num_exo>173:
        num_exo=num_exo+2
    if num_exo>205:
        num_exo=num_exo+1
    for i in range(1,num_exo+4):
        pos_debut1=data[10:].find('\exo')
        pos_debut2=data[10:].find('\pb')
        pos_debut3=data[10:].find('begin{exo}')
        if pos_debut2==-1:
            pos_debut2=pos_debut1+1
        if pos_debut3==-1:
            pos_debut3=pos_debut1+1
        if pos_debut1>pos_debut2 and pos_debut3>pos_debut2:
            data=data[pos_debut2+10:]
        if pos_debut2>pos_debut3 and pos_debut1>pos_debut3:
            data=data[pos_debut3+9:]
        if pos_debut3>pos_debut1 and pos_debut2>pos_debut1:
            data=data[pos_debut1+10:]
        if pos_debut1==-1 and pos_debut3 ==-1 and pos_debut2==-1:
            return ""
    pos_fin1=0
    pos_fin2=0
    pos_fin3=0
    if num_exo==173:
        for i in range (1,3):
            pos_fin1=data[10:].find('\exo',pos_fin1+1)
            pos_fin2=data[10:].find('\pb',pos_fin2+1)
            pos_fin3=data[10:].find('begin{exo}',pos_fin3+1)
    pos_fin1=data[10:].find('\exo',pos_fin1+1)
    pos_fin2=data[10:].find('\pb',pos_fin2+1)
    pos_fin3=data[10:].find('begin{exo}',pos_fin3+1)
    if pos_fin2==-1:
        pos_fin2=pos_fin1+1 
    if pos_fin3==-1:
        pos_fin3=pos_fin1+1
    if pos_fin1>pos_fin2 and pos_fin3>pos_fin2:
        return data[:pos_fin2+10]
    if pos_fin1>pos_fin3 and pos_fin2>pos_fin3:
        return data[:pos_fin3+10]
    if pos_fin1==-1:
        return data[:-14]
    postexotraite=data[:pos_fin1+10]
    debutit=postexotraite.find('exosd{')
    finit=postexotraite.find('}',debutit)
    if not debutit == -1:
        if not finit == -1 and not postexotraite[debutit+6:finit]=='':
            postexotraite=postexotraite[:debutit-1]+"Duree conseillee "+postexotraite[debutit+6:finit]+'$\\\\$'+postexotraite[finit+1:]
    debutit=postexotraite.find('exo{')
    finit=postexotraite.find('}',debutit)
    if not debutit == -1:
        if not finit == -1 and not postexotraite[debutit+6:finit]=='':
            postexotraite=postexotraite[:debutit-1]+postexotraite[debutit+4:finit]+'$\\\\$'+postexotraite[finit+1:]
    debutit=postexotraite.find('{')
    finit=postexotraite.find('}',debutit)
    if not debutit == -1:
        if not finit == -1 and not postexotraite[debutit+6:finit]=='':
            postexotraite=postexotraite[:debutit-1]+'//'+postexotraite[debutit+1:finit]+postexotraite[finit+1:]
    exotraite = "$\\textbf{Exercice "+str(num_exo1)+"}$"+"$\\\\$"+postexotraite.replace('%','')\
                .replace('-','').replace('\question','$\\\\Question :$').replace('\squestion','$\\\\Sous-question$')\
                .replace('\\RR','\\mathbb R').replace('\\ZZ','\\mathbb Z').replace('\\NN','\\mathbb N')\
                .replace('\\QQ','\\mathbb Q').replace('\\d','').replace('\\eps','\\epsilon').replace('\\epsilonilon','\\epsilon')\
                .replace('\\begin{enumerate}','').replace('\\end{enumerate}','').replace('\\item','$\\\\$').replace('[a)]','')\
                .replace('{\\trefle}','').replace('{\\coeur}','').replace('\\exo{}','').replace('\\exosd{}','').replace('\\begin{multicols}{2}','')\
                .replace('\\end{multicols}','').replace('{\\ccoeur}','').replace('{\\ttrefle}','').replace('\\section{Complexes}','')\
                .replace('\\begin{exo}{}{}','').replace('\\end{exo}','').replace('[(a)]','').replace('\\section{Equations différentielles}','')
    return exotraite
    
def get_exo_2(num_exo):
    num_exo=int(num_exo)
    num_exo1=num_exo
    data=open('./exos/exos.tex').read()
    if num_exo == -1:
        return data
    if num_exo>173:
        num_exo=num_exo+2
    if num_exo>205:
        num_exo=num_exo+1
    for i in range(1,num_exo+4):
        pos_debut1=data[10:].find('\exo')
        pos_debut2=data[10:].find('\pb')
        pos_debut3=data[10:].find('begin{exo}')
        if pos_debut2==-1:
            pos_debut2=pos_debut1+1
        if pos_debut3==-1:
            pos_debut3=pos_debut1+1
        if pos_debut1>pos_debut2 and pos_debut3>pos_debut2:
            data=data[pos_debut2+10:]
        if pos_debut2>pos_debut3 and pos_debut1>pos_debut3:
            data=data[pos_debut3+9:]
        if pos_debut3>pos_debut1 and pos_debut2>pos_debut1:
            data=data[pos_debut1+10:]
        if pos_debut1==-1 and pos_debut3 ==-1 and pos_debut2==-1:
            return ""
    pos_fin1=0
    pos_fin2=0
    pos_fin3=0
    if num_exo==173:
        for i in range (1,3):
            pos_fin1=data[10:].find('\exo',pos_fin1+1)
            pos_fin2=data[10:].find('\pb',pos_fin2+1)
            pos_fin3=data[10:].find('begin{exo}',pos_fin3+1)
    pos_fin1=data[10:].find('\exo',pos_fin1+1)
    pos_fin2=data[10:].find('\pb',pos_fin2+1)
    pos_fin3=data[10:].find('begin{exo}',pos_fin3+1)
    if pos_fin2==-1:
        pos_fin2=pos_fin1+1 
    if pos_fin3==-1:
        pos_fin3=pos_fin1+1
    if pos_fin1>pos_fin2 and pos_fin3>pos_fin2:
        return data[:pos_fin2+10]
    if pos_fin1>pos_fin3 and pos_fin2>pos_fin3:
        return data[:pos_fin3+10]
    if pos_fin1==-1:
        return data[:-14]
    postexotraite=data[:pos_fin1+10]
    exotraite="\\textbf{Exercice "+str(num_exo1)+"}"+postexotraite.replace('\\exo{}','').replace('\\exosd{}','')+'\\setcounter{qcounter}{0} \\setcounter{qscounter}{0}'
    return exotraite