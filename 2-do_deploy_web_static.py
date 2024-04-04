#!/usr/bin/python3
"""
    Fabric script that creates and distributes an archive
"""
from fabric.api import *
from fabric.operations import run, put, sudo, local
from datetime import datetime
import os
env.hosts = ['100.26.241.34', '54.90.13.18']

created_path = None


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
        new_archive = '.'.join(folder)
        run("tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, pat, folder[0]))
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
