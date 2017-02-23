import flask, codecs, psycopg2, os, json, functools, sys
from ..data import users

def user_is_logged_in(untouched_route):
    '''
    '''
    @functools.wraps(untouched_route)
    def wrapper(*args, **kwargs):
        print('flask.session:', flask.session, file=sys.stderr)
        if 'phone_number' in flask.session:
            print('Phone number exists:', flask.session['phone_number'], file=sys.stderr)
        else:
            print('No phone number exists.', file=sys.stderr)

        return untouched_route(*args, **kwargs)
    
    return wrapper

app = flask.Flask(__name__) 
app.secret_key = os.environ['FLASK_SECRET_KEY']

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
            signup_id = users.add_unverified_signup(db, twilio_account, to_number)
            return flask.redirect(flask.url_for('get_registered', signup_id=signup_id), code=303)

@app.route('/registered/<signup_id>')
def get_registered(signup_id):
    return flask.render_template('registered.html', signup_id=signup_id)

@app.route('/confirm', methods=['POST'])
def post_confirm():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            pin_number = flask.request.form['pin-number']
            signup_id = flask.request.form['signup-id']
            phone_number = users.verify_user_signup(db, pin_number, signup_id)
            print('Added phone number:', phone_number, file=sys.stderr)
            flask.session['phone_number'] = phone_number
            return flask.redirect(flask.url_for('get_confirmation'), code=303)

@app.route('/confirmation')
@user_is_logged_in
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
