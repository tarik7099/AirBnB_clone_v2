#!/usr/bin/python3
"""
    Fabric script that creates and distributes an archive
"""
from fabric.contrib.files import exists  # Import exists function

from fabric.api import *
from fabric.operations import run, put, sudo, local
from datetime import datetime
import os
env.hosts = ['100.26.241.34', '54.90.13.18']

created_path = None


def do_pack():
    """
        generates a .tgz archine from contents
    """
    time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_nm = "versions/web_static_{}.tgz".format(time)
    try:
        local("mkdir -p ./versions")
        local("tar --create --verbose -z --file={} ./web_static"
              .format(file_nm))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
        using fabric to distribute archive
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        pat = "/data/web_static/releases"
        put("{}".format(archive_path), "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("mkdir -p {}/{}/".format(pat, folder[0]))
        new_arv = '.'.join(folder)
        run("tar -xzf /tmp/{} -C {}/{}/"
            .format(new_arv, pat, folder[0]))
        run("rm /tmp/{}".format(archive))
        run("mv {}/{}/web_static/* {}/{}/"
            .format(pat, folder[0], pat, folder[0]))
        run("rm -rf {}/{}/web_static".format(pat, folder[0]))
        run("rm -rf /data/web_static/current")
        run("ln -sf {}/{} /data/web_static/current"
            .format(pat, folder[0]))
        return True
    except Exception:
        return False


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
    result = do_deploy(new_archive_path)
    return result
