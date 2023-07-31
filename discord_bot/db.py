from configparser import ConfigParser
import psycopg2
import json

# config function for database info
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

# send our question and answer pairs to the database
def send_to_database(q, a, cat):

    db = config()

    conn = psycopg2.connect(host=db['host'], database=db['database'], user=db['user'], 
                            password=db['password'])
    
    cur = conn.cursor()
    query = "INSERT INTO questions" + cat + " (question, answer) VALUES (%s, %s)"  
    
    cur.execute(query, (q,a))
    
    conn.commit()
    cur.close()
    
    return
    
if __name__ == "__main__":
    send_to_database("how old are you?", "20 at the time of writing this.", "misc_personal")