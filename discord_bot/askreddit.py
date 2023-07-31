from configparser import ConfigParser
import praw
import random

# config function for reddit API info
def config(filename='praw.ini', section='lawrencebot'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            info[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return info

def authenticate():

    info = config()

    # get a read-only reddit instance
    reddit = praw.Reddit(
        client_id=info['client_id'],
        client_secret=info['client_secret'],
        user_agent=info['user_agent'],
    )

    return reddit

def get_question():
    
    pass

if __name__ == "__main__":
    # test for debugging 
    reddit = authenticate()

    for submission in reddit.subreddit("AsKReddit").hot(limit=5):
        print(submission.title)