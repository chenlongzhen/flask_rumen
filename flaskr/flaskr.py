import os
import sqlite3

from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, logging, json, jsonify)

from raven.contrib.flask import Sentry


#sentry = Sentry()
from stock.stock1 import getStock


def create_app():
    app = Flask(__name__)
    #sentry.init_app(app, dsn='http://localhost:9000/1', logging=True,
    #                level=logging.ERROR,
    #                logging_exclusions=("logger1", "logger2"))
    return app

app = create_app() # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    USERNAME='admin',
    PASSWORD='default'
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)




# funcs

def connect_db():
    """Connects to the specific database."""

    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()

    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""

    init_db()
    print('Initialized the database.')

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries = entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

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
            app.logger.info("{} logging in!".format(request.form['username']))
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/kchart',methods=["GET"])
#@app.route('/echarts')
def echarts():
    app.logger.debug("in echarts func!")
    #dateData, histData = getStock()
    #datas = {
    #    "stockid":"sz",
    #    "dateData": dateData,
    #    "histData": histData
    #}
    stockData = getStock()
    datas = {
        "stockData" : stockData
    }

    #app.logger.debug(datas)
    #return jsonify(datas)
    #return render_template("k1.html", datas= json.dumps(datas))
    return render_template("kchart.html",datas = json.dumps(datas))



@app.route( "/get_kchart", methods = [ "POST", "GET" ] )
def test():
    if request.method == "POST":
        stockname = request.form.get( "stockId", "null" )
        stockData = getStock(stockname)
        datas = {
            "stockname" : stockname,
            "stockData" : stockData
        }

        app.logger.debug(jsonify(datas))
    #return jsonify(datas)

        return jsonify(datas)
    else:
        return render_template("get_kchart.html")

