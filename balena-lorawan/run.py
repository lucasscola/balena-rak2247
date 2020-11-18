#!/usr/bin/python

"""
LoRaWAN gateway for RPi and RAK2247 USB

Author: Lucas Scola

Based on:
https://github.com/balenalabs-incubator/ttn-gateway-balenafin/blob/master/run.py
"""
import os
import os.path
import sys
import time
import uuid
import json
import subprocess

if not os.path.exists("/opt/ttn-gateway/packet_forwarder"):
  print ("ERROR: gateway executable not found. Is it built yet?")
  sys.exit(0)

if os.environ.get('HALT') != None:
  print ("*** HALT asserted - exiting ***")
  sys.exit(0)

# Configure EUI - GW-EUI ENV
if os.environ.get("GW_EUI")==None:
  print("ERROR: Please specify GW_EUI")
  sys.exit(0)
my_eui = os.environ.get("GW_EUI")

print ("GW_EUI:\t"+my_eui)

# Build local_conf
gateway_conf = {}
gateway_conf['gateway_ID'] = my_eui
local_conf = {'gateway_conf': gateway_conf}
with open('/opt/ttn-gateway/local_conf.json', 'w') as the_file:
  the_file.write(json.dumps(local_conf, indent=4))

# Endless loop to reset and restart packet forwarder
while True:
  # Start forwarder
  subprocess.call('/opt/ttn-gateway/packet_forwarder/lora_pkt_fwd/lora_pkt_fwd')
  time.sleep(15)