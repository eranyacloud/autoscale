import requests
from .authonticate import Authonticate
from . import config
import json
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse



class Octavia():
    def __init__(self,project_id=None,instance_id=None,pool_id=None):
        self.project_id = project_id
        self.instance_id = instance_id
        self.pool_id = pool_id

        # https://{{ip}}:9876/v2/lbaas/loadbalancers?project_id=ebc2f28a985c4a90a1d7fc63e2d58d00
    def get_octavia(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:9876/v2/lbaas/loadbalancers?project_id={self.project_id}"
            response = requests.get(url,headers=header,verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful!->get_flavor")
                return response.json()
            else:
                print("Get request failed with status code:", response.status_code)
                return error_result(response.status_code,response.status_code)
                #error_result("Error","check the flavor or instance")
        except Exception as err:
            print("e2",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)

    def get_pools(self,pool_id):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:9876/v2/lbaas/pools/{pool_id}/members"
            response = requests.get(url,headers=header,verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful!->get_flavor")
                return response.json()
            else:
                print("Get request failed with status code:", response.status_code)
                return error_result(response.status_code,response.status_code)
                #error_result("Error","check the flavor or instance")
        except Exception as err:
            print("e2",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)


    def create_member(self,pool_id,address_ip):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:9876/v2/lbaas/pools/{pool_id}/members"
            body={

                "member": {
                    "name": "web-server-1",
                    "admin_state_up": True,
                    "address": address_ip,
                    "protocol_port": "80"
                }
            }

            response = requests.post(url,headers=header,data=json.dumps(body),verify=False)
            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful!->get_flavor")
                return response.json()
            else:
                print("Get request failed with status code:", response.status_code)
                return error_result(response.status_code,response.status_code)
                #error_result("Error","check the flavor or instance")
        except Exception as err:
            print("e2",err)
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
