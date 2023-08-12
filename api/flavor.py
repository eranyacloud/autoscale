import requests
from .authonticate import Authonticate
from . import config
import json
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse



class Flavor():
    def __init__(self):
        pass


    def get_flavor(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:8774/v2.1/flavors/detail"
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
