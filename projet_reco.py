#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
from flask import Flask, redirect,url_for, render_template, request, flash
from pylti.flask import lti
import MySQLdb
from get_params import get_params
import xlrd
import json
from get_exo import get_exo, get_exo_2
from get_eleves import get_eleves
from datetime import datetime
from get_name import get_name
from get_id import get_id
from match_exo import match_exo
import mainAlgo.main as main

reload(sys)
sys.setdefaultencoding('utf8')
VERSION = '1.08'
UPLOAD_FOLDER='exos/'
ALLOWED_EXTENSIONS=set(['xlsx'])
ALLOWED_EXTENSIONS2=set(['tex'])
app = Flask(__name__)
algo=main.Main()
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config.from_object('config')





def error(exception=None):
    """ Page d'erreur """
    return render_template('error.html')


@app.route('/is_up', methods=['GET'])
def hello_world(lti=lti):
    """ Test pour debug de l'application

    :param lti: the `lti` object from `pylti`
    :return: simple page that indicates the request was processed by the lti
        provider
    """
    return render_template('up.html', lti=lti)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/lti/', methods=['GET', 'POST'])
@lti(request='initial', error=error, app=app)
def index(lti=lti):
    """ Page d'acceuil, permet d'authentifier l'utilisateur.

    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor() 
    cHandler.execute("SHOW TABLES LIKE 'mdl_comp_recommendation'")
    condition=cHandler.fetchall()
    if condition==():
        return redirect(url_for('upload_exo_2'))
    if not os.path.isfile('data.json'):
        get_params(lti)
    cours_id=lti.user_id[0]
    cHandler.execute("SELECT id_theme,theme FROM mdl_theme_recommendation WHERE cours_id=%s",cours_id)
    themes=cHandler.fetchall()
    for items in themes:
        algo.ajouterTheme(int(items[0]),items[1])
    cHandler.execute("SELECT id_savoir_faire, savoir_faire FROM mdl_comp_recommendation WHERE cours_id=%s",cours_id)
    comp=cHandler.fetchall()
    for items in comp:
        cHandler.execute("SELECT id_theme FROM mdl_comp_recommendation WHERE id_savoir_faire=%s",items[0])
        id_theme=cHandler.fetchall()
        if not id_theme==():
            algo.ajouterCompetence(int(items[0]),items[1],id_theme[0][0],[])
    with open('data.json') as data_file:    
        data = json.load(data_file)
    for studs in data["eleves"]:
        algo.ajouterEtudiant(studs['id'], studs['prenom'], studs['nom'], studs['comp'], studs['res'])
    i=0
    while not get_exo(i)=="" or i<256:
        text=get_exo(i)
        cHandler.execute("SELECT DISTINCT id_theme FROM mdl_exos_recommendation WHERE num_exo=%s",i)
        id_theme=cHandler.fetchall()
        cHandler.execute("SELECT DISTINCT m1.id_savoir_faire FROM mdl_exos_recommendation m1 JOIN mdl_comp_recommendation m2 ON m1.id_savoir_faire=m2.id_savoir_faire WHERE m1.num_exo=%s",i)
        id_comp=cHandler.fetchall()
        tab_id_theme=[]
        tab_id_comp=[]
        for ids in id_theme:
            tab_id_theme.append(int(ids[0]))
        for ids in id_comp:
            tab_id_comp.append(int(ids[0]))
        algo.ajouterExercice(i,text,"",tab_id_theme,tab_id_comp,{}, 1)
        i+=1
    return render_template('index.html', lti=lti)

@app.route('/index2', methods=['GET', 'POST'])
@lti(request='session', error=error, app=app)
def index2(lti=lti):
    """ Page d'acceuil2, permet de rediriger l'utilisateur.

    """
    return render_template('index.html', lti=lti)


@app.route('/index_staff', methods=['GET', 'POST'])
@lti(request='session', error=error, app=app)
def index_staff(lti=lti):
    """ Affiche le template staff.html

    :param lti: the `lti` object from `pylti`
    :return: the staff.html template rendered
    """
    return render_template('staff.html', lti=lti)

#Permet de restrindre les uploads à un format excel
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2

@app.route('/upload_exo_2', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def upload_exo_2(lti=lti):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser will
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.name='bdd_exos'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'bdd.xlsx'))
            return redirect(url_for('majDB2'))
        if file and not allowed_file(file.filename):
            flash('Mauvais format, les formats possibles sont : ' + str(ALLOWED_EXTENSIONS).split('set([')[-1].split('])')[0])
    return render_template('testupload.html', lti=lti)

@app.route('/upload_exo', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def upload_exo(lti=lti):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser will
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.name='bdd_exos'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'bdd.xlsx'))
            return redirect(url_for('majDB'))
        if file and not allowed_file(file.filename):
            flash('Mauvais format, les formats possibles sont : ' + str(ALLOWED_EXTENSIONS).split('set([')[-1].split('])')[0])
    return render_template('testupload.html', lti=lti)
    
@app.route('/maj_db', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def majDB(lti=lti):
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor() 
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_recommendation (num_exo integer, id_theme integer, id_savoir_faire integer, cours_id integer)")
    cHandler.execute("DELETE FROM mdl_exos_recommendation WHERE cours_id=%s",lti.user_id[0])
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_comp_recommendation (id_savoir_faire integer, savoir_faire text, id_theme integer, cours_id integer) ")  
    cHandler.execute("DELETE FROM mdl_comp_recommendation WHERE cours_id=%s",lti.user_id[0])
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_theme_recommendation (id_theme integer, theme text, cours_id integer) ")  
    cHandler.execute("DELETE FROM mdl_theme_recommendation WHERE cours_id=%s",lti.user_id[0])
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_eleves_recommendation (id_stud integer, id_exo integer, cours_id integer, date_created date, realised boolean) ")  
    # Open the workbook and define the worksheet
    book = xlrd.open_workbook("./exos/bdd.xlsx")
    sheets = book.sheet_names()
    sheet0 = book.sheet_by_name(sheets[0])
    sheet1 = book.sheet_by_name(sheets[1])
    sheet2 = book.sheet_by_name(sheets[2])
    sheet3 = book.sheet_by_name(sheets[3])
    # Get the cursor, which is used to traverse the database, line by line
    cursor = database.cursor()
    cours_id = lti.user_id[0]
    # Tableau pour stocker les différents savoirs faire associés aux exercices
    tab_sf=[]
    tab_sf.append([])
    tab_sft=[]
    tab_sft2=[]
    tab_sft2.append([])
    tab_sft.append([])
    tab_t=[]
    tab_t.append([])
    theme=[]
    #Trie les différents savoirs et les attache aux exercices concernés
    for r in range(1, sheet2.nrows):
        tab_sf.append([])
        tab_sf[int(sheet2.cell(r,0).value)].append(int(sheet2.cell(r,1).value))
    #Trie les savoir_faire et les attache à leur id
    for r in range(1,sheet3.nrows):
        tab_sft.append([])
        tab_sft[int(sheet3.cell(r,0).value)].append(sheet3.cell(r,2).value)
        tab_sft2.append([])
        tab_sft2[int(sheet3.cell(r,0).value)].append(sheet3.cell(r,1).value)
    #Associe les themes a leur id
    for r in range(1,sheet0.nrows):
        tab_t.append([])
        tab_t[int(sheet0.cell(r,1).value)].append(sheet0.cell(r,0).value)
    #Remplissage de la db
    for r in range(1,sheet1.nrows):
        theme = int(sheet1.cell(r,1).value)
        for j in range(0,len(tab_sf[r])):
            value=tab_sf[r][j]
            cursor.execute("INSERT INTO mdl_exos_recommendation (num_exo, id_savoir_faire, cours_id, id_theme) VALUES (%s,%s,%s,%s)", \
                       (r,value,cours_id,theme)) 
    for r in range(1,sheet0.nrows):
        for j in range(0,len(tab_t[r])):
            cursor.execute("INSERT INTO mdl_theme_recommendation (id_theme, theme, cours_id) VALUES (%s,%s,%s)",(r,tab_t[r][j].lower(),lti.user_id[0]))
    cursor.close()
    database.commit()
    database.close()
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cursor = database.cursor() 
    for r in range(1,sheet3.nrows):
       cursor.execute("SELECT DISTINCT id_theme FROM mdl_theme_recommendation WHERE theme=%s",tab_sft2[r][0])
       id_theme=cursor.fetchall()
       if not id_theme==():
           cursor.execute("INSERT INTO mdl_comp_recommendation (id_savoir_faire, savoir_faire, id_theme, cours_id) VALUES (%s,%s,%s,%s)",(r,tab_sft[r][0].lower(),id_theme[0][0],lti.user_id[0]))

    # Close the cursor
    cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()
    return render_template("upload_reussit.html")

@app.route('/maj_db_2', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def majDB2(lti=lti):
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor() 
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_recommendation (num_exo integer, id_theme integer, id_savoir_faire integer, cours_id integer)")
    cHandler.execute("DELETE FROM mdl_exos_recommendation WHERE cours_id=%s",lti.user_id[0])
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_comp_recommendation (id_savoir_faire integer, savoir_faire text, id_theme integer, cours_id integer) ")  
    cHandler.execute("DELETE FROM mdl_comp_recommendation WHERE cours_id=%s",lti.user_id[0])
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_theme_recommendation (id_theme integer, theme text, cours_id integer) ")  
    cHandler.execute("DELETE FROM mdl_theme_recommendation WHERE cours_id=%s",lti.user_id[0])
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_eleves_recommendation (id_stud integer, id_exo integer, cours_id integer, date_created date, realised boolean) ")  
    # Open the workbook and define the worksheet
    book = xlrd.open_workbook("./exos/bdd.xlsx")
    sheets = book.sheet_names()
    sheet0 = book.sheet_by_name(sheets[0])
    sheet1 = book.sheet_by_name(sheets[1])
    sheet2 = book.sheet_by_name(sheets[2])
    sheet3 = book.sheet_by_name(sheets[3])
    # Get the cursor, which is used to traverse the database, line by line
    cursor = database.cursor()
    cours_id = lti.user_id[0]
    # Tableau pour stocker les différents savoirs faire associés aux exercices
    tab_sf=[]
    tab_sf.append([])
    tab_sft=[]
    tab_sft2=[]
    tab_sft2.append([])
    tab_sft.append([])
    tab_t=[]
    tab_t.append([])
    theme=[]
    #Trie les différents savoirs et les attache aux exercices concernés
    for r in range(1, sheet2.nrows):
        tab_sf.append([])
        tab_sf[int(sheet2.cell(r,0).value)].append(int(sheet2.cell(r,1).value))
    #Trie les savoir_faire et les attache à leur id
    for r in range(1,sheet3.nrows):
        tab_sft.append([])
        tab_sft[int(sheet3.cell(r,0).value)].append(sheet3.cell(r,2).value)
        tab_sft2.append([])
        tab_sft2[int(sheet3.cell(r,0).value)].append(sheet3.cell(r,1).value)
    #Associe les themes a leur id
    for r in range(1,sheet0.nrows):
        tab_t.append([])
        tab_t[int(sheet0.cell(r,1).value)].append(sheet0.cell(r,0).value)
    #Remplissage de la db
    for r in range(1,sheet1.nrows):
        theme = int(sheet1.cell(r,1).value)
        for j in range(0,len(tab_sf[r])):
            value=tab_sf[r][j]
            cursor.execute("INSERT INTO mdl_exos_recommendation (num_exo, id_savoir_faire, cours_id, id_theme) VALUES (%s,%s,%s,%s)", \
                       (r,value,cours_id,theme)) 
    for r in range(1,sheet0.nrows):
        for j in range(0,len(tab_t[r])):
            cursor.execute("INSERT INTO mdl_theme_recommendation (id_theme, theme, cours_id) VALUES (%s,%s,%s)",(r,tab_t[r][j].lower(),lti.user_id[0]))
    cursor.close()
    database.commit()
    database.close()
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cursor = database.cursor() 
    for r in range(1,sheet3.nrows):
       cursor.execute("SELECT DISTINCT id_theme FROM mdl_theme_recommendation WHERE theme=%s",tab_sft2[r][0])
       id_theme=cursor.fetchall()
       if not id_theme==():
           cursor.execute("INSERT INTO mdl_comp_recommendation (id_savoir_faire, savoir_faire, id_theme, cours_id) VALUES (%s,%s,%s,%s)",(r,tab_sft[r][0].lower(),id_theme[0][0],lti.user_id[0]))

    # Close the cursor
    cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()
    return render_template("upload_reussit2.html")

@app.route('/up_latex', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def upload_latex(lti=lti):
    # L'utilisateur entre son fichier latex
    return render_template('up_latex.html',lti=lti)
    
@app.route('/latex', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def latex(lti=lti):
    data=request.files['file']
    if data == '':
        flash('Entrez un fichier latex (.tex)')
        return redirect(request.url)
    if data and allowed_file2(data.filename):
        data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'exos.tex'))
#        data=open('.\exos\exos.tex').read()
#        database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
#        cHandler = database.cursor() 
#        cours_id = lti.user_id
#        cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_recommendation_latex (fichier_latex blob, cours_id integer, exo_id integer)")
#        cHandler.execute("DELETE FROM mdl_exos_recommendation_latex WHERE cours_id=%s",lti.user_id)
#        cHandler.execute("INSERT INTO mdl_exos_recommendation_latex (fichier_latex, cours_id) VALUES (%s,%s)",(data,cours_id))
        return render_template('ok_latex.html',lti=lti)
    return render_template('up_latex.html',lti=lti)
    
@app.route('/see_competences', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def see_competences(lti=lti):
    # L'utilisateur tape le numero de l'exo dont il désir avoir les compétences
    return render_template('see_competences.html',lti=lti)
    

@app.route('/competences', methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def competences(lti=lti):
    # Contrôles sur le numéro de l'exo à faire : pas trop grand, si négatif
    data=request.form['numero_exo']
    if data == '':
            flash('Entrez un numero')
            return redirect(request.url)
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor() 
    cours_id = lti.user_id[0]
    cHandler.execute("SELECT DISTINCT id_savoir_faire FROM mdl_exos_recommendation WHERE num_exo=%s AND cours_id=%s",(data,cours_id))
    results=cHandler.fetchall()
    if results == ():
        flash('Entrez un numéro d\'éxercice valide')
        return render_template('see_competences.html')
    resultats=[]
    for items in results:
        cHandler.execute("SELECT savoir_faire FROM mdl_comp_recommendation WHERE id_savoir_faire=%s AND cours_id=%s",(items[0],cours_id))
        viv=cHandler.fetchall()
        resultats.append((viv[0][0].decode("latin1"),items))
    return render_template("competences.html",lti=lti, resultats=resultats,num=data)

@app.route('/see_exos', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def see_exos(lti=lti):
    # L'utilisateur tape le numero de l'exo dont il désire avoir les compétences
    return render_template('see_exos.html',lti=lti)

@app.route('/exos', methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def exos(lti=lti):
    # Contrôles sur le numéro de la competence à faire : pas trop grand, si négatif
    data1=request.form['numero_comp1']
    data2=request.form['numero_comp2']
    if data1 == '':
            flash('Entrez un numero dans la case 1 en priorité')
            return render_template('see_exos.html',lti=lti)
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor() 
    cours_id = lti.user_id[0]
    if data1 and data2=='':
        cHandler.execute("SELECT num_exo FROM mdl_exos_recommendation WHERE id_savoir_faire=%s AND cours_id = %s",(data1,cours_id))
        results=cHandler.fetchall()
        if not results == ():
            resultats=[]
            num_resultats=[]
            for items in results:
                resultats.append(get_exo(str(items[0])))
                num_resultats.append(str(items[0]))
            return render_template("exos.html",lti=lti, num_resultats=num_resultats, resultats=resultats,num1=data1)
        if results == ():
            flash('Une ou plusieures compétences sont invalides OU aucun exercie ne correspond aux compétences renseignées')
            return render_template('see_exos.html',lti=lti)
    if data1 and not data2=='':
        cHandler.execute("SELECT m1.num_exo FROM mdl_exos_recommendation m1 JOIN\
                         mdl_exos_recommendation m2 ON\
                         m1.num_exo = m2.num_exo AND m2.id_savoir_faire = %s WHERE \
                         m1.id_savoir_faire = %s AND m1.cours_id=%s",(data1,data2,cours_id))
        results=cHandler.fetchall()
        if not results == ():
            resultats=[]
            num_resultats=[]
            for items in results:
                resultats.append(get_exo(str(items[0])))
                num_resultats.append(str(items[0]))        
            return render_template("exos2.html",lti=lti, num_resultats=num_resultats, resultats=resultats,num1=data1, num2=data2)
        if results == ():
            flash('Une ou plusieures compétences sont invalides')
            return render_template('see_exos.html',lti=lti)
    return render_template('see_exos.html',lti=lti)
    
@app.route('/teacher',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def teachers_class(lti=lti):
	[coursename,results] = get_params(lti)
			
	return render_template('displayStuds2.html', results=results, coursename=coursename)
 
@app.route('/gen',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def gen(lti=lti):
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    c = database.cursor()
    cours_id=lti.user_id[0]
    c.execute('SELECT DISTINCT id_savoir_faire,savoir_faire FROM mdl_comp_recommendation WHERE cours_id=%s',cours_id)
    sf=c.fetchall()
    return render_template("gen.html",sf=sf)

@app.route('/gen_exo',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def gen_exo(lti=lti):
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor()
    res=get_eleves(lti)
    cours_id=lti.user_id[0]
    comp=request.form.getlist('comp')
    date=datetime.today().strftime('%Y-%m-%d')
#    cHandler.execute('SELECT * FROM mdl_exos_eleves_recommendation WHERE date_created>sysdate-6 AND cours_id=%s',cours_id)
#    will=cHandler.fetchall()
    will=[1]
    if not will == []:
        cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_eleves_recommendation (id_stud integer, id_exo integer, cours_id integer, date_created date, realised boolean) ")
#        cHandler.execute('DELETE * FROM mdl_exos_eleves_recommendation WHERE cours_id=%s AND realised=1',cours_id)
        for eleves in res:
            id_stud=eleves[0]
            exos=algo.genererFE(int(id_stud),map(int, comp),8)
            for exo in exos:
                if exo == None:
                    return render_template('no_exo.html')
                cHandler.execute("INSERT INTO mdl_exos_eleves_recommendation (id_stud, id_exo, cours_id,\
                date_created, realised) VALUES (%s,%s,%s,%s,0)",(id_stud,exo.nId,cours_id,date))
        # Close the cursor
        cHandler.close()
        # Commit the transaction
        database.commit()
        # Close the database connection
        database.close()
        return render_template('exosok.html')
    return render_template('not_yet.html')

@app.route('/select_stud',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def select_stud(lti=lti):
    studs=get_eleves(lti)
    return render_template('select_stud.html',studs=studs)

@app.route('/checkexo',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def checkexo(lti=lti):
    if request.method == 'POST':
        id_stud=get_id(request.form.get("nom"))
    else:
        id_stud=open('id_stud.txt')
        id_stud=id_stud.read()
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor()
    cHandler.execute('SELECT DISTINCT id_exo FROM mdl_exos_eleves_recommendation WHERE realised = 0 AND id_stud=%s',id_stud)
    exos=cHandler.fetchall()
    i=0
    results=[]
    for item in exos:
        new=[item,get_exo(item[0]),str(i)]
        results.append(new)
        i=i+1   
    return render_template('checkexo.html',results=results, namestud=get_name(id_stud)[0], id_stud=id_stud)    
    
@app.route('/val_exo',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def val_exos(lti=lti):
    if request.method == 'POST':
        id_stud=request.form.get("id_stud")
        nom=get_name(id_stud)
        cours_id=lti.user_id[0]
        database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
        cHandler = database.cursor()
        r=request.form.getlist("exo")
        cHandler.execute('SELECT DISTINCT id_exo FROM mdl_exos_eleves_recommendation WHERE id_stud=%s AND cours_id=%s AND realised=0',(id_stud,cours_id))
        exos=cHandler.fetchall()
        results=match_exo(r,exos)
        resultats=[]
        for items in results:
            resultats.append(get_exo(str(items)))
        return render_template('exos_val.html',resultats=resultats, num_resultats=results, nom=nom[0], id_stud=id_stud)
    return redirect(url_for('checkexo'))

@app.route('/send_exo',methods=['GET','POST'])
@lti(request='session', error=error,role = 'staff', app=app)
def send_exo(lti=lti):
    if request.method == 'POST':
        exo_id=request.form.get('exo_id')
        exo_id=exo_id.replace('[','')
        exo_id=exo_id.replace(']','')
        exo_id=exo_id.replace('L','')
        exo_id=exo_id.split(',')
        id_stud=request.form.get('id_stud')
        date=datetime.today().strftime('%Y-%m-%d')
        cours_id=lti.user_id[0]
        database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
        cHandler = database.cursor()
        cHandler.execute('DELETE FROM mdl_exos_eleves_recommendation WHERE id_stud=%s AND cours_id=%s',(id_stud,cours_id))
        for id_exo in exo_id:
            cHandler.execute("INSERT INTO mdl_exos_eleves_recommendation (id_stud, id_exo, cours_id,\
                date_created, realised) VALUES (%s,%s,%s,%s,0)",(id_stud,id_exo,cours_id,date))
        cHandler.close()
        database.commit()        
        database.close()    
        return render_template('exosok.html')
    else:
        return redirect(url_for('checkexo'))
        
@app.route('/get_my_exos',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def get_my_exos(lti=lti):
    [cours_id,id_stud]=lti.user_id
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor()
    cHandler.execute('SELECT DISTINCT id_exo FROM mdl_exos_eleves_recommendation WHERE id_stud=%s AND cours_id=%s AND realised=0',(id_stud,cours_id))
    exos=cHandler.fetchall()
    results=[]
    for items in exos:
        results.append(get_exo_2(items[0]))
    nom=get_name(id_stud)
    f=open('start.tex','r')
    string=f.read()
    f.close()
    for stuff in results:
        string+=stuff
    string+='\\end{document}'
    f=open('static\pdf\%s.tex' % id_stud,'w')
    f.write(string)
    f.close()
    os.system('pdflatex static/pdf/%s.tex' % id_stud)
    return render_template('get_my_exos.html',num_resultats=exos,nom=nom[0],idstud=id_stud)

@app.route('/corr',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def corr(lti=lti):
    studs=get_eleves(lti)
    id_stud=[]
    for items in studs:
        id_stud.append(items[0])
    return render_template('corr.html',studs=studs)

@app.route('/corr_exo',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def corr_exo(lti=lti):
    if request.method=='POST':
        text=request.form.get('nom')
        debutit=text.find('"')
        finit=text.find('"',debutit+1)
        id_stud=int(text[debutit+1:finit])
        database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
        cHandler = database.cursor()
        cHandler.execute('SELECT DISTINCT id_exo FROM mdl_exos_eleves_recommendation WHERE id_stud=%s',id_stud)
        exos=cHandler.fetchall()
        nom=get_name(id_stud)
        return render_template('corr_exo.html',exos=exos,nom=nom,id_stud=id_stud)

@app.route('/corr_exo_eff',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def corr_exo_eff(lti=lti):
    if request.method=='POST':
        acquis=request.form.getlist("exo")
        exos=request.form.get('id_exos')
        id_stud=request.form.get('id_stud')
    tab_stud={}
    [cours_id,q]=lti.user_id
    exos=str(exos)
    exoss=[int(s) for s in exos.split() if s.isdigit()]
    exos=exos.replace('(','')
    exos=exos.replace(')','')
    exos=exos.replace(",","")
    exos=exos.replace('L','')
    exoss=[int(s) for s in exos.split() if s.isdigit()]
    j=0
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor()
    for items in exoss:
        cHandler.execute('DELETE FROM mdl_exos_eleves_recommendation WHERE id_exo=%s \
        AND id_stud=%s AND cours_id=%s',(items,id_stud,cours_id))
    for i in exoss:
        if acquis[j]=='Acquis':
            tab_stud[i]=1
        if acquis[j]=='Non acquis':
            tab_stud[i]=0
        if acquis[j]=="En cours d'acquisition":
            tab_stud[i]=0.5
        j+=1
    with open('data.json','r') as data_file:
        data = json.load(data_file)
    for studs in data['eleves']:
        if studs['id']==int(id_stud):
            studs['res'].update(tab_stud)
            algo.etudiants[int(id_stud)].majResultat(tab_stud)  
    algo.actualiserNiveaux(int(id_stud))
    for studs in data['eleves']:
        if studs['id']==int(id_stud):
            studs['comp']=algo.etudiants[int(id_stud)].niveauxCompetences
            studs['res']={}
    results=json.dumps(data,indent=4)
    with open('data.json','w') as data_file:
        data_file.write(results)
    
    return render_template('merci_corr.html')

   
@app.route('/test',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def test(lti=lti):
    algo.actualiserNiveaux(int(3))
    return render_template('testexo.html',res=algo.etudiants[3].niveauxCompetences)
    
    
def set_debugging():    
    """ Debuggage du logging

    """
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

set_debugging()

if __name__ == '__main__':
    """
    For if you want to run the flask development server
    directly
    """
    port = int(os.environ.get("FLASK_LTI_PORT", 5000))
    host = os.environ.get("FLASK_LTI_HOST", "localhost")
    app.run(debug=True, host=host, port=port)
