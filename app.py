from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


@app.route('/')
def homepage():
    """Show homepage"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template("index.html", board=board, highscore=highscore, numplays=numplays)

@app.route('/check-word')
def check_word():
    """Cheking word in dictionary"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result' : response})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Updatting score"""

    score = request.json["score"]
    numplays = session.get("numplays", 0)
    highscore = session.get("higscore", 0)

    session['highscore'] = max(score, highscore)
    numplays['numplays'] = numplays + 1

    return jsonify(record=score > highscore)
