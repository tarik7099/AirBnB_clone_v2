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

