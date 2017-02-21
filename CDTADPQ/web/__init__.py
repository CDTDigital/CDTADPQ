import flask, codecs, psycopg2, os, json

app = flask.Flask(__name__)

if os.environ['TWILIO_ACCOUNT'].startswith('AC'):
    app.config['twilio_sid'] = os.environ.get('TWILIO_SID', '')
    app.config['twilio_secret'] = os.environ.get('TWILIO_SECRET', '')
    app.config['twilio_account'] = os.environ.get('TWILIO_ACCOUNT', '')
    app.config['twilio_number'] = os.environ.get('TWILIO_NUMBER', '')
else:
    app.config['twilio_sid'] = codecs.decode(os.environ.get('TWILIO_SID', ''), 'rot13')
    app.config['twilio_secret'] = codecs.decode(os.environ.get('TWILIO_SECRET', ''), 'rot13')
    app.config['twilio_account'] = codecs.decode(os.environ.get('TWILIO_ACCOUNT', ''), 'rot13')
    app.config['twilio_number'] = os.environ.get('TWILIO_NUMBER', '')

@app.route('/')
def get_index():
    return flask.render_template('index.html')

@app.route('/about')
def get_about():
    return flask.render_template('about.html')

@app.route('/register')
def get_register():
    return flask.render_template('register.html')

@app.route('/confirmation')
def get_confirmation():
    return flask.render_template('confirmation.html')

@app.route('/earth.geojson')
def get_earth():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            db.execute('SELECT ST_AsGeoJSON(geom) FROM world LIMIT 1')
            (geometry, ) = db.fetchone()
    
    feature = dict(geometry=json.loads(geometry), type='Feature', properties={})
    geojson = dict(type='FeatureCollection', features=[feature])
    
    return flask.jsonify(geojson)