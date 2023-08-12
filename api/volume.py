import requests
from .authonticate import Authonticate
from . import config
import json
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse



class Volume():
    def __init__(self,snapshot_id=None,size=None,volume_id=None):
        self.snapshot_id = snapshot_id
        self.size = size
        self.volume_id = volume_id

    def Create_volume_from_snapshot(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:8774/v2.1/os-volumes"
            body = {
                "volume": {
                "snapshot_id": self.snapshot_id,
                #"name": "new_volume_name",
                "size": self.size
                }
            }
            response = requests.post(url,headers=header,data=json.dumps(body),verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful->Create_volume_from_snapshot!")
                return response.json()
            else:
                print("Get request failed with status code:", response.text)
                return error_result(response.status_code,response.text)
                #error_result("Error","check the flavor or instance")
        except Exception as err:
            print("e2",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)


    def get_volume(self):
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:8774/v2.1/os-volumes/{self.volume_id}"
            response = requests.get(url,headers=header,verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful->get_volume!")
                return response.json()
            else:
                print("Get request failed with status code:", response.text)
                return error_result(response.status_code,response.text)


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
