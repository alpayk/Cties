import json
import sqlite3
import random
from flask import Flask
app = Flask(__name__)

@app.route('/verify/<int:question>/<int:answer>')
def verify(question, answer):
    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    row = c.execute(f'SELECT city FROM questions WHERE id = {question}').fetchone()
    conn.commit()
    conn.close()
    if row['city'] == answer:
        return 1
    else:
        return 0

@app.route('/country_list')
def country_list():
    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #rows = c.execute('SELECT * FROM countries').fetchall()
    rows = c.execute('SELECT DISTINCT questions.country AS id, countries.name FROM questions, countries WHERE questions.country = countries.id').fetchall()
    conn.commit()
    conn.close()

    result = []

    for i in rows:
        result.append({'id': i['id'], 'name': i['name']})

    return json.dumps(result)

@app.route('/question/')
@app.route('/question/<int:country_id>')
def question(country_id = -1):
    question = {}

    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if country_id == -1:
        row = c.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;').fetchone()
    else:
        row = c.execute(f'SELECT * FROM questions WHERE country = {country_id} ORDER BY RANDOM() LIMIT 1;').fetchone()
    
    if row == None:
        return 'No questions available for this country'

    answers = [int(row['city'])]

    while len(answers) < 4:
        temp_rand = random.randint(1, 48313) # Current # of cities
        if temp_rand not in answers:
            answers.append(temp_rand)

    rows = c.execute(f'SELECT * FROM cities WHERE id IN ({str(answers)[1:-1]})').fetchall()
    question['options'] = []

    for i in rows:
        question['options'].append({'id': i['id'], 'name': i['name']})

    question['url'] = row['url']
    question['id'] = row['id']
    question['text'] = row['question']

    return json.dumps(question)

if __name__ == '__main__':
   app.run()


# no input - ülke listesi 
# input ülke ismi - şehir sorusu
