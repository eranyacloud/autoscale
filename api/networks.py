import requests
from .authonticate import Authonticate
from . import config
import json
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse



class Network():
    def __init__(self,network_name):
        self.network_name = network_name


    def get_network(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            # http://{{ip}}:9696/v2.0/subnets
            url = f"http://{config.cloud_ip}:9696/v2.0/networks"
            response = requests.get(url,headers=header,verify=False)

            if response.status_code == 200 or response.status_code == 202:
                print("Get request was successful!->get_network")
                network_uuid =0
                for i in response.json()["networks"]:
                    if i["name"] == self.network_name:
                        network_uuid = i["id"]
                return network_uuid
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
