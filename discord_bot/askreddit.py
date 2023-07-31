from configparser import ConfigParser
from datetime import datetime
import asyncpraw
import pytz
import random

# config function for reddit API info
def config(filename='praw.ini', section='lawrencebot'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to lawrencebot
    info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            info[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return info

async def authenticate():

    info = config()

    # get a read-only reddit instance
    reddit = asyncpraw.Reddit(
        client_id=info['client_id'],
        client_secret=info['client_secret'],
        user_agent=info['user_agent'],
    )

    return reddit

async def get_question():

    reddit = await authenticate()

    # get a random askreddit question
    # exclude nsfw questions
    while True:
        submissions = await reddit.subreddit("AskReddit")

        print(submissions)

        submission = random.choice([submission async for submission in submissions.hot(limit=200)])

        if not submission.over_18:
            break

    question = submission.title

    # get time
    utc_datetime = datetime.utcfromtimestamp(submission.created_utc)
    local_timezone = pytz.timezone('Canada/Mountain')
    local_time = utc_datetime.astimezone(local_timezone)
    local_time = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    time_posted = str(local_time)

    print(question)
    print(time_posted)

    return question, time_posted

if __name__ == "__main__":
    # test for debugging 
    reddit = authenticate()

    submission = reddit.subreddit("AskReddit").random()

    print("Question: " + submission.title)

    utc_datetime = datetime.utcfromtimestamp(submission.created_utc)
    local_timezone = pytz.timezone('Canada/Mountain')
    local_time = utc_datetime.astimezone(local_timezone)
    local_time = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

    print("Time posted: " + str(local_time))
    print("NSFW? " + str(submission.over_18))