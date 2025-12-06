import eventlet

eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app,async_mode='eventlet', cors_allowed_origins="*",logger=True, engineio_logger=True)

# in-memory doc storage (simple)
documents = {}

@app.route("/", methods=["GET"])
def create():
    return {"status": True, "message": "sever on"}

@app.route("/create", methods=["POST"])
def create_doc():
    doc_id = request.json.get("doc_id")
    documents[doc_id] = ""
    return {"status": True, "message": "Doc created"}

@socketio.on("join")
def handle_join(data):
    doc_id = data["doc_id"]
    join_room(doc_id)
    emit("load", {"content": documents.get(doc_id, "")})

@socketio.on("edit")
def handle_edit(data):
    doc_id = data["doc_id"]
    content = data["content"]
    documents[doc_id] = content
    emit("update", {"content": content}, room=doc_id, include_self=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000,debug=True)
