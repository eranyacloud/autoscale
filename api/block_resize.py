import requests
from .authonticate import Authonticate
from . import config
import json
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse



class BlockResize():
    def __init__(self,instance_id,project_id=None,volume_id=None):
        self.instance_id = instance_id
        self.project_id = project_id
        self.volume_id = volume_id


    def get_instance(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            instance_ref = self.instance_id
            url = f"http://{config.cloud_ip}:8774/v2.1/servers/{instance_ref}"
            response = requests.get(url,headers=header,verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful!")
                return response.json()
            else:
                print("Get request failed with status code:", response.status_code)
                return error_result(response.status_code,response.status_code)
                #error_result("Error","check the flavor or instance")
        except Exception as err:
            print("block_resize:",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)

    def do_resize_block(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            instance_ref = self.instance_id
            project_id = self.project_id
            volume_id = self.volume_id
            body = {
                    "os-extend": {
                     "new_size": 30
                     }
            }
            url = f"http://{config.cloud_ip}:8776/v3/{{project_id}}/volumes/{{volume_id}}/action"
            response = requests.post(url,headers=header,data = json.dumps(body),verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful!")
                return response.json()
            else:
                print("Get request failed with status code:", response.status_code)
                return error_result(response.status_code,response.status_code)
                #error_result("Error","check the flavor or instance")
        except Exception as err:
            print("block_resize:",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)





def error_result(status, message):
    results = {
        "badRequest": {
            "code": status,
            "message": message
        }
    }
    return json.dumps(results)


def success_result(status,message):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    results["data"]['message']=message
    return JSONResponse(results)
