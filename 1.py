# data = [
#     {
#         "id": "03504d53-1574-42ec-82fb-0be2ec84812e",
#         "name": "F3_F6",
#         "ram": 8192,
#         "disk": 35,
#         "swap": "",
#         "OS-FLV-EXT-DATA:ephemeral": 0,
#         "OS-FLV-DISABLED:disabled": False,
#         "vcpus": 4,
#         "os-flavor-access:is_public": True,
#         "rxtx_factor": 1.0
#     },
#     {
#         "id": "03504d53-1574-42ec-82fb-0be2ec84812e",
#         "name": "F3_F6",
#         "ram": 8195,
#         "disk": 30,
#         "swap": "",
#         "OS-FLV-EXT-DATA:ephemeral": 0,
#         "OS-FLV-DISABLED:disabled": False,
#         "vcpus": 3,
#         "os-flavor-access:is_public": True,
#         "rxtx_factor": 1.0
#     }
# ]

# # Create a new list of dictionaries with selected attributes
# mapped_data = [
#     {
#         "id": item["id"],
#         "ram": item["ram"],
#         "disk": item["disk"],
#         "vcpus": item["vcpus"]
#     }
#     for item in data
# ]

# # Print the mapped data
# for item in mapped_data:
#     print(item)


import json

input_json = '''{
  "badRequest": {
    "code": 400,
    "message": "When resizing, instances must change flavor!"
  }
}'''

parsed_json = json.loads(input_json)

bad_request_dict = parsed_json["badRequest"]
output_json = json.dumps(bad_request_dict, indent=2)

print(output_json)