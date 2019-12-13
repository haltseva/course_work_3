from app import db
from flask_login import UserMixin
from app import login

db.Model.metadata.reflect(bind=db.engine, schema='ka7603')

class User(UserMixin, db.Model):
    '''id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))'''

    __table__ = db.Model.metadata.tables['ka7603.Customer']

    def check_password(self, password):
        return True if self.Password==password else False

    def __repr__(self):
        return f'<User {self.FirstName} {self.email}>'

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_id(self):
           return (self.cid)

class Product(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.Product']

    def __repr__(self):
        return str({"ID": self.ProductID,"name":self.ProductName})

class Color(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.Color']

    def __repr__(self):
        return str({"ID": self.ColorID,"name":self.Name})

class Deteis(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.OrdDetails']

    def __repr__(self):
        return str({"ID": self.OrdID,"name":self.ProductID})

class Cart(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.Cart']

    def __repr__(self):
        return str({"ID": self.OrdID,"name":self.CustomerID})

class Ord(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.Ord']

    def __repr__(self):
        return str({"ID": self.OrdID,"name":self.CustomerID})

class OrdDetails(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.OrdDetails']

    def __repr__(self):
        return str({"ID": self.id,"Ord":self.OrdID})

class Categorie(db.Model):

    __table__ = db.Model.metadata.tables['ka7603.Categorie']

    def __repr__(self):
        return str({"ID": self.CategorieID,"Name":self.Name})