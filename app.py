#importing modules from flask to set up the web application#
#importing custom module 'Boggle' that contains the logic of the game"""
from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

#initializing the Flask application
app = Flask(__name__)
app.config["secret_key"] = "shiiiii!"

#create an instance of the Boggle game
boggle_game = Boggle()

#create home route
@app.route("/")
def homepage():
    #generate a new Boggle board
    board = boggle.game.make_board()
    #store the generated board in the session, making accessible accross requests
    session['board'] = board
    
    highscore = session.get("highscore", 0)
    xplays = session.get("xplays", 0)

    #Render the "index.html" template and pass the Boggle board, high score, and number of plays as template variables
    return render_template("index.html", board=board, highscore=highscore, xplays=xplays)

#create check_word route
@app.route("/check-word")
def check_word():
    """check if the word is in the dictionary"""

    # Retrieve the word from the query parameters
    word = request.args["word"]
    #Retrieve the Boggle board from the session
    board = session["board"]
    #Check if the given word is valid on the Boggle board
    response = boggle_game.check_valid_word(board, word)

    #Return a JSON response containing whether the word is valid
    return jsonify({'result': response})

#create post-score route (POST request)
@app.route("/post-score", method=["POST"])
def post_score():
    """Receive score, update xplays, update high score if needed"""
    #Retrieve the score from the JSON payload in the request
    score = request.json["score"]

    #Retrieve the high score and number of plays from the session
    #If they don't exist, set their default values to 0
    highscore = session.get("highscore", 0)
    xplays = session.get("xplays", 0)

    #increment the number of plays by 1
    session['xplays'] = xplays + 1
    #Update the high score if the new score is greater than the previous high score
    session['highscore'] = max(score, highscore)

    #Return a JSON response containing whether the new score broke the previous record
    return jsonify(brokeRecord=score > highscore)