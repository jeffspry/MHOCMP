import time
import datetime
import praw
import csv
import os
import redis

__author__ = '/u/spookyyz'
__version__ = '0.1'
user_agent = 'MHOCMP Vote Reminder by /u/spookyyz'
bot_signature = "\r\n\r\n^(_MHOCMP Vote Reminder v%s created by /u/spookyyz ) ^|| ^(Feel free to message me with any ideas or problems_)" % __version__

###########Global Vars
SUBREDDIT = 'MHOC'
WAIT_TIME = 30
SLEEP_TIME = 10
DEVELOPER = True #True to print output instead of post
START_TIME = time.time() #new var to monitor time of startup so posts prior to that time can be ignored. (in Unix)
REPLIED_TO = [] #will read redis db keys into this list
#REDIS_DB = redis.from_url(os.environ.get("REDIS_URL"))
###########

###########CSV PROCESSING HOLDER (needs to be read periodically to check for updates)

class MHOC_bot(object):
    """
    This bot will check /r/MHOCMP for any posts aged 4 days or more.  If a post is found,
    it will compare users who have commented (voted) on said post and those who should have
    voted (via CSV list provided).  If person on list has not voted a PM will be sent to that
    user reminding them to vote on the current issue.  Submission ID will then be posted to a
    redis with a value of each person messaged.
    """
    def __init__(self):
        self.r = praw.Reddit(user_agent=user_agent) #init praw
        if (DEVELOPER):
            print "DEVELOPER MODE ON (NO POSTING)"
        else:
            try:
                self.r.login(os.environ['MHOCMP_REDDIT_USER'], os.environ['MHOCMP_REDDIT_PASS'])
            except Exception, e:
                print "ERROR(@login): " + str(e)

    def submission_age(self, submission):
        """
        Take submission object.
        RETURN: True if submission is 4 days or older, False if not
        """
        age = datetime.datetime.utcfromtimestamp(submission.created)
        print "[@get_submission_age]: %s" % str(age)

    def scan(self):
        """
        Workhorse, will iterate through submissions in an effort to find submissions older
        than 4 days old.  If found will pass to processing method.
        RETURN: Submission object that is 4 days or older.
        """
        try:
            sub_obj = self.r.get_subreddit(SUBREDDIT)
            if (DEVELOPER):
                print "Getting listings for /r/%s..." % SUBREDDIT
        except Exception, e:
            print "ERROR(@sublisting): " + str(e)

        for submission in sub_obj.get_new(limit=25):
            self.submission_age(submission)


bot = MHOC_bot()
bot.scan()
