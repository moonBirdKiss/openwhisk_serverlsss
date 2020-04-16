# 这个action的名字是 process_hail

import couchdb
import time
import requests

gl_times = 1
gl_ow_database = "http://192.168.66.90:8080"

def init_function(_id, url, dbname):

    # 链接数据库
    print("1.0 now the link information is ", _id, url, dbname)
    server = couchdb.Server(url)
    db = server[dbname]
    doc = db[_id]
    print("1.1 now the doc information is", doc)

    # 获得数据，同时打下标签
    data = doc.get("data")

    # start_time = time.time()
    start_time = requests.get(url=gl_ow_database)    
    start_time = float(start_time.content)    

    # 处理数据，同时记录标签
    data = process_data(data)
    end_time = requests.get(url=gl_ow_database)
    end_time = float(end_time.content)

    # 更新数据
    ## 获得此前执行的时间信息
    pre_time_info = doc.get("time")
    print("3.0 now the pre_time is", pre_time_info, "and its type is", type(pre_time_info))

    ## 获得此时的delta_time
    delta_time = doc.get("delta_time")
    print("3.1 now the deltatime is", delta_time, "and its type is", type(delta_time))
    delta_time.append(start_time-pre_time_info[-1][-1])

    ## 跟新此时的pre_time
    pre_time_info.append([start_time, end_time])
    doc = {
        "_id": _id,
        "_rev": doc.get("_rev"),
        "data": data,
        "time": pre_time_info,
        "delta_time": delta_time
    }
    docs = [doc]
    db.update(docs)
    print("4. now the init_funtion is over")
    return data


def process_data(hail_num):
    for i in range(gl_times):
        if hail_num % 2 == 0:
            hail_num = hail_num // 2
        else :
            hail_num = hail_num * 3 + 1
    return hail_num




def main(args):
    myurl = args.get("url", "http://admin:iam123@106.52.174.212:5984")
    dbname = args.get("dbname", "hail_num")
    _id = args.get("_id", "1")
    data = init_function(_id, myurl, dbname)

    # 进行判断，如果为奇数就停止执行，否则就接着执行
    if data == 1:
        return {
            "status" : "even",
            "data": data
        }
    else:
        resp = requests.post(
            # url = "https://192.168.66.200:31001/api/v1/namespaces/guest/actions/helloPy?blocking=0&result=0",
            url = "https://192.168.66.200:31001/api/v1/namespaces/guest/actions/mypython/couchdb_process_hail?blocking=0&result=0",
            auth = ("23bc46b1-71f6-4ed5-8c54-816aa4f8c502", "123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"),
            # json = {
            #     "name": "bill"
            # },
            json = {
                "url": myurl,
                "_id": _id,
                "dbname": dbname
            },
            verify = False
        )
        return {
            "status": "odd",
            "data": data
        }

