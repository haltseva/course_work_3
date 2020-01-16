# -*- coding: utf-8 -*-
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrateForm, BuyForm, SortForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, db, Cart, Product, Ord, OrdDetails


@app.route('/')
@app.route('/index')
def index():
   
    products = db.session.execute(f'''
        SELECT DISTINCT *
        FROM Product
        ORDER BY RAND() LIMIT 3
    ''').fetchall()
    num=0
    
    if current_user.is_authenticated:
        UserID = current_user.cid
        count=db.session.execute(f'''
            SELECT DISTINCT COUNT(*)
            FROM Cart
            WHERE CustomerID='{UserID}'
        ''').fetchall()
        num=count[0]
    return render_template('index.html', title='Главная', products=products, num=num)

@app.route('/catalog/<start>', strict_slashes=False, methods=['GET', 'POST'] )
def catalog(start):
    
    num=0
    if start=='0':
        products = db.session.execute(f'''
            SELECT DISTINCT *
            FROM Product
            ORDER BY NameProduct
        ''').fetchall()
        categories =db.session.execute(f'''
            SELECT DISTINCT *
            FROM Categorie
        ''').fetchall()

    else:
        products = db.session.execute(f'''
            SELECT DISTINCT *
            FROM Product
            WHERE CategorieID LIKE '{start}%' 
            ORDER BY NameProduct
        ''').fetchall()
        categories =db.session.execute(f'''
            SELECT DISTINCT *
            FROM Categorie
            WHERE CategorieID LIKE '{start}%' 
        ''').fetchall()

    form = SortForm()
    if form.validate_on_submit():
        sort=form.sort.data
        print(sort)
        if(sort=='2'):
            if start=='0':
                products = db.session.execute(f'''
                    SELECT DISTINCT *
                    FROM Product
                    ORDER BY Price ASC
                ''').fetchall()
            else:
                products = db.session.execute(f'''
                    SELECT DISTINCT *
                    FROM Product
                    WHERE CategorieID LIKE '{start}%' 
                    ORDER BY Price ASC
                ''').fetchall()
        if(sort=='3'):
            if start=='0':
                products = db.session.execute(f'''
                    SELECT DISTINCT *
                    FROM Product
                    ORDER BY Price DESC
                ''').fetchall()
            else:
                products = db.session.execute(f'''
                    SELECT DISTINCT *
                    FROM Product
                    WHERE CategorieID LIKE '{start}%' 
                    ORDER BY Price DESC
                ''').fetchall() 



    if current_user.is_authenticated:
        UserID = current_user.cid
        count=db.session.execute(f'''
            SELECT DISTINCT COUNT(*)
            FROM Cart
            WHERE CustomerID='{UserID}'
        ''').fetchall()
        num=count[0]

    return render_template('catalog.html', title='Каталог', products=products, categories=categories, form=form, num=num)


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
    
    num=0
    form = BuyForm()
 
    if form.validate_on_submit():
        if current_user.is_authenticated:
            UserID = current_user.cid
            cart = Cart(CustomerID=UserID, ColorID=color_choose, Amont=form.amont.data)
            db.session.add(cart)
            db.session.commit()
          
            return redirect(url_for('catalog', start='0'))
        else:
            return redirect(url_for('login'))

    if current_user.is_authenticated:
        UserID = current_user.cid
        count=db.session.execute(f'''
            SELECT DISTINCT COUNT(*)
            FROM Cart
            WHERE CustomerID='{UserID}'
        ''').fetchall()
        num=count[0]


    return render_template('prod_page.html', product=product, title='Товар', colors=colors, color1=color1, color_choose=color_choose, form=form, num=num)


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
        count=0
        for pr in products:
            totalPrice += pr[6]
            count += 1

        return render_template('shopcart.html',title='Корзина товаров', products=products, totalPrice=totalPrice, num=count, count=count)
    else:
        return redirect(url_for('login'))

@app.route('/checkout',methods=['GET', 'POST'])
def checkout():
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
    prod = db.engine.execute(f'''
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

    item = Ord(CustomerID=UserID, TotalPrice=totalPrice)
    db.session.add(item)
    db.session.commit()
    MyOrd=db.engine.execute(f'''
    SELECT DISTINCT *
    FROM Ord
    WHERE CustomerID='{UserID}' 
    ORDER BY OrdID desc
    LIMIT 1
    ''').fetchone() 
   
    for pr in products:
        detail = OrdDetails(OrdID=MyOrd[0], ProductID=pr[7], Amont=pr[4], ColorID=pr[1])
        db.session.add(detail)
        db.session.commit()
        item = Cart.query.filter_by(OrdID=pr[0]).first()   
        db.session.delete(item)
        db.session.commit()
  
    return render_template('checkout.html', title='Подтверждение заказа', prod=prod, MyOrd=MyOrd, num='0')

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
    return render_template('login.html', title='Войти', form=form, num='0')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrateForm()
    if form.validate_on_submit():
        user = User(FirstName=form.name.data, email=form.email.data, Password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form, num='0')



