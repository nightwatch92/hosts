from datetime import datetime
import requests
import json
import os
import time

from classes.ipaddr import IpAddr

api_key = os.environ.get('API_KEY')
url = "https://s-platform.api.opendns.com/1.0/events?customerKey={}".format(api_key)

headers = {'content-type': 'application/json'}
requst_data_structure = { 
    "alertTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "deviceId": "",
    "deviceVersion": "",
    "dstDomain": "",
    "dstUrl": "",
    "eventTime": "",
    "protocolVersion": "",
    "providerName": "",
    "disableDstSafeguards": True
}

payload = []

def split_list(alist, wanted_parts=1):
  length = len(alist)
  return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
      for i in range(wanted_parts) ]

with open('../hosts') as fp: 
  content = fp.readlines()
domains = split_list(content, wanted_parts=6)



for domain_chunks in domains:
  payload_chunk = []
  for record in domain_chunks:
    domain = IpAddr(record)
    domain.get_domain()
    # Skip None records
    if domain.domain == None:
      continue
    # Building the payload structure for each record
    requst_data_structure["deviceId"] = domain.device_id
    requst_data_structure['deviceVersion'] = domain.device_version
    requst_data_structure['dstDomain'] = domain.domain
    requst_data_structure['dstUrl'] = domain.domain
    requst_data_structure['eventTime'] = domain.event_time
    requst_data_structure['protocolVersion'] = domain.protocol_version
    requst_data_structure['providerName'] = domain.provider_name

    payload_chunk.append(requst_data_structure.copy())
  payload.append(payload_chunk)

for chunk in payload:
  ###r = requests.post(url, data=json.dumps(chunk), headers=headers)
  print('{0}   {1}'.format(r.status_code))
  print(r.text)
  time.sleep(61)
