import eventlet

eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
import ot
import globals

app = Flask(__name__)
socketio = SocketIO(app,async_mode='eventlet', cors_allowed_origins="*",logger=True, engineio_logger=True)

# in-memory doc storage (simple)
# globals.documents = {}

def updateDoc(doc_id, change):
    if doc_id not in globals.documents:
        globals.documents[doc_id] = {"content": "","version": 0}

    text = globals.documents[doc_id]["content"]

    if change["type"] == "insert":
        pos = change["position"]
        text = text[:pos] + change["character"] + text[pos:]

    elif change["type"] == "delete":
        pos = change["position"]
        length = change["len"]
        text = text[:pos] + text[pos + length:]

    globals.documents[doc_id]["content"] = text


@app.route("/", methods=["GET"])
def check():
    return {"status": True, "message": "sever on"}

@app.route("/create", methods=["POST"])
def create_doc(doc_id):
    globals.documents[doc_id] = {
                            "content": "",
                            "version" : 0
                        }
    return {"status": True, "message": "Doc created"}

@socketio.on("join")
def handle_join(data):
    doc_id = data["doc_id"]
    join_room(doc_id)
    if doc_id not in globals.documents:
        create_doc(doc_id)
    emit("load", {
        "content": globals.documents[doc_id]["content"],
        "version": globals.documents[doc_id]["version"]
    })

@socketio.on("edit")
def handle_edit(data):
    doc_id = data["doc_id"]
    changes = data["changes"] 
    version = data["version"]
    ot.updateDoc(doc_id, changes,version)
    print("-->",globals.documents[doc_id])
    new_version = globals.documents[doc_id]["version"]
    emit(
    "update",
    {
        "changes": changes,
        "version": new_version
    },
    room=doc_id,
    include_self=False
        )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000,debug=True)
