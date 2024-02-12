from flask import render_template
from core import app
from core.models import Item
from flask_login import current_user

@app.route("/catalog", methods=['GET'])
def catalog():
    items = Item.query.all()
    return render_template('catalog.html',
                           title='catalog',
                           items=items, 
                           current_user_username=current_user.is_authenticated)