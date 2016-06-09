# Globals
import datetime
import getopt
import time
import sys

import praw
from slacker import Slacker

import config

from util import (
    retrieve_credentials
)


post_limit = 10
dry_run = False


def notify_slack(submission: praw.objects.Submission):
    """
    Takes a submission and generates a message for Slack

    :type submission: praw.objects.Submission
    :param submission: Submission instance to parse
    """
    slack = Slacker(credentials['slack_key'])

    message = '*%s*' % submission.title
    message += '\n\nID: %s' % submission.id
    if submission.author:
        message += '\n\nUser: /u/%s' % submission.author.name
    message += '\n\nComments link: %s' % submission.permalink
    if submission.url and 'www.reddit.com' not in submission.url:
        message += '\n\nPost link: %s' % submission.url
    slack.chat.post_message('#newposts', message, as_user='postbot')


if __name__ == '__main__':
    credentials = retrieve_credentials()
    channel_id = credentials['channel_id']

    # Set up praw
    r = praw.Reddit('%s_watcher by /u/pandanomic' % config.subreddit)
    r.login(credentials['reddit_username'], credentials['reddit_pwd'], disable_warning=True)
    subreddit = r.get_subreddit(config.subreddit)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dpu:", ["dry", "poll", "unsticky="])
    except getopt.GetoptError:
        print('scraper.py -d -p -u')
        sys.exit(2)

    if len(opts) != 0:
        for o, a in opts:
            if o in ("-d", "--dry"):
                dry_run = True
            elif o in ("-p", "--poll"):
                now = datetime.datetime.utcnow()
                now_minus_10 = now + datetime.timedelta(minutes=-10)
                float_now = time.mktime(now_minus_10.timetuple())
                print("Checking for new posts")
                posts = [p for p in subreddit.get_new(limit=post_limit) if p.created_utc > float_now]
                if len(posts) is 0:
                    print("Nothing new")
                else:
                    print("Length is %s" % len(posts))
                    for post in sorted(posts, key=lambda p: p.created_utc):
                        if not dry_run:
                            notify_slack(post)
                        print("Notified")
            else:
                sys.exit('No valid args specified')
