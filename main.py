from api.authonticate import *
from api.autoscale  import  *
from api.autoscale_vm import *
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import  PlainTextResponse, FileResponse, JSONResponse

import requests


app = FastAPI(
    title="AutoScale",
    description="eranyacloud Atoscale Instances and Vm",
    version="0.5.1",
)

class server_mode(BaseModel):
    instance_id: Union[str, None] = Field(default=None, example="af766182-101f-48be-8c80-0027b72c51f6")
    flavor_id: Union[str, None] = Field(default=None, example="af766182-101f-48be-8c80-0027b72c51f6")
    disk_type: Union[str, None] = Field(default=None, example="local/block")



@app.get("/")
def health_check():
    return {"Status": "Ok"}


@app.post("/resize")
def do_resize_instnce(data:server_mode):
    try:
        autoscale = AutoScale(data.instance_id,data.flavor_id,data.disk_type)
        response_resize = autoscale.resize_instance()
        print("response_resize",response_resize)
        return response_resize
    except Exception as err:
        print("ee-->",err)




class instance_mode(BaseModel):
    instance_id: Union[str, None] = Field(default=None, example="af766182-101f-48be-8c80-0027b72c51f6")
@app.get("/instance")
def get_instance(data:instance_mode):
    try:
        autoscale_vm = AutoScaleVm(data.instance_id)
        response_resize = autoscale_vm.get_instance()
        return response_resize
    except Exception as err:
        print("ee-->",err)


@app.get("/get_snapshot")
def get_instance(data:instance_mode):
    try:
        autoscale_vm = AutoScaleVm(data.instance_id)
        response_instance = autoscale_vm.get_instance()
        network_array = []
        for key in response_instance["server"]["addresses"].keys():
            network_array.append(key)
        #print("dynamic_key",network_array)
        autoscale_vm = AutoScaleVm(None,response_instance["server"]["tenant_id"],response_instance["server"]["os-extended-volumes:volumes_attached"][0].get("id"),network_array)
        response_snapshot = autoscale_vm.get_snapshot()

        return response_snapshot

    except Exception as err:
        print("ee-->",err)


@app.post("/autoscale")
def do_autoscale(data:instance_mode):
    try:
        autoscale_vm = AutoScaleVm(data.instance_id)
        response_instance = autoscale_vm.get_instance()
        network_array = []
        for key in response_instance["server"]["addresses"].keys():
            network_array.append(key)
        #print("dynamic_key",network_array)
        autoscale_vm = AutoScaleVm(None,response_instance["server"]["tenant_id"],response_instance["server"]["os-extended-volumes:volumes_attached"][0].get("id"),network_array,response_instance["server"]["flavor"].get("id"))
        response_snapshot = autoscale_vm.get_snapshot()
        volume = {
             "snapshot_id": response_snapshot[0].get("id"),
             "size":response_snapshot[0].get("size")
         }

        autoscale_vm = AutoScaleVm(None,response_instance["server"]["tenant_id"],response_instance["server"]["os-extended-volumes:volumes_attached"][0].get("id"),network_array,response_instance["server"]["flavor"].get("id"),volume)
        response_autoscale = autoscale_vm.do_autoscale()
        print("---------------------------")
        network_key = next(iter(response_autoscale['Network']))  # Get the dynamic key under 'Network'
        ip_address = response_autoscale['Network'][network_key][0]['addr']
##=========================================== Loadbalancer ======================================================
        response_autoscale = autoscale_vm.get_interface(data.instance_id)
        ha = Octavia(project_id=response_instance["server"]["tenant_id"],instance_id=data.instance_id)
        ha_get = ha.get_octavia()
        pool_ids = []
        pool_exsit=[]

        for lb in ha_get['loadbalancers']:
            for pool in lb['pools']:
                pool_ids.append(pool['id'])
        i = 0
        member_array = []
        pool_id = []
        for i in pool_ids:
            member_array.append(ha.get_pools(i))
            pool_id.append(i)

        members_array = {
            "data": member_array,
            "pool_id": pool_id
        }

        for entry in members_array["data"]:
            for member in entry["members"]:
                #https://{{ip}}:9876/v2/lbaas/pools/80887f02-a8ef-4b3a-9763-0f90a34208ca/members
                if member.get("address") == response_autoscale["interfaceAttachments"][0]["fixed_ips"][0].get("ip_address"):
                    for j in members_array["pool_id"]:
                        results = ha.create_member(j,ip_address)
                        print("==>",results)


##====================================================end Loadbalancer code===========================================

        return response_autoscale

    except Exception as err:
        print("ee-->",err)


