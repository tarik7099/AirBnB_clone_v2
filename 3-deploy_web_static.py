#!/usr/bin/python3
""" This module contains the function do_pack that generates a .tgz archive
  from the contents of the web_static folder (fabric script) """
from os.path import exists

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

env.hosts = ['100.26.241.34', '54.90.13.18']  # Replace with your web server IPs

def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    try:
        if not exists(archive_path):
            print("Error: Archive file does not exist.")
            return False
        
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        remote_dir = "/data/web_static/releases/"

        # Upload archive
        put(archive_path, '/tmp/')

        # Create release directory
        run('mkdir -p {}{}'.format(remote_dir, no_ext))

        # Extract archive
        with run('tar -xzf /tmp/{} -C {}{}'.format(file_name, remote_dir, no_ext)) as result:
            if result.failed:
                print("Error extracting archive:", result)
                return False

        # Remove archive
        run('rm /tmp/{}'.format(file_name))

        # Move files and create symlink
        run('mv {0}{1}/web_static/* {0}{1}/'.format(remote_dir, no_ext))
        run('rm -rf {}{}/web_static'.format(remote_dir, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(remote_dir, no_ext))

        print("Deployment successful.")
        return True
    except CommandException as e:
        print("Command execution failed:", e)
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False

def deploy():
    """ creates and distributes an archive to your web servers
    """
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
    result = do_deploy(new_archive_path)
    return result

