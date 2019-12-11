# -*- coding: utf-8 -*-
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, BuyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, db, Cart, Product


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/catalog/<start>', strict_slashes=False)
def catalog(start):
    if start=='0':
        products = db.session.execute(f'''
        SELECT DISTINCT *
        FROM Product
    ''').fetchall()

    else:
        products = db.session.execute(f'''
            SELECT DISTINCT *
            FROM Product
            WHERE CategorieID LIKE '{start}%' 
        ''').fetchall()
    return render_template('catalog.html', title='Home', products=products)


@app.route('/prod/<ProductID>', strict_slashes=False, methods=['GET', 'POST'] )
def prod(ProductID):
    
    product = db.engine.execute(f'''
        SELECT DISTINCT *
        FROM Product
        WHERE ProductID='{ProductID}'
    ''').fetchall()

    color1 = db.engine.execute(f'''
        SELECT DISTINCT *
        FROM Color
        WHERE ProductID='{ProductID}'
        LIMIT 1
    ''').fetchall()

    color_choose = request.args.get('color', color1[0].ColorID, int)

    colors = db.engine.execute(f'''
        SELECT DISTINCT *
        FROM Color
        WHERE ProductID='{ProductID}'
    ''').fetchall()

    form = BuyForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            UserID = current_user.cid
            cart = Cart(CustomerID=UserID, ColorID=color_choose)
            db.session.add(cart)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('prod_page.html', product=product, colors=colors, color1=color1, color_choose=color_choose, form=form)

@app.route("/cart",methods=['GET', 'POST'])
def cart():
    if current_user.is_authenticated:
          
        UserID = current_user.cid
        products = db.engine.execute(f'''
        SELECT DISTINCT o.OrdID, o.ColorId, p.NameProduct, c.Name as Color ,o.Amont, o.CustomerID,
        o.Amont * p.Price as Price, p.ProductID
        FROM Cart o join Color c 
        ON (o.ColorID = c.ColorID)
        LEFT JOIN Product p 
        ON (p.ProductID = c.ProductID)
        WHERE o.CustomerID='{UserID}' 
        ''').fetchall()  

        totalPrice = 0
        for pr in products:
            totalPrice += pr[6]
        return render_template('shopcart.html', products=products, totalPrice=totalPrice)
    else:
        return redirect(url_for('login'))
    

@app.route("/removeFromCart/<ID>", strict_slashes=False, methods=['GET', 'POST'])
def removeFromCart(ID):
    if current_user.is_authenticated:

        # db.engine.execute(f'''
        # DELETE FROM Ord
        # WHERE OrdID='{ID}' 
        # ''').fetchall()  

        item = Cart.query.filter_by(OrdID=ID).first()   
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('login'))
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(FirstName=form.name.data, email=form.email.data, Password=form.password.data, phone=form.phone.data, birthday=form.birthday.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



