from flask import Blueprint, request
from flask_socketio import join_room, send, emit

import socketio
from .gamemanager import GameManager

game_bp = Blueprint("game", __name__)

gameManager = GameManager()


def check_win(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] is not None:
            return True
    return False

  
@socketio.on('joinGame', namespace='/game')
def onJoin(json):
    gameId = json["gameId"]
    gameManager.createGame(gameId)
    join_room(gameId)
    # send game state and players to joining player
    send(gameId, to=gameId)

    
@socketio.on("doTurn", namespace="/game")
def doTurn(json):
    # call game logic to process then send new game state to players
    # verify player is in room before doing stuff
    gameId = json["gameId"]
    send(gameManager.getGame(gameId).gameState, to=gameId)
    move_index = json.get("moveIndex")
    if move_index is not None and game:
        game["board"][move_index] = "X"
        if check_win(game["board"]):
            emit("gameWin", {"winner": "X"}, to=gameId)
        else:
            # Send updated game state to players
            emit("gameState", {"board": game["board"]}, to=gameId)

            
@socketio.on("sendMessage", namespace="/game")
def sendMessage(json):
    # chat message feature
    # verify player is in room before doing stuff
    gameId = json["gameId"]
    message = json["message"]
    emit("messageBroadcast", json, to=gameId)

@game_bp.route("/game")
def sessionPage():
    return "a"