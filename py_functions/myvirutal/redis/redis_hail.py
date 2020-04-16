# 由redis的特点，每一个data_process程序使用如下数据存储

# 这样一来，似乎思路也很清楚
# hail:id:data ——string类型
# hail:id:start_time ——list类型
# hail:id:end_time ——list类型
# hail:id:delta_time ——list类型

# 这里是init_function
# 初始情况下，redis 仅仅存储着 hail:id:data
# action名字叫做 redis_hail
import redis
import time
import requests


gl_ow_database = "http://192.168.66.90:8080"

# 参数设定：
# url
# port
# password
# db_name
# db_index
# id
def main(args):
    # 获取链接的信息
    my_url = args.get("url", "106.52.174.212")
    my_port = args.get("port", 6379)
    my_password = args.get("password", "iam123")
    my_db_name = args.get("db_name", "hail")
    my_db_index = args.get("db_index", 0)
    my_id = args.get("id", 1)

    # r = redis.StrictRedis(host="106.52.174.212",port=6379,password="iam123",db=0)
    r = redis.StrictRedis(host=my_url, port=my_port, password=my_password, db=my_db_index)
    des_index = my_db_name + ":" + str(my_id) + ":"

    # 获取上一个function的结果
    data = int(r.get(des_index + "data"))
    start_time = requests.get(url=gl_ow_database)
    start_time = float(start_time.content)

    print(data, type(data))

    # 处理数据
    if data % 2 == 0:
        data = data // 2
    else:
        data = data * 3 + 1

    r.set(des_index+"data", str(data))

    end_time = requests.get(url=gl_ow_database)
    end_time = float(end_time.content)

    end_time_list = r.lrange(des_index + "end_time", 0, -1)
    delta_time = 0

    if len(end_time_list) == 0:
        delta_time = 0
    else:
        delta_time = start_time - float(end_time_list[-1])

    r.rpush(des_index + "start_time", start_time)
    r.rpush(des_index + "end_time", end_time)
    r.rpush(des_index + "delta_time", delta_time)

    print("main...over")
    if data == 1:
        return {
            "status": "True"
        }
    else:
        requests.post(
            url="https://192.168.66.200:31001/api/v1/namespaces/guest/actions/mypython/redis_hail?blocking=0&result=0",
            auth=("23bc46b1-71f6-4ed5-8c54-816aa4f8c502", "123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"),
            json={
                "url": my_url,
                "port": my_port,
                "password": my_password ,
                "db_name": my_db_name,
                "db_index": my_db_index,
                "id": my_id,
            },
            verify=False
        )
        return {
            "status": "False"
        }

