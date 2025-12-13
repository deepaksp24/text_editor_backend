import eventlet

eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app,async_mode='eventlet', cors_allowed_origins="*",logger=True, engineio_logger=True)

# in-memory doc storage (simple)
documents = {}

def updateDoc(doc_id, changes_map):
    if doc_id not in documents:
        documents[doc_id] = { "content": "", "gridMap": {} }

    for key, value in changes_map.items():
        if value is None:
            if key in documents[doc_id]['gridMap']:
                del documents[doc_id]['gridMap'][key]
        else:
            documents[doc_id]['gridMap'][key] = value

@app.route("/", methods=["GET"])
def create():
    return {"status": True, "message": "sever on"}

@app.route("/create", methods=["POST"])
def create_doc(doc_id):
    documents[doc_id] = {
                            "content": "",
                            "gridMap": {}
                        }
    return {"status": True, "message": "Doc created"}

@socketio.on("join")
def handle_join(data):
    doc_id = data["doc_id"]
    join_room(doc_id)
    create_doc(doc_id)
    emit("load", {
        "content": documents[doc_id]["content"],
        "gridMap": documents[doc_id]["gridMap"]
    })

@socketio.on("edit")
def handle_edit(data):
    doc_id = data["doc_id"]
    changes = data["changes"] 
    updateDoc(doc_id, changes)
    emit("update", changes, room=doc_id, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000,debug=True)
