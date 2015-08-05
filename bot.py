__author__ = 'sweemeng'
import yaml
import twitter
import random
import github3
import time

class TwitterNotifier(object):
    def __init__(self):
        self.config = yaml.load(open("config.yaml"))

        self.consumer_key = self.config["consumer_key"]
        self.consumer_secret = self.config["consumer_secret"]
        self.access_token_key = self.config["access_token_key"]
        self.access_token_secret = self.config["access_token_secret"]
        self.client = twitter.Api(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token_key=self.access_token_key,
            access_token_secret=self.access_token_secret
        )
        self.message = ""
        check = self.client.VerifyCredentials()
        if not check:
            raise Exception("Credential Fail")

    def generate_message(self):
        raise NotImplementedError("Method need to be implemented")

    def notify(self):
        self.generate_message()
        if not self.message:
            raise Exception("Can't post empty message")
        self.client.PostUpdate(self.message)


class FortuneNotifier(TwitterNotifier):
    def generate_message(self):
        msg_config = yaml.load(open("statuses.yaml"))
        messages = msg_config["status"]
        self.message = random.choice(messages)


class AnnouncementNotifier(TwitterNotifier):
    def generate_message(self):
        msg_config = yaml.load(open("statuses.yaml"))
        self.message = msg_config["motd"]



class GithubNotifier(TwitterNotifier):
    def generate_message(self):
        repo = github3.repository("sinar", "blockedornot.sinarproject.org")



def main():
    announcement = AnnouncementNotifier()
    announcement.notify()

    time.sleep(30)
    notifiers = [
        FortuneNotifier,
    ]

    notifier = random.choice(notifiers)()

    notifier.notify()


if __name__ == "__main__":
    main()