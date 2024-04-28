import requests
import json

class Http:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        pass
    # get请求
    def get(self,url):
        response = requests.get(url)
        if 'application/json' in response.headers['Content-Type']:
            html = response.json()  # 如果响应内容是JSON格式，则使用.json()解析
        else:
            html = response.text
        return html
    # post请求
    def post(self,url,data_dict):
        data_json = json.dumps(data_dict)
        response = requests.post(url, data=data_json, headers=self.headers)
        return response.text