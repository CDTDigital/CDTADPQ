import os, unittest, unittest.mock, httmock, urllib.parse
from . import recreate
from . import notify
from . import users
from . import wildfires
from . import notifications

import psycopg2, psycopg2.extras

class NotifyTests (unittest.TestCase):
    def setUp(self):
        '''
        '''
        self.database_url = os.environ['DATABASE_URL']
        recreate.main(self.database_url)

        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as db:
                fire_dict = wildfires.convert_fire_point({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-122, 37]},
                                                     'properties': {'objectid': 1, 'latitude': 37, 'longitude': -122, 'gacc': 'SACC',
                                                     'hotlink': 'http://www.nifc.gov/fireInfo/nfn.htm', 'state': 'OK', 'status': 'I', 'irwinid': '{14DD44C2-ACF0-4998-A99B-971BF60E9A11}',
                                                     'acres': 1500, 'firecause': 'Human', 'reportdatetime': 1487091600000, 'percentcontained': 49, 'uniquefireidentifier': '2017-OKNEU-170102',
                                                     'firediscoverydatetime': 1486984500000, 'complexparentirwinid': None, 'pooresponsibleunit': 'OKNEU', 'incidentname': 'Spike Road',
                                                     'iscomplex': 'false', 'irwinmodifiedon': 1487067267000, 'mapsymbol': '1', 'datecurrent': 1487235965000, 'pooownerunit': None,
                                                     'owneragency': None, 'fireyear': None, 'localincidentidentifier': None, 'incidenttypecategory': None}})
                wildfires.store_fire_point(db, fire_dict)
                db.execute('INSERT INTO users (phone_number, zip_codes, email_address) VALUES (%s, %s, %s)',
                           ('+15105551212', ['95065'], 'user1@example.com'))
                db.execute('INSERT INTO users (phone_number, zip_codes, email_address) VALUES (%s, %s, %s)',
                           ('+15103351786', ['94103'], 'user2@example.com'))


    def test_main(self):
        '''
        '''
        with unittest.mock.patch('CDTADPQ.data.wildfires.get_current_fires') as get_current_fires, \
             unittest.mock.patch('CDTADPQ.data.notify.get_users_to_notify') as get_users_to_notify, \
             unittest.mock.patch('CDTADPQ.data.notify.send_notification') as send_notification, \
             unittest.mock.patch('CDTADPQ.data.notify.send_email_notification') as send_email_notification, \
             unittest.mock.patch('CDTADPQ.data.notify.log_user_notification') as log_user_notification:
            get_current_fires.return_value = [wildfires.FirePoint({'type': 'Point', 'coordinates': [-122, 37]}, 1, '123', 'fire', 'True', 'now', 'people', 15)]
            get_users_to_notify.return_value = [users.User(1, '+15105551212', ['94107'], 'me@example.com', ['fire'])]
            notify.main()
        self.assertEqual(len(get_current_fires.mock_calls), 1)
        self.assertEqual(len(get_users_to_notify.mock_calls), 1)
        self.assertEqual(len(send_notification.mock_calls), 1)
        self.assertEqual(len(send_email_notification.mock_calls), 1)
        self.assertEqual(len(log_user_notification.mock_calls), 1)

    def test_get_users_to_notify(self):
        '''
        '''
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as db:
                (fire, ) = wildfires.get_current_fires(db)

                # Look for users within a half-mile of the fire
                os.environ['RADIUS_MILES'] = '0.5'
                users = notify.get_users_to_notify(db, fire)
                self.assertEqual(1, len(users))
                self.assertEqual('+15105551212', users[0].phone_number)

                # Now look again with a really big radius
                os.environ['RADIUS_MILES'] = '500'
                users = notify.get_users_to_notify(db, fire)
                self.assertEqual(2, len(users))

        # If the user has been notified, it should not be returned
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as db:
                (fire, ) = wildfires.get_current_fires(db)

                # Look for users within a half-mile of the fire
                os.environ['RADIUS_MILES'] = '0.5'

                # Log entry indicates user has been notified
                db.execute('INSERT INTO user_emergencies_log (emergency_type, emergency_external_id, user_id) VALUES (%s, %s, %s)',
                    ('fire', fire.usgs_id, 1))

                users = notify.get_users_to_notify(db, fire)
                self.assertEqual(0, len(users))

    def test_send_notification(self):
        '''
        '''
        account = notifications.TwilioAccount('sid', 'secret', 'account', 'number')
        fire = unittest.mock.Mock(name='Bad Fire')
        test_user = users.User(1, '+15105551212', ['94107'], 'test_user@example.com', ['fire'])

        with unittest.mock.patch('CDTADPQ.data.notifications.send_sms') as send_sms:
            notify.send_notification(account, test_user, 'omg fire')
            send_sms.assert_called_once_with(account, test_user.phone_number, 'omg fire')

    def test_send_email_notification(self):
        '''
        '''
        account = notifications.MailgunAccount('api-key', 'domain', 'sender')
        fire = unittest.mock.Mock(name='Bad Fire')
        test_user1 = users.User(1, '+15105551212', ['94107'], 'test_user@example.com', ['fire'])
        test_user2 = users.User(1, '+15105551212', ['94107'], None, ['fire'])

        with unittest.mock.patch('CDTADPQ.data.notifications.send_email') as send_email:
            notify.send_email_notification(account, test_user1, 'omg fire')
            notify.send_email_notification(account, test_user2, 'omg fire')

        send_email.assert_called_once_with(account, test_user1.email_address, 'Emergency!', 'omg fire')

    def test_log_user_notification(self):
        '''
        '''
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as db:
                user = users.User(1, '+15105551212', ['94107'], 'me@example.com', ['fire'])
                fire = wildfires.FirePoint({'type': 'Point', 'coordinates': [-122, 37]}, 1, '123', 'fire', 'True', 'now', 'people', 15)
                logging_succeeded = notify.log_user_notification(db, user, fire)
                self.assertTrue(logging_succeeded)

    def test_log_notification_for_admin_records(self):
        '''
        '''
        # Log without an emergency (i.e. fire)
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as db:
                logging_succeeded = notify.log_notification_for_admin_records(db, 'This is an arbitrary message', 3)
                self.assertTrue(logging_succeeded)

        # Log with an emergency
        fire = wildfires.FirePoint({'type': 'Point', 'coordinates': [-122, 37]}, 1, '123', 'fire', 'True', 'now', 'people', 15)
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as db:
                logging_succeeded = notify.log_notification_for_admin_records(db, 'This is an arbitrary message', 3, fire.id, 'fire')
                self.assertTrue(logging_succeeded)
