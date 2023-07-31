import json
import pandas as pd
import random
import askreddit

path_to_misc = "../questions/misc_personal.txt"

# which categories of questions we have for now (constantly updated)
categories = ['misc_personal', 'askreddit']

async def generate(category):
    
    # if miscellaneous personal questions, ask a random line in the file
    if category == 'misc_personal':
        f = open(path_to_misc, 'r', encoding='utf-8')
        questions = f.readlines()
        
        num = random.randrange(0, len(questions))
        question = questions[num]
        time = 'null' # deal with later

        print(question)
        
        f.close()
    elif category == 'askreddit':
        # get askreddit question
        question, time = await askreddit.get_question()

    return question, category, time

"""
Generates a random question to ask.
In future, add categories of question
"""
async def get_question(category='Any'):
    
    if category == 'Any':
        num = random.randrange(0, len(categories))
        category = categories[num]
    else:
        question, cat, time = await generate(category)
    
    return question, cat, time