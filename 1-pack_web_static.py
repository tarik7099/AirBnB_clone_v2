#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric import task, Connection
from datetime import datetime
from os.path import exists

def do_pack(c):
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(date)
        archive_path = "versions/{}".format(archive_name)
        
        if not exists("versions"):
            c.local("mkdir -p versions")
        
        c.local("tar -czvf {} web_static".format(archive_path))
        
        return archive_path
    except Exception as e:
        print("Error:", e)
        return None
