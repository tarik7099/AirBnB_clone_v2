#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes
an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.87.222.204', '100.25.194.62']

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        file_no_ext = file_name.split('.')[0]
        dest_folder = '/data/web_static/releases/{}'.format(file_no_ext)
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(dest_folder))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, dest_folder))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}'.format(dest_folder, dest_folder))
        run('rm -rf {}/web_static'.format(dest_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(dest_folder))
        return True
    except Exception:
        return False
