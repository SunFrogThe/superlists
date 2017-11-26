from unittest.mock import patch, call

from django.test import TestCase

from accounts import views
from accounts.models import Token

from .constants import TEST_EMAIL

EMAIL = 'email'

# urls
SEND_LOGIN_EMAIL = '/accounts/send_login_email'
LOGIN = '/accounts/login'
TEST_TOKEN = 'abcd123'
TEST_TOKEN_URI = f'?token={TEST_TOKEN}'


class SendLoginMailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post(SEND_LOGIN_EMAIL,
                                    data={EMAIL: TEST_EMAIL})
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post(SEND_LOGIN_EMAIL,
                         data={EMAIL: TEST_EMAIL})

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, views.SUBJECT)
        self.assertEqual(from_email, views.FROM_EMAIL)
        self.assertEqual(to_list, [TEST_EMAIL])

    def test_adds_success_message(self):
        response = self.client.post(
            SEND_LOGIN_EMAIL,
            data={EMAIL: TEST_EMAIL},
            follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            views.MESSAGE
        )
        self.assertEqual(message.tags, "success")

    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, mock_messages):
        response = self.client.post(
            SEND_LOGIN_EMAIL,
            data={EMAIL: TEST_EMAIL},)

        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, views.MESSAGE)
        )

    def test_creates_token_associated_with_email(self):
        self.client.post(SEND_LOGIN_EMAIL,
                         data={EMAIL: TEST_EMAIL})
        token = Token.objects.first()
        self.assertEqual(token.email, TEST_EMAIL)

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(SEND_LOGIN_EMAIL,
                         data={EMAIL: TEST_EMAIL})
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get(LOGIN + TEST_TOKEN_URI)
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get(LOGIN + TEST_TOKEN_URI)
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid=TEST_TOKEN)
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get(LOGIN + TEST_TOKEN_URI)
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get(LOGIN + TEST_TOKEN_URI)
        self.assertEqual(mock_auth.login.called, False)
