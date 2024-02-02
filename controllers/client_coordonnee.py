#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    utilisateur=[]

    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()
    print(utilisateur)

    sql = '''
    SELECT *, nom_adresse as nom
    FROM adresse
    JOIN habite ON adresse.id_adresse = habite.adresse_id
    WHERE utilisateur_id = %s 
    '''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                         #  , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT *
    FROM utilisateur
    WHERE id_utilisateur = %s
    '''
    mycursor.execute(sql,id_client)
    utilisateur=mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')
    utilisateur = []

    sql = '''
    SELECT *
    FROM utilisateur
    WHERE (login = %s OR nom = %s OR email = %s) AND id_utilisateur != %s
    '''
    tuple = (nom,login,email,id_client)
    mycursor.execute(sql,tuple)

    user = mycursor.fetchone()
    if user:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               ,utilisateur=utilisateur
                               )
    
    sql = '''
    UPDATE utilisateur
    SET nom = %s, login = %s, email = %s
    WHERE id_utilisateur = %s;
    '''
    tuple = (nom,login,email,id_client)
    mycursor.execute(sql,tuple)

    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    sql = '''
    DELETE FROM habite
    WHERE adresse_id = %s
    '''

    mycursor.execute(sql,id_adresse)
    get_db().commit()

    sql = '''
    DELETE FROM adresse
    WHERE id_adresse = %s
    '''

    mycursor.execute(sql,id_adresse)
    get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT *
    FROM adresse
    JOIN habite ON adresse.id_adresse = habite.adresse_id
    JOIN utilisateur ON habite.utilisateur_id = utilisateur.id_utilisateur
    WHERE utilisateur_id = %s
    '''

    mycursor.execute(sql,id_client)
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    sql = '''
    INSERT INTO adresse(nom_adresse,code_postal,ville,rue,valide)
    VALUES(%s,%s,%s,%s,'1');
    '''
    tuple = (nom,rue,code_postal,ville)
    mycursor.execute(sql,tuple)
    get_db().commit()

    
    sql = '''
    INSERT INTO habite (utilisateur_id,adresse_id)
    VALUES(%s,(SELECT MAX(id_adresse) FROM adresse));
    '''

    mycursor.execute(sql,id_client)
    get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    return render_template('/client/coordonnee/edit_adresse.html'
                           # ,utilisateur=utilisateur
                           # ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    return redirect('/client/coordonnee/show')
