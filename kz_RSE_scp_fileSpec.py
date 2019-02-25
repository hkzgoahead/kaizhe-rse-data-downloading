# RSE Spat data download
# 2019/2/24 try to download data from 119st

import paramiko
from scp import SCPClient 
import logging
import sys

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# Download files to local directory
def ssh_scp_get(ip, port, user, password, remote_file, local_file):
	# create a logging under the current folder
    logging.basicConfig(filename='RSE_SSH_connection_Download.log', level=logging.INFO)
    # start ssh connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, 22, user, password)
        logging.info('ssh connection established')
    except AuthenticationException:
        logging.info('Authentication Failed')
    
    # get system time at the RSE
    logging.info('Download started at:')
    stdin, stdout, stderr = ssh.exec_command('date')
    stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    for line in lines:
        logging.info(line)
    
    # from scp import SCPClient #method 2
    scpclient_session = SCPClient(ssh.get_transport(), socket_timeout=120.0, progress=progress)
    # remote_path=the data directory in RSE, local_path=the local download folder
    scpclient_session.get(remote_path=remote_file, local_path=local_file) 
    
    #end the transport
    logging.info('Download completed at:')
    stdin, stdout, stderr = ssh.exec_command('date')
    stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    for line in lines:
        logging.info(line)
    
    # file information
    logging.info('File info: ')
    filesize_cmd = 'du -h ' + remote_file
    stdin, stdout, stderr = ssh.exec_command(filesize_cmd)
    stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    for line in lines:
        logging.info(line)
	
    scpclient_session.close()
    ssh.close()


# main code
# parameter definition
# 23 Ave & 119 St
ip = '10.20.0.29' 
password = 'CV2SaveLivescst119' 
port = 22
user = 'root'
print("ip =", ip, ",password =", password)

"""
#while True:  
    print ( '''
    -------Type for --------
    Upload    [ 1 ]:
    Download  [ 2 ]:
    Exit      [ q ]:
    ------------------------
    ''' )   
    choice = input('Please type [1/2/q]')
"""

remote_file = input("Enter directory of RSE data file: ")
#remote_file = '/tmp/usb/spatDataRecording.csv'

#local_file = input("Enter download directory: ")
#Edit your local folder for testing here:  
local_file = 'C:/Users/tonqiu/Downloads/ljc/SpatDataAutoArchive/23ave_119st'
ssh_scp_get(ip,port,user,password,remote_file,local_file)
print('Downloaded successfully')

  
    



