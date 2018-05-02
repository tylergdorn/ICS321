from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app
from app.db import db
from app.db import gamelogic as gl
from app import exceptions

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html', title='Statistics', stats=db.getStats())

@app.route('/checkers')
def checkers():
    return render_template('checkers.html', title='checc')

@app.route('/api/board', methods=['GET'])
def get_board():
    return jsonify(db.getBoardState())

@app.route('/api/newgame', methods=['POST'])
def new_game():
    if request.method == 'POST':
        secret = int(request.values.get('secret'))
        if secret == 420: #HAH ITS THE WEED NUMBER
            db.clearGame()
            return jsonify(True)
    return jsonify(db.getBoardState())

@app.route('/api/jump', methods=['POST'])
def jump():
    if request.method == 'POST':
        start = int(request.values.get('start'))
        end = int(request.values.get('end'))
        db.jump(start, end)
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
    if request.method == 'POST':
        start = request.values.get('start')
        end = request.values.get('end')
        print("s: " + str(start) + "e: " + str(end))
        if((start != '') and (end != '')):
            print("passed check")
            db.updatePosition(start, end)    
            return jsonify(True)
        else:
            raise exceptions.InvalidUsage('Use the "start" and "end" parameter with a number', status_code=400)
    else:
        raise exceptions.InvalidUsage('Use the "start" and "end" parameter with a number', status_code=400)

@app.route('/api/legal', methods=['POST'])
def legal():
    if request.method == 'POST':
        startPoint = request.values.get('start')
        if(startPoint != ''):
            temp = gl.validMoves(startPoint)
            combined = []
            combined.extend(temp['steps'])
            combined.extend(temp['hops'])
            return jsonify({
                'startPoint': startPoint,
                'endPoints': combined
            })
        else:
            raise exceptions.InvalidUsage('Use the "start" parameter with a number', status_code=400)
        return jsonify(request.values[0])
    else:
        raise exceptions.InvalidUsage('Use the "start" parameter with a number', status_code=400)

@app.errorhandler(exceptions.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response