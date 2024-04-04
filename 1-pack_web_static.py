#!/usr/bin/python3
""" This module contains the function do_pack that generates a .tgz archive
  from the contents of the web_static folder (fabric script) """


from fabric.api import *
from datetime import datetime


def do_pack():
    """
    fabric script
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filen = f"versions/web_static_{date}.tgz"
    res = local(f"sudo tar -cvzf {filen} web_static")
    if res.succeeded:
        return filen
    else:
        return None
