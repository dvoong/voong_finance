import datetime
from django.test import TestCase, Client
from django.urls import resolve
from voong_finance_app import views
from voong_finance_app.models import User, Transaction
from django.contrib.auth import authenticate, login

class HomePage(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        # self.assertEqual(resolve('/home').func, views.home)
        response = self.client.get('/home')
        self.assertEqual(response.resolver_match.func, views.home)

    def test_template(self):
        username = 'voong.david@gmail.com'
        password = 'password'
        user = User.objects.create_user(username=username, first_name='David', last_name='Voong', email=username, password=password)
        login = self.client.login(username=username, password=password)
        
        response = self.client.get('/home')

        self.assertTemplateUsed(response, 'voong_finance_app/home.html')
        self.assertEqual(response.context['today'], datetime.date.today().isoformat())

    def test_if_not_authenticated_redirect_to_signin_page(self):
        response = self.client.get('/home')
        self.assertRedirects(response, '/signin')

        
class TestRegistration(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        self.assertEqual(resolve('/registration').func, views.registration)

    def test_template(self):
        response = self.client.get('/registration')
        self.assertTemplateUsed(response, 'voong_finance_app/registration.html')

    def test_post_registration_form(self):
        data = {
            'first-name': 'David',
            'last-name': 'Voong',
            'email': 'voong.david@gmail.com',
            'password': 'password'
        }
        
        response = self.client.post('/registration', data)
        
        users = User.objects.all()

        self.assertEqual(len(users), 1)

        user = users[0]
        self.assertEqual(user.first_name, 'David')
        self.assertEqual(user.last_name, 'Voong')
        self.assertEqual(user.email, 'voong.david@gmail.com')
        self.assertTrue(user.check_password('password'))
        self.assertEqual(user.username, 'voong.david@gmail.com')
        self.assertRedirects(response, '/signin')
        
        
class TestSignin(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        self.assertEqual(resolve('/signin').func, views.signin)

    def test_template(self):
        response = self.client.get('/signin')
        self.assertTemplateUsed(response, 'voong_finance_app/signin.html')

    def test_check_credentials(self):
        email = 'voong.david@gmail.com'
        password = 'password'
        
        user = User.objects.create_user(email=email, password=password, username=email)
        response = self.client.post('/signin', data={'email': email, 'password': password})
        self.assertRedirects(response, '/home')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

class TestCreateTransaction(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        self.assertEqual(resolve('/create-transaction').func, views.create_transaction)

    def test(self):
        username = 'voong.david@gmail.com'
        password = 'password'
        user = User.objects.create_user(username=username, first_name='David', last_name='Voong', email=username, password=password)
        login = self.client.login(username=username, password=password)

        data = {
            'date': '2017-09-01',
            'transaction-type': 'income',
            'description': 'description',
            'transaction-size': '100'
        }

        response = self.client.post('/create-transaction', data=data)

        transactions = Transaction.objects.all()
        self.assertEqual(len(transactions), 1)
        transaction = transactions[0]

        self.assertEqual(transaction.user, user)
        self.assertEqual(transaction.date, datetime.date(2017, 9, 1))
        self.assertEqual(transaction.type, data['transaction-type'])
        self.assertEqual(transaction.description, data['description'])
        self.assertEqual(transaction.size, 100)
        self.assertEqual(transaction.ordinal, 0)
        self.assertEqual(response.json(), {
            'date': data['date'],
            'transaction_type': data['transaction-type'],
            'description': data['description'],
            'transaction_size': 100,
            'balance': 100,
            'ordinal': 0
        })

class TestGetTransactions(TestCase):

    def setUp(self):
        self.client = Client()
        username = 'voong.david@gmail.com'
        password = 'password'
        self.user = User.objects.create_user(username=username, first_name='David', last_name='Voong', email=username, password=password)
        login = self.client.login(username=username, password=password)

    def test_url_resolve(self):
        response = self.client.get('/get-transactions')
        self.assertEqual(response.resolver_match.func, views.get_transactions)

    def test(self):

        transaction = Transaction.objects.create(
            user=self.user,
            date=datetime.date(2017, 11, 1),
            type='income',
            description='description',
            size=10,
            balance=10,
            ordinal=0
        )

        response = self.client.get('/get-transactions')

        self.assertEqual(response.json(), {
            'status': 200,
            'data': [
                {
                    'date': '2017-11-01',
                    'transaction_type': 'income',
                    'description': 'description',
                    'transaction_size': 10,
                    'balance': 10,
                    'ordinal': 0
                }
            ]
        })
