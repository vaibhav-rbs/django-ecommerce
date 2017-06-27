from django.test import TestCase, RequestFactory
from django.shortcuts import render_to_response, resolve_url
from django.db import IntegrityError
import django_ecommerce.settings as settings
from payments.views import soon, register
from payments.models import User
from payments.forms import SigninForm, UserForm, CardForm
import unittest
import mock

########################
#### Testing routes ####
########################

from .views import sign_in, sign_out
from django.core.urlresolvers import resolve

class ViewTesterMixin(object):
    @classmethod
    def setupViewTester(cls, url, view_func, expected_html, status_code=200,
                        session={}):
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code  = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolves_to_correct_view(self):
        test_view = resolve(self.url)
        self.assertEquals(test_view.func, self.view_func)

    def test_returns_appropriate_reponse_code(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.status_code, self.status_code)

    def test_return_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.content, self.expected_html)


class RegisterPageTest(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': range(1,12),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years':range(2017, 2036)
            }
        )
        ViewTesterMixin.setupViewTester(
            '/register',
            register,
            html.content,
        )
    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    def test_invalid_form_returns_registration_page(self):
        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False
            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEquals(resp.content, self.expected_html)
            self.assertEquals(user_mock.call_count, 1)

    def test_registering_new_user_returns_sucessfully(self):
        self.request.session = {}
        self.request.method == 'POST'
        self.request.POST = {
            'email' : 'test@testemail.com',
            'name' : 'test',
            'stripe_token' : '....',
            'last_4_digits' : '4242',
            'password' : 'test_pass',
            'ver_password' : 'test_pass',
        }
        with mock.patch ('stripe.Customer') as stripe_mock:

            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)
            resp = register(self.request)
            self.assertEquals(resp.content, "")
            self.assertEquals(resp.status_code, 302)
            self.assertEqual(self.request.session['user'], 1)
            User.objects.get(email='test@testemail.com')

    def test_registering_user_twice_cause_error_msg(self):
        user = User(name='test', email='test@testemail.com')
        user.save()

        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email' : 'test@testemail.com',
            'name' : 'test',
            'stripe_token' : '....',
            'last_4_digits' : '4242',
            'password' : 'test_pass',
            'ver_password' : 'test_pass',
        }
        expected_form = UserForm(self.request.POST)
        expected_form.is_valid()
        expected_form.addError('test@testemail.com is already registered.')

        html = render_to_response(
            'register.html',
            {
                'form' : expected_form,
                'months' : range(1, 12),
                'publishable' : settings.STRIPE_PUBLISHABLE,
                'soon' : soon(),
                'user' : None,
                'years' : range(2017, 2036),

            }
        )
        with mock.patch('stripe.Customer') as stripe_mock:
            config = {'create.return_value' : mock.Mock()}
            stripe_mock.configure(**config)
            resp = register(self.request)

            self.assertEquals(resp.status_code, 200)
            self.assertEquals(self.request.session, {})

            users = Users.objects.filter(email='test@testemail.com')
            self.assertEquals(len(users), 1)




