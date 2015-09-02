import unittest
from bot import TwitterNotifier, FortuneNotifier, AnnouncementNotifier
from mock import Mock, patch, call

__author__ = 'lowks'


class SinarNotifierTests(unittest.TestCase):

    @patch("__builtin__.open")
    @patch("twitter.Api.VerifyCredentials")
    @patch("yaml.load")
    def setUp(self, mock_load_config, mock_twitter, mock_open):
        mock_open.return_value = "config.yaml"
        self.base_auth = dict(consumer_key='consumer_key',
                              consumer_secret='consumer_secret',
                              access_token_key='access_token_key',
                              access_token_secret='access_token_secret')
        self.statuses = dict(status='Status', motd='I am the MOTD')

        def load_config(filename):
            if "config.yaml" in filename:
                return self.base_auth
            elif "statuses.yaml" in filename:
                return self.statuses
        mock_load_config.side_effect = load_config
        mock_twitter.return_value = True
        self.bot = TwitterNotifier()
        self.fortune_notifier = FortuneNotifier()

    def tearDown(self):
        pass

    def test_generate_message_not_implemented(self):

        """Assert that generate_message has not been implemented yet"""

        with self.assertRaises(NotImplementedError):
            self.bot.generate_message()

    @patch("twitter.Api.VerifyCredentials")
    def test_generate_message_exception(self, mock_twitter):

        """Assert that generate_message Exception: Fail Credentials"""
        mock_twitter.return_value = False

        with self.assertRaises(Exception):
            self.bot.generate_message()

    def test_notify_exception(self):

        """Assert that when generate_message

        is empty notify will generate Exception
        """

        self.bot.message = ""
        with self.assertRaises(Exception):
            self.bot.notify()

    @patch("bot.TwitterNotifier.generate_message")
    @patch("twitter.Api.PostUpdate")
    def test_notify(self, mock_twitter, mock_twitter_notifier_message):

        """Assert that when generate_message \
        is empty notify will generate Exception
        """
        self.bot.message = "gugu"
        self.bot.notify()
        self.assertIn(call('gugu'), mock_twitter.mock_calls)

    @patch("__builtin__.open")
    @patch("twitter.Api.VerifyCredentials")
    @patch("yaml.load")
    def test_fortune_notifier(self, mock_load_config, mock_twitter, mock_open):

        """Assert that FortuneNotifier works"""

        mock_open.return_value = "config.yaml"

        def load_config(filename):
            if "config.yaml" in filename:
                return self.base_auth
            elif "statuses.yaml" in filename:
                return self.statuses
        mock_load_config.side_effect = load_config
        self.fortune_notifier = FortuneNotifier()
        mock_open.return_value = "statuses.yaml"
        self.fortune_notifier.generate_message()
        self.assertIn(self.fortune_notifier.message, 'Status')

    @patch("__builtin__.open")
    @patch("twitter.Api.VerifyCredentials")
    @patch("yaml.load")
    def test_announcement_notifier(self, mock_load_config,
                                   mock_twitter, mock_open):

        """Assert that AnnouncementNotifier works"""

        mock_open.return_value = "config.yaml"

        def load_config(filename):
            if "config.yaml" in filename:
                return self.base_auth
            elif "statuses.yaml" in filename:
                return self.statuses
        mock_load_config.side_effect = load_config
        self.announcement_notifier = AnnouncementNotifier()
        mock_open.return_value = "statuses.yaml"
        self.announcement_notifier.generate_message()
        self.assertEqual(self.announcement_notifier.message,
                         'I am the MOTD')
