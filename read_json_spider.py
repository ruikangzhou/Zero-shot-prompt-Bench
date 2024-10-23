import json


def read_json(id):
    with open('D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_new.json','rb') as f:
        d = json.load(f)
        return d[id]['question'],d[id]['SQL'], d[id]['db_id'],d[id]['difficulty']#here id = real id - 1, altogether 1034

def read_json_evidence(id):
    with open('D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_new.json','rb') as f:
        d = json.load(f)
        return d[id]['question'],d[id]['evidence'],d[id]['SQL']#here id = real id - 1

read_json(1)