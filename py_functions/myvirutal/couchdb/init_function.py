# 首先创建第一个action _init_hail
# 这个action的作用是处理couchdb的初始化数据
# 同时调用process_function这个action
import couchdb 
import time
import requests

gl_times = 1
gl_ow_database = "http://192.168.66.90:8080"

def init_function(_id, url, dbname):
    print("**********now the linke information is ", _id, url, dbname)
    print("the _id is ", type(_id))
    server = couchdb.Server(url)
    print("*****************ok 1.1 *****************")
    db = server[dbname]
    print("*****************ok 1.2 *****************")
    _id = str(_id)
    print("the _id is", type(_id))
    doc = db[_id]
    print(doc)

    data = doc.get("data")

    #  start_time = time.time()
    start_time = requests.get(url=gl_ow_database)
    start_time = float(start_time.content)
    print(data)

    # 处理数据
    data = process_data(data)
    print(data)

    # 更新数据
    # end_time = time.time()
    end_time = requests.get(url=gl_ow_database)
    end_time = float(end_time.content)

    doc = {
        "_id": _id,
        "_rev": doc.get("_rev"),
        "data": data,
        "time": [[start_time, end_time]],
        "delta_time": [0]
    }
    docs = [doc]
    db.update(docs)



def process_data(hail_num):
    for i in range(gl_times):
        if hail_num % 2 == 0:
            hail_num = hail_num // 2
        else :
            hail_num = hail_num * 3 + 1
    return hail_num


def main(args):
    my_url = args.get("url", "http://admin:iam123@106.52.174.212:5984")
    dbname = args.get("dbname", "hail_num")
    _id = args.get("_id", "1")
    init_function(_id, my_url, dbname)

    # 调用 process_hail action
    resp = requests.post(
        url = "https://192.168.66.200:31001/api/v1/namespaces/guest/actions/mypython/couchdb_process_hail?blocking=0&result=0",
        auth = ("23bc46b1-71f6-4ed5-8c54-816aa4f8c502", "123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"),
        json = {
            "url": my_url,
            "_id":str(_id),
            "dbname": dbname
        },
        verify = False
    )
    return {
        "staus": "True"
    }
