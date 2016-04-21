from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Item

from flask import session as login_session
import random, string


#Connect to Database and create database session
engine = create_engine('sqlite:///catalogitemwithuser.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']

#Show all categories
@app.route('/')
@app.route('/catalog/')
def showCatalogs():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    items_with_catalog = session.query(Item,Catalog).join(Catalog).order_by(desc(Item.inserted)).limit(9).all()
    return render_template('catalogs.html', catalogs = catalogs, items_with_catalog = items_with_catalog)

#Show a catalog
@app.route('/catalog/<string:cat_name>/items/')
def showCatalog(cat_name):
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    catalog = session.query(Catalog).filter_by(name=cat_name).one()
    items_query = session.query(Item).filter_by(cat_id = catalog.id)
    items = items_query.all()
    count = items_query.count()
    return render_template('items.html', items = items, catalogs = catalogs, catalog = catalog, count = count)

#Show a catalog
@app.route('/catalog/<string:cat_name>/<string:item_name>/')
def showItem(cat_name, item_name):
    catalog = session.query(Catalog).filter_by(name=cat_name).one()
    item = session.query(Item).filter_by(cat_id = catalog.id).filter_by(title = item_name).one()
    return render_template('itemdetails.html', item = item)

@app.route('/catalog/new/', methods=['GET','POST'])
def newCatalog():
    if request.method == 'POST':
        newCatalog = Catalog(name = request.form['name'])
        session.add(newCatalog)
        flash('New Catalog %s successfully created!' % newCatalog.name)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html');

@app.route('/catalog/<int:cat_id>/edit', methods=['GET','POST'])
def editCatalog(cat_id):
    if request.method == 'POST':
        editedCatalog = session.query(Catalog).filter_by(id=cat_id).one()
        editedCatalog.name = request.form['name']
        session.add(editedCatalog)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('editCatalog.html')

@app.route('/catalog/<int:cat_id>/delete', methods=['GET','POST'])
def deleteCatalog(cat_id):
    catalogToDelete = session.query(Catalog).filter_by(id = cat_id).one()
    if request.method == 'POST':
        session.delete(catalogToDelete)
        session.commit()
        return redirect(url_for('showCatalogs', cat_id = cat_id))
    else:
        return render_template('deleteCatalog.html', catalog = catalogToDelete)
    #return 'deleteCatalog blank'

@app.route('/catalog/<int:cat_id>/item/new', methods=['GET','POST'])
def addItem(cat_id):
    return 'addItem blank'


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)