documents = {}
versioHistory = {}
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
    if doc_id not in documents:
        documents[doc_id] = {"content": "","version":0}
        versioHistory[doc_id] = {}

    text = documents[doc_id]["content"]
    currentVersion = documents[doc_id]["version"]
    mod_pos = 0
    if version < currentVersion:
        mod_pos = op(doc_id,change,version,currentVersion,versioHistory)

    if change["type"] == "insert":
        
        pos = mod_pos if mod_pos else change["position"]
        text = text[:pos] + change["character"] + text[pos:]
        documents[doc_id]["version"] +=   1
        versioHistory[doc_id][currentVersion] = [change["len"],change["position"]]

    elif change["type"] == "delete":
        pos = mod_pos if mod_pos else change["position"]
        length = change["len"]
        text = text[:pos] +  text[pos + length:]
        documents[doc_id]["version"] +=   1
        versioHistory[doc_id][currentVersion] = [change["len"],-change["position"]]

    documents[doc_id]["content"] = text

def handle_edit(data):
    doc_id = data["doc_id"]
    changes = data["changes"] 
    version = data["version"]
    updateDoc(doc_id, changes,version)
    print("-->",documents[doc_id])

def op(doc_id,change,version,currentVersion,versioHistory):
    postion = 0
    print(versioHistory)
    for ver in range(version,currentVersion):
        print(ver)
        if versioHistory[doc_id][ver][1] <= change['position']:
            postion += versioHistory[doc_id][ver][0]
        print("mod",postion)
    return change['position'] +  postion


handle_edit(state1)
handle_edit(state2)
handle_edit(state3)
handle_edit(state4)
handle_edit(state5)

print(versioHistory)
print(documents)