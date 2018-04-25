from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app
from app.forms import LoginForm
from app.db import db
from app import exceptions

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tyler'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/statistics')
def statistics():
    return render_template('statistics.html', title='Statistics')
@app.route('/checkers')
def checkers():
    return render_template('checkers.html', title='checc')

@app.route('/api/board', methods=['GET'])
def get_board():
    return jsonify(db.getBoardState())

@app.route('/api/stats', methods=['GET'])
def stats():
    statsEntry = db.getStats()
    retJson = {
        'redWins': statsEntry[0][0],
        'blackWins': statsEntry[0][1],
        'gameOver': (statsEntry[0][2] == 1),
        'turn': statsEntry[0][3]
    }
    return jsonify(retJson)

@app.route('/api/move', methods=['POST'])
def move():
    return(jsonify(True))

@app.route('/api/legal', methods=['POST', 'GET'])
def legal():
    if request.method == 'POST':
        startPoint = request.values.get('start')
        if(startPoint != None):
            return jsonify({
                'startPoint': startPoint,
                'endPoints': [0, 1, 2, 3, 4, 5, 6, 7]
            })
        else:
            raise exceptions.InvalidUsage('Use the "start" parameter with a number', status_code=418)
        return jsonify(request.values[0])
    return jsonify({
        'startPoint': 0,
        'endPoints': [0, 1, 2, 3, 4, 5, 6, 7]
        })

@app.errorhandler(exceptions.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response