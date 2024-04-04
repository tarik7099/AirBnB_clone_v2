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

#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers using the function do_deploy.
"""

from fabric.api import *
from os.path import exists

env.hosts = ['52.87.222.204', '100.25.194.62']  # Replace with your web server IPs

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        file_name = archive_path.split('/')[-1]
        file_prefix = file_name.split('.')[0]
        target_path = '/data/web_static/releases/{}/'.format(file_prefix)
        run('mkdir -p {}'.format(target_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, target_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current linked to the new version
        run('ln -s {} /data/web_static/current'.format(target_path))

        return True
    except Exception as e:
        print(e)
        return False

def deploy():
    """ creates and distributes an archive to your web servers
    """
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
    result = do_deploy(new_archive_path)
    return result

