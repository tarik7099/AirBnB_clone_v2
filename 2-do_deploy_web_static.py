#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers using the function do_deploy.
"""

from fabric.api import *
from os.path import exists

env.hosts = ['100.26.241.34', '54.90.13.18']  # Replace with your web server IPs
env.user = 'ubuntu'  # Replace with your username

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

        # Remove existing files in the target directory
        run('sudo rm -rf {}'.format(target_path))

        # Extract the new archive
        run('sudo mkdir -p {}'.format(target_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(file_name, target_path))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(file_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current linked to the new version
        run('sudo ln -s {} /data/web_static/current'.format(target_path))

        return True
    except Exception as e:
        print(e)
        return False 
