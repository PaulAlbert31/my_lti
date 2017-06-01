#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import MySQLdb

def get_name(stud_id):
    myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = myDB.cursor()
    results=[]
    if type(stud_id)==int:
        cHandler.execute("SELECT firstname, lastname FROM mdl_user WHERE id=%s",stud_id)
        res = cHandler.fetchall()[0]
        return res
    for ids in stud_id:
        cHandler.execute("SELECT firstname, lastname FROM mdl_user WHERE id=%s",ids)
        res = cHandler.fetchall()
        results.append(res[0])
    return results