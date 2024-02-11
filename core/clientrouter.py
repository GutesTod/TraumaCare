from flask import render_template
from core import app
from flask_login import current_user

@app.route("/catalog", methods=['GET'])
def catalog():
    return render_template('catalog.html',
                           title='catalog', 
                           current_user_username=current_user.is_authenticated)