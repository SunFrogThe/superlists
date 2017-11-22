from unittest.mock import patch, call

from django.test import TestCase

from accounts import views
from accounts.models import Token

EMAIL = 'email'
TEST_EMAIL = 'edith@example.com'

# urls
SEND_LOGIN_EMAIL = '/accounts/send_login_email'
LOGIN = '/accounts/login'


class SendLoginMailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get(LOGIN + '?token=abcd123')
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
            "Check your email, we've sent you a link you can use to log in."
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
