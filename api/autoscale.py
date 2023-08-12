import requests
from .authonticate import Authonticate
from .flavor import Flavor
from .block_resize import BlockResize
from . import config
import json
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse

class AutoScale():
    def __init__(self,instance_id=None,flavor_id=None,disk_type="block"):
        self.instance_id = instance_id
        self.flavor_id = flavor_id
        self.disk_type = disk_type


    def resize_instance(self):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            try:
                ############## get flavor ###############
                flavor_info=Flavor()
                flavor_get = flavor_info.get_flavor()
                sorted_data = sorted(flavor_get["flavors"], key=lambda x: (x["disk"], x["vcpus"], x["ram"]))
                #print("sorted_data:",sorted_data)
                mapped_data = [
                {
                    "id": item["id"],
                    "ram": item["ram"],
                    "disk": item["disk"],
                    "vcpus": item["vcpus"]
                }
                for item in sorted_data
            ]
            # Print the mapped data
                index_plus = 0
                flavor_array = []
                for index,item in enumerate(mapped_data):
                    flavor_array.append(item)
                    if item.get('id') == self.flavor_id:
                        index_plus = index
                        #print(item,index)

            except Exception as err:
                print("error flavor==>",err)


            ############## resize instance ##########


            instance_ref = self.instance_id
            flavor_id = self.flavor_id
            url = f"http://{config.cloud_ip}:8774/v2.1/servers/{instance_ref}/action"
            body = {
                "resize" : {
                    "flavorRef" : flavor_array[index_plus+1].get('id'),
                    "OS-DCF:diskConfig": "AUTO"
                }
            }

            if (self.disk_type == "local"): #local
                response = request_http(url,header,body)
            elif (self.disk_type == "block"):  # block
                response = request_http(url,header,body)
                # block_resize_info=BlockResize(self.instance_id)
                # block_get = block_resize_info.get_instance()
                # block_id = block_get["server"]["os-extended-volumes:volumes_attached"][0].get('id')
                # project_id = block_get["server"]["tenant_id"]

                #response = request_http(url,header,body)
            else:
                return error_result("400","please check the input")

            #response = requests.post(url,headers=header,data = json.dumps(body),verify=False)

            if response.status_code == 200 or response.status_code == 202:
                print("POST request was successful!")
                return success_result("success","the vm is resizing with new flavor")
            else:
                print("POST request failed with status code:", response.status_code)
                return json.loads(response.text)

        except Exception as err:
            print("e1-->",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)


    def get_snapshot(self):
        url = f"https://{config.cloud_ip}:8774/v2.1/os-snapshots"
        response = requests.get(url)
        if response.status_code == 200:
            print("GET request was successful!")
            print("Response JSON:", response.json())
            return response.json()  # Return the JSON data
        else:
            print("GET request failed with status code:", response.status_code)
            return None  # Return None to indicate failure
            return json.loads(response.text)





def request_http(url,header,data=None):
    response = requests.post(url,headers=header,data = json.dumps(data),verify=False)
    return response

def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return results


def success_result(status,message):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    results["data"]['message']=message
    return JSONResponse(results)
