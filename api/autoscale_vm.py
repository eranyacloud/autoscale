import requests
from .authonticate import Authonticate
from .flavor import Flavor
from .networks import Network
from .block_resize import BlockResize
from .volume import Volume
from .octavia import Octavia
from . import config
import json
import time
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse

class AutoScaleVm():
    def __init__(self,instance_id=None,project_id=None,volume_id=None,network=None,flavor_id=None,volume_data=None):
        self.instance_id = instance_id
        self.project_id = project_id
        self.volume_id = volume_id
        self.network = network
        self.flavor_id = flavor_id
        self.volume_data = volume_data



    def get_instance(self):
        self.auth=Authonticate(config.username,config.password)
        header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
        url = f"http://{config.cloud_ip}:8774/v2.1/servers/{self.instance_id}"
        response = requests.get(url,headers=header,verify=False)
        if response.status_code == 200:
            print("GET request was successful!->get_instance")
            return response.json()  # Return the JSON data
        else:
            print("GET request failed with status code:", response.status_code)
            return None  # Return None to indicate failure

    def get_interface(self,instance_id):
        self.auth=Authonticate(config.username,config.password)
        header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
        url = f"http://{config.cloud_ip}:8774/v2.1/servers/{instance_id}/os-interface"
        response = requests.get(url,headers=header,verify=False)
        if response.status_code == 200:
            print("GET request was successful!->get_instance")
            return response.json()  # Return the JSON data
        else:
            print("GET request failed with status code:", response.status_code)
            return None  # Return None to indicate failure


    def get_snapshot(self,project_id):
        self.auth=Authonticate(config.username,config.password)
        header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
        url = f"http://{config.cloud_ip}:8776/v3/{project_id}/snapshots"
        response = requests.get(url,headers=header,verify=False)

        if response.status_code == 200:
            print("GET request was successful!")
            return response.json()["snapshots"]
        else:
            print("GET request failed with status code:", response.status_code)
            return None  # Return None to indicate failure

    def do_autoscale(self,network,volume_data,flavor_id):
        try:
            self.auth=Authonticate(config.username,config.password)
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
            url = f"http://{config.cloud_ip}:8774/v2.1/servers"
            network_info = Network(network[0])
            network_get = network_info.get_network()
            create_volume_info = Volume(volume_data["snapshot_id"],volume_data["size"])
            create_volume = create_volume_info.Create_volume_from_snapshot()

            body = {
                "server" : {
                    "name" : "autoscale",
                    "flavorRef": flavor_id, #flavor_array[index_plus+1].get('id'),
                    "networks" : [{
                        "uuid" : network_get
                    }],
                    "availability_zone": "nova",
                    "block_device_mapping_v2": [{
                        "uuid": create_volume["volume"].get("id"),
                        "source_type": "volume",
                        "destination_type": "volume",
                        "boot_index": 0,
                    }]
                }
            }
            print("body:",body)
            result = ""
            while True:
                get_volume_info = Volume(None,None,create_volume["volume"].get("id"))
                get_volume = get_volume_info.get_volume()
                if get_volume["volume"].get("status")== "available":
                    response = requests.post(url,headers=header,data = json.dumps(body),verify=False)
                    if response.status_code == 200 or response.status_code == 202:
                        print("Get request was successful!->do_autoscale")
                        result = response.json()
                        break  # Exit the loop since your action is complete
                    else:
                        print("Get request failed with status code:", response.status_code)
                        break  # Exit the loop since your action is complete
                time.sleep(60)

            while True:
                self.instance_id = result["server"].get("id")
                status_machine= self.get_instance()
                if status_machine["server"].get("OS-EXT-STS:vm_state") != "building":
                    break
                else:
                    time.sleep(20)  # Add a delay of 60 seconds before the next iteration
            return {
                    "id":status_machine["server"].get("id"),
                    "Network":status_machine["server"].get("addresses"),
                    "status":status_machine["server"].get("OS-EXT-STS:vm_state")}
        except Exception as err:
            print("e1-->",err)
            raise InvalidUsage(error_result("fail","key error missing %s"%err),status_code=400)







def error_result(status, message):
    results = {
        "badRequest": {
            "code": status,
            "message": message
        }
    }
    return results


def success_result(status,message):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    results["data"]['message']=message
    return JSONResponse(results)
