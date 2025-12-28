import concurrent
from app import documents,create_doc,handle_edit
from concurrent.futures import ThreadPoolExecutor
doc_id = '1'
print(create_doc(doc_id))

state1 = {
    "doc_id": "1",
    "changes": {
        "type": "insert",
        "character": "hello",
        "position": 0,
        "len": 5
    }
}

state2 = {
    "doc_id": "1",
    "changes": {
        "type": "insert",
        "character": "e",
        "position": 1,
        "len": 1
    }
}

state3 = {
    "doc_id": "1",
    "changes": {
        "type": "insert",
        "character": "?",
        "position": 5,
        "len": 1
    }
}
print(handle_edit(state1))
print(documents)
print(handle_edit(state2))
print(documents)
print(handle_edit(state3))
print(documents)