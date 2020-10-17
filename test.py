from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def index():
    #conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True) #Redis 연결
    conn = redis.from_url(os.environ['REDISCLOUD_URL']) # redis heroku addon 연결
    ret_str = conn.get("hello_redis")
    return ret_str

@app.route('/list', methods=['GET','POST'])
def get_list():

    #conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True) #Redis 연결
    conn = redis.from_url(os.environ['REDISCLOUD_URL']) # redis heroku addon 연결    

    redis_key = "my_sp_list_"+datetime.today().strftime('%Y%m%d')
    redis_data = conn.get(redis_key)
    res = dict(json.loads(redis_data))  

    print("list 조회결과:" + str(res))

    return jsonify(res)    

# 1개 value 조회
@app.route('/getValue', methods=['GET','POST'])
def get_value():

    params = request.get_data().decode('utf-8')
    # params = request.get_json()
    if len(params) == 0:
      redis_key = "my_sp_list_"+datetime.today().strftime('%Y%m%d')
    else :
      redis_key = params

    print('getValue 수신 파라메터:' + str(params))  

    #conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True) #Redis 연결
    conn = redis.from_url(os.environ['REDISCLOUD_URL']) # redis heroku addon 연결    
    redis_data = conn.get(redis_key)
    res = dict(json.loads(redis_data)) 

    print("getValue 조회결과:" + str(res))

    return jsonify(res) 

# 모든 key 목록 조회
@app.route('/getKeys', methods=['GET','POST'])
def get_keys():
    #conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True) #Redis 연결
    conn = redis.from_url(os.environ['REDISCLOUD_URL']) # redis heroku addon 연결    
    redis_data = conn.keys()

    print("getKeys 조회결과:" + str(redis_data))

    return jsonify(redis_data)

@app.route('/save', methods=['GET','POST'])
def save_list():
    req_data = request.get_json()
    print(req_data)
    #conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True) #Redis 연결
    conn = redis.from_url(os.environ['REDISCLOUD_URL']) # redis heroku addon 연결    
    redis_key = "my_sp_list_"+datetime.today().strftime('%Y%m%d')
    if req_data:
      json_data = json.dumps(req_data)
    else :
      json_data = '{"json":"null"}'
    conn.set(redis_key, json_data)
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True, port=4000)   