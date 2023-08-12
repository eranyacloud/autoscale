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


        return response_autoscale

    except Exception as err:
        print("ee-->",err)


