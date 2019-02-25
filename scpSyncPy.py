# -*- coding:utf-8 -*-
# see method 1 in link : https://blog.csdn.net/yaningli/article/details/78223361
# modify code to adapt py3,190208,
# most active code,190209,
# functioning fine,V2 190210,
# V2.1，removed additional useless codes,

import paramiko
from scp import SCPClient #method 2
import os,sys,time
import pexpect
from pexpect import popen_spawn
from contextlib import closing
import argparse

def ssh_scp_put(ip,port,user,password,local_file,remote_file):
    print("11连接已建立")
    ssh = paramiko.SSHClient()
    print("12连接已建立")
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("13连接已建立")
    ssh.connect(ip, 22, 'root', password)
    print("13连接已建立")
    a = ssh.exec_command('date')
    print("15连接已建立")
    stdin, stdout, stderr = a
    print("16连接已建立")
    print( stdout.read())
    print("17连接已建立")
    # sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    # sftp = ssh.open_sftp()
    # sftp.put(local_file, remote_file)

def ssh_scp_get(ip, port, user, password, remote_file, local_file):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, 'root', password) #连接
    print("21连接已建立")

    a = ssh.exec_command('date') #执行命令1：date
    (stdin, stdout, stderr) = a
    print( "24远程机器时间：",stdout.read() )

    ssh_session = ssh.get_transport().open_session()  # 打开会话
    command = 'ls'
    if ssh_session.active:
        ssh_session.exec_command(command) #执行命令2： ls
        print("245当前目录下ls结果：",ssh_session.recv(1024))
    print("2450命令2已执行")

    # from scp import SCPClient #method 2
    scpclient_session = SCPClient(ssh.get_transport(), socket_timeout=15.0)
    remotepath = '/var/testforsync/testSync.txt'
    #localpath1 = 'get.txt'
    scpclient_session.get(remotepath) # 不设置localpath的话，默认本地目录是本py脚本所在的本地目录.
    print("24710内部传输完成")


#### main code
# parameter definition
ip = '192.168.0.202'  #"远端主机的IP地址："
password = 'password' #"远端主机的密码："
port = 22
user = 'root'
print("ip =", ip, ",password =", password)

while True:
    print ( '''
    -------欢迎使用 scp software--------
    上传文件请输入  [ 1 ]:
    下载文件请输入  [ 2 ]:
    退出SCP请输入   [ q ]:
    ------------------------------------
    ''' )
    # choice = input("请输入 [ ]")
    choice = '2'
    if choice == "1":
        local_file = input("请输入本地文件的绝对路径：")
        remote_file = input("请输入文件上传的绝对路径：")
        ssh_scp_put(ip,port,user,password,local_file,remote_file)
        print("01已完成文件上传")

    elif choice == "2":
        # remote_file = input("请输入远端文件的绝对路径：")
        # local_file = input("请输入要放到本地的绝对路径：")
        remote_file = '/var/testforsync/'
        local_file = 'D:/'
        ssh_scp_get(ip,port,user,password,remote_file,local_file)
        print("02已完成文件下载")

    elif choice == "q":
        print ("03感谢使用，再见")
        exit()

    else:
        print ("00输入错误，请重新输入：")