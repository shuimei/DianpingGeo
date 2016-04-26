import sqlite3
import json
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, render_template, flash, jsonify
# from flask.ext import restful
import pandas as pd


# configuration
DATABASE = r"P:\files\codes\flask-proj\dianpingGeo\store.db"
DEBUG = True
SECRET_KEY = 'SECRET_KEY'
USERNAME = 'admin'
PASSWORD = 'default'

# create application
app = Flask(__name__)
app.config.from_object(__name__)

fields = ('id', 'location', 'region', 'category', 'subcategory', 'address', 'name', 'lng', 'lat', 'confidence')


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    return render_template('index/main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/_eval_numbers')
def eval_numbers():
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=str)
    method = request.args.get('method', '+', type=str)
    return jsonify(result=eval(a + method + b))


@app.route('/_id')
def query_id():
    id = request.args.get('id', 0, type=str)
    query = g.db.execute("select * from store where id=%s;" % id)
    record = query.fetchall()[0]
    return jsonify(rid=record[0],
                   locaton=record[1],
                   region=record[2],
                   category=record[3],
                   subcategory=record[4],
                   address=record[5],
                   name=record[6],
                   lng=record[7],
                   lat=record[8],
                   confidence=record[9],
                   )


@app.route('/testj')
def test():
    return render_template('test.html')


@app.route('/templates/bootstrap_template')
def templates():
    return render_template('bootstrap_template.html')


@app.route('/map')
def get_map():
    return render_template('map.html')


@app.route('/baidumap')
def get_baidumap():
    return render_template('baidumap.html')


@app.route('/leaflet')
def get_leaflet():
    return render_template('leaflet.html')


@app.route('/_subcategory')
def query_subcategory():
    subcategory = request.args.get('subcategory', 0, type=str)
    query = g.db.execute("select * from store where subcategory='%s';" % subcategory)
    records = query.fetchall()
    table_fields = fields
    subcat_table = pd.DataFrame(records, columns=table_fields)
    return subcat_table.to_json().encode('utf-8')


@app.route('/_like_subcategory')
def query_like_subcategory():
    like_subcategory = request.args.get('like_subcategory', 0, type=str)
    query = g.db.execute("select * from store where name like'%{0}%';".format(like_subcategory))
    records = query.fetchall()
    table_fields = fields
    like_subcategory_table = pd.DataFrame(records, columns=table_fields)
    return like_subcategory_table.to_json().encode('utf-8')


@app.route('/_category')
def query_category():
    category = request.args.get('category', 0, type=str)
    query = g.db.execute("select * from store where category='%s';" % category)
    records = query.fetchall()
    table_fields = fields
    subcat_table = pd.DataFrame(records, columns=table_fields)
    return subcat_table.to_json().encode('utf-8')


@app.route('/_like_category')
def query_like_category():
    like_category = request.args.get('like_category', 0, type=str)
    query = g.db.execute("select * from store where name like'%{0}%';".format(like_category))
    records = query.fetchall()
    table_fields = fields
    like_category_table = pd.DataFrame(records, columns=table_fields)
    return like_category_table.to_json().encode('utf-8')


@app.route('/_name')
def query_name():
    name = request.args.get('name', 0, type=str)
    query = g.db.execute("select * from store where name='%s';" % name)
    records = query.fetchall()
    table_fields = fields
    name_table = pd.DataFrame(records, columns=table_fields)
    return name_table.to_json().encode('utf-8')


@app.route('/_like_name')
def query_like_name():
    like_name = request.args.get('like_name', 0, type=str)
    query = g.db.execute("select * from store where name like'%{0}%';".format(like_name))
    records = query.fetchall()
    table_fields = fields
    like_name_table = pd.DataFrame(records, columns=table_fields)
    return like_name_table.to_json().encode('utf-8')


@app.route('/_region')
def query_region():
    region = request.args.get('region', 0, type=str)
    query = g.db.execute("select * from store where region='%s';" % region)
    records = query.fetchall()
    table_fields = fields
    region_table = pd.DataFrame(records, columns=table_fields)
    return region_table.to_json().encode('utf-8')


@app.route('/_location')
def query_location():
    location = request.args.get('location', 0, type=str)
    query = g.db.execute("select * from store where location='%s';" % location)
    records = query.fetchall()
    table_fields = fields
    location_table = pd.DataFrame(records, columns=table_fields)
    return location_table.to_json().encode('utf-8')


@app.route('/drawing')
def charts():
    return render_template('charts.html')


@app.route('/stats/group_by_region')
def group_by_region():
    store = pd.read_sql("select * from store;", g.db)
    regions = store.groupby(['region']).count()
    region = store['region'].unique()
    counts = list(regions['id'])
    c = []
    for i, j in enumerate(region):
        c.append({'name': j, 'value': str(counts[i])})
    return json.dumps(c)


@app.route('/stats/group_by_category')
def group_by_category():
    store = pd.read_sql("select * from store;", g.db)
    categories = store.groupby(['category']).count()
    categorie = store['category'].unique()
    counts = list(categories['id'])
    c = []
    for i, j in enumerate(categorie):
        c.append({'name': j, 'value': str(counts[i])})
    return json.dumps(c)


if __name__ == '__main__':
    app.run()
