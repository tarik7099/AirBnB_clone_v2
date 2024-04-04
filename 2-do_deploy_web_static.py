#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes..
     """

from fabric.api import env, put, run
from fabric.contrib.files import exists

env.hosts = ['52.87.222.204', '100.25.194.62']  # <IP web-01>, <IP web-02>

def do_deploy(archive_path):
    """ distributes an archive to my web servers """
    if not exists(archive_path):
        return False
    filename11 = archive_path.split('/')[-1]
    no_tgz = "/data/web_static/releases/{}".format(filename11.split('.')[0])
    tmep = "/tmp/" + filename11

    try:
        put(archive_path, temp)
        run("mkdir -p {}".format(no_tgz))
        run("tar -xzf {} -C {}".format(temp, no_tgz))
        run("mv {}/web_static/* {}".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        return True
    except:
        return False

