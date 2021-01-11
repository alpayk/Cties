import json
import sqlite3
import random
from flask import Flask
from flask import Flask, render_template
from flask import request
app = Flask(__name__)

@app.route('/save_question', methods=['POST'])
def save_question():
    req_data = request.get_json()
    url = req_data['url']
    question = req_data['question']
    answer = req_data['answer']
    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    country_id = c.execute(f'SELECT countries.id as id FROM cities, countries, states WHERE cities.id = {answer} AND cities.state_id = states.id AND states.country_id = countries.id').fetchone()['id']
    c.execute(f'INSERT INTO questions(url, question, city, country) VALUES(\'{url}\', \'{question}\', {answer}, {country_id})')
    conn.commit()
    conn.close()
    return 'OK'

@app.route('/admin')
def admin():
    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    rows = c.execute('SELECT * FROM cities').fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', cities=rows)

@app.route('/city/<query>')
def city(query):
    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    rows = c.execute(f'SELECT cities.id, cities.name || \' - \' || countries.name as name FROM cities, countries, states WHERE cities.name like \'{query}%\' AND cities.state_id = states.id AND states.country_id = countries.id LIMIT 20').fetchall()
    conn.commit()
    conn.close()

    result = []

    for i in rows:
        result.append({'id': i['id'], 'name': i['name']})
    return json.dumps(result)


@app.route('/verify/<int:question>/<int:answer>')
def verify(question, answer):
    conn = sqlite3.connect('ccs.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    row = c.execute(f'SELECT city FROM questions WHERE id = {question}').fetchone()
    conn.commit()
    conn.close()
    if row['city'] == answer:
        return '1'
    else:
        return '0'

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
        answers = c.execute(f'SELECT cities.* FROM cities, states WHERE cities.state_id = states.id AND cities.id <> {row["city"]} ORDER BY random() LIMIT 3;').fetchall()
        answers.append(c.execute(f'SELECT * FROM cities WHERE id={row["city"]}').fetchone())
    else:
        row = c.execute(f'SELECT * FROM questions WHERE country = {country_id} ORDER BY RANDOM() LIMIT 1;').fetchone()
        answers = c.execute(f'SELECT cities.* FROM cities, states WHERE cities.state_id = states.id AND cities.id <> {row["city"]} AND states.id IN (SELECT id FROM states WHERE country_id={country_id}) ORDER BY random() LIMIT 3;').fetchall()
        answers.append(c.execute(f'SELECT * FROM cities WHERE id={row["city"]}').fetchone())
    if row == None:
        return 'No questions available for this country'

    random.shuffle(answers)
    question['options'] = []

    for i in answers:
        question['options'].append({'id': i['id'], 'name': i['name']})

    question['url'] = row['url']
    question['id'] = row['id']
    question['text'] = row['question']

    return json.dumps(question)

if __name__ == '__main__':
   app.run()

# no input - ülke listesi 
# input ülke ismi - şehir sorusu
