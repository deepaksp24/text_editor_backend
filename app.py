import eventlet

eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app,async_mode='eventlet', cors_allowed_origins="*",logger=True, engineio_logger=True)

# in-memory doc storage (simple)
documents = {}

def updateDoc(doc_id, change):
    if doc_id not in documents:
        documents[doc_id] = {"content": ""}

    text = documents[doc_id]["content"]

    if change["type"] == "insert":
        pos = change["position"]
        text = text[:pos] + change["character"] + text[pos:]

    elif change["type"] == "delete":
        pos = change["position"]
        length = change["len"]
        text = text[:pos] + text[pos + length:]

    documents[doc_id]["content"] = text


@app.route("/", methods=["GET"])
def create():
    return {"status": True, "message": "sever on"}

@app.route("/create", methods=["POST"])
def create_doc(doc_id):
    documents[doc_id] = {
                            "content": "",
                        }
    return {"status": True, "message": "Doc created"}

@socketio.on("join")
def handle_join(data):
    doc_id = data["doc_id"]
    join_room(doc_id)
    if doc_id not in documents:
        create_doc(doc_id)
    emit("load", {
        "content": documents[doc_id]["content"],
    })

@socketio.on("edit")
def handle_edit(data):
    doc_id = data["doc_id"]
    changes = data["changes"] 
    updateDoc(doc_id, changes)
    # print("-->",documents[doc_id])
    emit("update", changes, room=doc_id, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000,debug=True)
