"""
--------------------------------------------------------
Licensed under the terms of the BSD 3-Clause License
(see LICENSE for details).
Copyright © 2025, A.A. Suvorov
All rights reserved.
--------------------------------------------------------
"""
import socket
import requests


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ssh_ip = s.getsockname()[0]
        s.close()
        return ssh_ip
    except Exception as e:
        print(e)
        return None


def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']
