#!/usr/bin/python3
#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes
an archive to your web servers
"""
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes..
     """

from fabric.api import env, put, run
from os.path import exists
from fabric.contrib.files import exists

env.hosts = ['100.26.241.34', '54.90.13.18']

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    """ distributes an archive to my web servers """
    if not exists(archive_path):
        return False
    filename11 = archive_path.split('/')[-1]
    no_tgz = "/data/web_static/releases/{}".format(filename11.split('.')[0])
    tmep = "/tmp/" + filename11

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

