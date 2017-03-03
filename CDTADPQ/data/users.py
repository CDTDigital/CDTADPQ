import requests, logging, uritemplate, random, uuid, re
from . import notifications

MailgunURL = 'https://api.mailgun.net/v2/{domain}/messages'

class MailgunAccount:

    def __init__(self, api_key, domain, sender):
        self.api_key = api_key
        self.domain = domain
        self.sender = sender

class User:

    def __init__(self, id, phone_number, zip_codes, email_address, emergency_types):
        self.id = id
        self.phone_number = phone_number
        self.zip_codes = zip_codes
        self.email_address = email_address
        self.emergency_types = emergency_types


def add_unverified_signup(db, account, to_number, zipcode):
    logging.info('add_unverified_signup: {}'.format(to_number))

    pin_number = '{:04d}'.format(random.randint(0, 9999))
    signup_id = str(uuid.uuid4())

    db.execute('''INSERT INTO unverified_signups
                  (signup_id, phone_number, pin_number, zipcode)
                  VALUES (%s, %s, %s, %s)''',
               (signup_id, to_number, pin_number, zipcode))

    send_verification_code(account, to_number, pin_number)
    return signup_id

def send_verification_code(account, to_number, code):
    '''
    '''
    body = 'Your CA Alerts PIN code is {}. Use this to confirm your phone number. \n\nIf you didn\'t ask for this, please ignore this message.'.format(code)
    return notifications.send_sms(account, to_number, body)

def send_email_verification_code(account, to_address, code):
    '''
    '''
    url = uritemplate.expand(MailgunURL, dict(domain=account.domain))
    body = 'Your CA Alerts PIN code is {}.\n\nUse this to confirm your email address. If you didn\'t ask for this, please ignore this message.'.format(code)
    data = {'from': account.sender, 'to': to_address, 'subject': 'Your CA Alerts PIN code', 'text': body}
    auth = 'api', account.api_key
    posted = requests.post(url, auth=auth, data=data)

    if posted.status_code not in range(200, 299):
        if 'message' in posted.json():
            raise RuntimeError(posted.json()['message'])
        else:
            raise RuntimeError('Bad response from Mailgun')

    return True

def verify_user_signup(db, given_pin_number, signup_id):
    '''
    '''
    db.execute('''SELECT pin_number, phone_number, zipcode
                  FROM unverified_signups WHERE signup_id = %s''',
               (signup_id, ))

    try:
        (expected_pin_number, phone_number, zipcode) = db.fetchone()
    except TypeError:
        return False

    if given_pin_number != expected_pin_number:
        return False

    db.execute('SELECT true FROM users WHERE phone_number = %s', (phone_number, ))
    existing_user = db.fetchone()
    zip_codes = [zipcode] if zipcode else []

    if existing_user is None:
        db.execute('INSERT INTO users (phone_number, zip_codes) VALUES (%s, %s)',
                   (phone_number, zip_codes))
    else:
        # Login screen does not offer a zip code input field
        pass

    return phone_number

def get_user_info(db, phone_number):
    '''
    '''
    db.execute('''SELECT phone_number, zip_codes, email_address
                  FROM users WHERE phone_number = %s''',
               (phone_number, ))

    try:
        (phone_number, zip_codes, email_address) = db.fetchone()
    except TypeError:
        return None

    return phone_number, zip_codes, email_address

def update_user_profile(db, phone_number, zip_codes_str):
    '''
    '''
    zip_codes = re.findall(r'\b(\d{5})\b', zip_codes_str)

    db.execute('''UPDATE users SET zip_codes = %s
                  WHERE phone_number = %s''',
               (zip_codes, phone_number))

def update_email_address(db, phone_number, email_address):
    '''
    '''
    db.execute('UPDATE users SET email_address = %s WHERE phone_number = %s',
               (email_address, phone_number))

def delete_user(db, phone_number):
    '''
    '''
    db.execute('DELETE FROM users WHERE phone_number = %s',
               (phone_number, ))

def get_all_users(db):
    '''
    '''
    db.execute('SELECT * FROM users')
    all_users = []
    for user_row in db.fetchall():
        all_users.append(User(user_row['id'], user_row['phone_number'], user_row['zip_codes'],
                                                  user_row['email_address'], user_row['emergency_types']))
    return all_users
