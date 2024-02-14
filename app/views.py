import json
import time
from app import app
from app.config import *
from flask import render_template, json, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from app.common_utils.database import transaction, get_value_by_field

app.config.from_pyfile('config.py')

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/showProfile')
def showProfile():
    return render_template('profile.html')

@app.route('/signUp',methods=['POST'])
def signUp():# read the posted values from the UI
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        created_time = round(time.time() * 1000)

        app.logger.info(_name)
        app.logger.info(_email)
        app.logger.info(_password)

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            with transaction() as session:
                app.logger.info('Opened session')
                _hashed_password = generate_password_hash(_password)
                result = session.execute(text("SELECT 1 FROM webapp.app_users WHERE user_name = '{p_name}' AND user_email = '{p_email}'".format(
                                p_name=_name, 
                                p_email=_email)))
                
                app.logger.info("SELECT 1 FROM webapp.app_users WHERE user_name = '{p_name}' AND user_email = '{p_email}'".format(
                                p_name=_name, 
                                p_email=_email))


                data = result.fetchall()

                if len(data) == 0:
                    app.logger.info(f"Queried data empty : {len(data) == 0}")
                    result = session.execute(text("INSERT INTO webapp.app_users (user_name, user_email, user_password, created_time, updated_time) \
                                                    VALUES ('{p_name}', '{p_email}', '{p_password}', {p_created_time}, {p_updated_time});".format(
                                p_name= _name, 
                                p_email= _email,
                                p_password= _hashed_password,
                                p_created_time= created_time,
                                p_updated_time= created_time
                                )))
                    app.logger.info(f"User created successfully: {created_time}")
                    return json.dumps({'message':'User created successfully !'})
                else:
                    flash('User already exists')
                    return redirect('/showSignUp')
        else:
            flash('Enter the required fields')
            return redirect('/showSignUp')
    except Exception as e:
        app.logger.error(json.dumps({'error':str(e)}))
        return redirect('/showSignUp')
        
@app.route('/signIn', methods=['POST'])
def signIn():# read the posted values from the UI
    try:
        _name_or_email = request.form['inputNameorEmail']
        _password = request.form['inputPassword']
        created_time = round(time.time() * 1000)

        app.logger.info(_name_or_email)
        app.logger.info(_password)

        # validate the received values
        if _name_or_email and _password:
            # All Good, let's call MySQL
            with transaction() as session:
                app.logger.info('Opened session')
                result = session.execute(text("SELECT * FROM webapp.app_users WHERE user_name = '{_name_or_email}' OR user_email = '{_name_or_email}'".format(
                                _name_or_email=_name_or_email)))
                
                app.logger.info("SELECT * FROM webapp.app_users WHERE user_name = '{_name_or_email}' OR user_email = '{_name_or_email}'".format(
                                _name_or_email=_name_or_email))

                data = result.fetchall()

                app.logger.info(data)

                if len(data) == 0 or not check_password_hash(get_value_by_field(data[0], 'user_password'), _password):
                    app.logger.info(f"Queried data empty : {len(data) == 0}")
                    flash('Please check your login details and try again.')
                    return redirect('/showSignIn')
                else:
                    id = get_value_by_field(data[0], 'user_id')
                    app.logger.info(f"User id: {id}")
                    result = session.execute(text("UPDATE webapp.app_users \
                                                SET latest_signed_in_time = {p_latest_signed_in_time} \
                                                WHERE user_id = {id};".format(
                                            id= id, 
                                            p_latest_signed_in_time= created_time,
                                            )
                                        )
                                    )
                    app.logger.info(f"User latest_signed_in_time: {created_time}")
                    return redirect('/showProfile')
        else:
            flash('Enter the required fields')
            return redirect('/showSignIn')
    except Exception as e:
        app.logger.error(json.dumps({'error':str(e)}))
        return redirect('/showSignIn')