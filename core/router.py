from flask import Flask,render_template,url_for, flash, redirect,request
from datetime import date
import datetime
from sqlalchemy import text,update
from core.forms import LoginForm,RegistrationForm,addItemForm,SearchItemForm
from core import app, db, login_manager
from core.models import User,Item,Bill
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
flag=0

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

@app.route('/',methods=['GET', 'POST'])
@app.route("/about")
def about():
    return render_template('about.html',
                           title='about', 
                           current_user_username=current_user.is_authenticated)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            if user.is_admin:
                return redirect(url_for('admin'))
        return redirect(url_for('login'))
    return render_template('login.html', form=form, current_user_username=current_user.is_authenticated)

@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method=="POST":
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=form.password.data,
                    is_admin=True if User.query.count() == 0 else False)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='register',
                           form=form, 
                           current_user_username=current_user.is_authenticated)

@app.route("/bill",methods=['GET']) 
def bill():
    bill = Bill.query.all()
    return render_template('bill.html',
                           title='home', 
                           bill=bill, 
                           current_user_username=current_user.is_authenticated)
    
@app.route("/items",methods=['GET', 'POST'])
def items():
    form = SearchItemForm()
    items=Item.query.filter(Item.quantity!=0)
    sort_price = request.args.get('sortPrice')
    if request.method == 'POST':
        print(form.search.data)
        items = Item.query.filter(form.search.data==Item.item_name).all()
        print(items)
        return render_template('items.html',
                                title='items', 
                                items=items, 
                                current_user_username=current_user.is_authenticated,
                                form=form)
    if sort_price:
        if sort_price == 'asc':
            items = Item.query.filter(Item.quantity!=0).order_by(Item.price.asc()).all()
        elif sort_price == 'desc':
            items = Item.query.filter(Item.quantity!=0).order_by(Item.price.desc()).all()
    return render_template('items.html',
                           title='items',
                           items=items,
                           current_user_username=current_user.is_authenticated, 
                           form=form)
@app.route("/expired")
def expired():
    items=Item.query.filter(text(":val")>Item.exp_date).params(val=datetime.datetime.now())
    return render_template('expired.html',
                           title='expired',
                           items=items, 
                           current_user_username=current_user.is_authenticated)
@app.route("/outOfStock")
def outOfStock():
    items=Item.query.filter(Item.quantity==0)
    return render_template('outOfStock.html',
                           title='outOfStock',
                           items=items, 
                           current_user_username=current_user.is_authenticated)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/admin",methods=['GET'])
@admin_required
@login_required
def admin():
    return render_template('admin.html',
                           title='admin', 
                           current_user_username=current_user.is_authenticated)

@app.route("/admin/addItem",methods=['GET', 'POST'])
@admin_required
@login_required
def editItems():
    form=addItemForm()
    items=Item.query.all()
    itemupd=Item.query.all()
    delete_item_id = request.args.get('deleteItem')
    if delete_item_id:
        print(delete_item_id)
        for item in itemupd:
            print(item.id)
            if int(item.id) == int(delete_item_id):
                db.session.delete(item)
                db.session.commit()
                flash('Препарат удален')
                return redirect(url_for('editItems'))

    if request.method=="POST":

        name=request.form['itemName']
        q=request.form['quantity']
        for i in itemupd:
            if i.item_name == name:
                stmt = update(Item).where(Item.item_name == name).values(quantity = q+Item.quantity)
                db.session.execute(stmt)
                db.session.commit()
                global flag
                flag=1

        if flag==0:
            items = Item.query.all()
            addd = Item(item_name=form.itemName.data,
                       pkd_date=form.pkdDate.data, 
                       exp_date=form.expDate.data, 
                       quantity=form.quantity.data, 
                       price=form.price.data)
            db.session.add(addd)
            db.session.commit()
        return redirect(url_for('editItems'))
    return render_template('admin_additem.html',title='addItem',form=form,items=items)
