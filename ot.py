import globals

# globals.versioHistory = {}
state1 = {
    "doc_id": "1",
    "version" : 0,
    "changes": {
        "type": "insert",
        "character": "hello",
        "position": 0,
        "len": 5
    }
}

state2 = {
    "doc_id": "1",
    "version" : 1,
    "changes": {
        "type": "insert",
        "character": "ey",
        "position": 1,
        "len": 2
    }
}

state3 = {
    "doc_id": "1",
    "version" : 1,
    "changes": {
        "type": "insert",
        "character": "?",
        "position": 5,
        "len": 1
    }
}

state4 = {
    "doc_id": "1",
    "version" : 1,
    "changes": {
        "type": "insert",
        "character": "hi",
        "position": 0,
        "len": 2
    }
}

state5 = {
    "doc_id": "1",
    "version" : 1,
    "changes": {
        "type": "delete",
        "position": 2, # first l from 'hello'
        "len": 1
    }
}


def updateDoc(doc_id, change,version):
    if doc_id not in globals.documents:
        globals.documents[doc_id] = {"content": "","version":0}
    if doc_id not in globals.versioHistory:
        globals.versioHistory[doc_id] = {}

    text = globals.documents[doc_id]["content"]
    currentVersion = globals.documents[doc_id]["version"]
    mod_pos = 0
    if version < currentVersion:
        mod_pos = op(doc_id,change,version,currentVersion,globals.versioHistory)

    if change["type"] == "insert":
        
        pos = mod_pos if mod_pos is not None else change["position"]
        text = text[:pos] + change["character"] + text[pos:]
        globals.documents[doc_id]["version"] +=   1
        globals.versioHistory[doc_id][currentVersion] = [change["len"],change["position"]]

    elif change["type"] == "delete":
        pos = mod_pos if mod_pos is not None else change["position"]
        length = change["len"]
        text = text[:pos] +  text[pos + length:]
        globals.documents[doc_id]["version"] +=   1
        globals.versioHistory[doc_id][currentVersion] = [change["len"],-change["position"]]

    globals.documents[doc_id]["content"] = text

def handle_edit(data):
    doc_id = data["doc_id"]
    changes = data["changes"] 
    version = data["version"]
    updateDoc(doc_id, changes,version)
    print("-->",globals.documents[doc_id])

def op(doc_id,change,version,currentVersion,versioHistory):
    postion = 0
    print(versioHistory)
    history = versioHistory.get(doc_id, {})
    for ver in range(version, currentVersion):
        if ver not in history:
            continue
        if history[ver][1] <= change["position"]:
            postion += history[ver][0]
    return change['position'] +  postion


# handle_edit(state1)
# handle_edit(state2)
# handle_edit(state3)
# handle_edit(state4)
# handle_edit(state5)

print(globals.versioHistory)
print(globals.documents)