import flask, codecs, psycopg2, os, json
from ..data import users

app = flask.Flask(__name__)

if os.environ['TWILIO_ACCOUNT'].startswith('AC'):
    app.config['twilio_account'] = users.TwilioAccount(
        sid = os.environ.get('TWILIO_SID', ''),
        secret = os.environ.get('TWILIO_SECRET', ''),
        account = os.environ.get('TWILIO_ACCOUNT', ''),
        number = os.environ.get('TWILIO_NUMBER', '')
        )
else:
    app.config['twilio_account'] = users.TwilioAccount(
        sid = codecs.decode(os.environ.get('TWILIO_SID', ''), 'rot13'),
        secret = codecs.decode(os.environ.get('TWILIO_SECRET', ''), 'rot13'),
        account = codecs.decode(os.environ.get('TWILIO_ACCOUNT', ''), 'rot13'),
        number = os.environ.get('TWILIO_NUMBER', '')
        )

@app.route('/')
def get_index():
    return flask.render_template('index.html')

@app.route('/about')
def get_about():
    return flask.render_template('about.html')

@app.route('/register', methods=['GET'])
def get_register():
    return flask.render_template('register.html')

@app.route('/register', methods=['POST'])
def post_register():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            twilio_account = flask.current_app.config['twilio_account']
            to_number = flask.request.form['phone-number']
            users.add_verified_signup(db, twilio_account, to_number)
            return flask.render_template('signed-up.html')

@app.route('/confirmation')
def get_confirmation():
    return flask.render_template('confirmation.html')

@app.route('/admin')
def get_admin():
    return flask.render_template('admin.html')

@app.route('/send-alert')
def get_sendalert():
    return flask.render_template('send-alert.html')

@app.route('/sent')
def get_sent():
    return flask.render_template('sent.html')

@app.route('/stats')
def get_stats():
    return flask.render_template('stats.html')

@app.route('/earth.geojson')
def get_earth():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            db.execute('SELECT ST_AsGeoJSON(geom) FROM world LIMIT 1')
            (geometry, ) = db.fetchone()
    
    feature = dict(geometry=json.loads(geometry), type='Feature', properties={})
    geojson = dict(type='FeatureCollection', features=[feature])
    
    return flask.jsonify(geojson)
