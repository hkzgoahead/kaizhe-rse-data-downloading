
# only use download mode (ssh_scp_get)

import paramiko
from scp import SCPClient #method 2
import logging
import sys

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# Upload files to RSE
def ssh_scp_put(ip,port,user,password,local_file,remote_file):
    logging.basicConfig(filename='RSE_SSH_connection_Upload.log', level=logging.INFO)
    # start ssh connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    """
    # get system time at the RSE
    rse_time = ssh.exec_command('date')
    stdin, stdout, stderr = rse_time
    logging.info('start ssh: ',stdout.read())
    """
    try:
        ssh.connect(ip, 22, 'root', password)
        logging.info('ssh connection established')
    except AuthenticationException:
        logging.info('Authentication Failed')

    #upload files to rse
    logging.info('uploading banned')

    #end the transport
    """
    rse_time = ssh.exec_command('date')
    stdin, stdout, stderr = rse_time
    logging.info('end ssh: ',stdout.read())
    """
    ssh.close()

# Download files to local directory
def ssh_scp_get(ip, port, user, password, remote_file, local_file):
    logging.basicConfig(filename='RSE_SSH_connection_Download.log', level=logging.INFO)
    # start ssh connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, 22, user, password)
        logging.info('ssh connection established')
    except AuthenticationException:
        logging.info('Authentication Failed')
    
    #"""
    # get system time at the RSE
    logging.info('Download started at:')
    stdin, stdout, stderr = ssh.exec_command('date')
    stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    for line in lines:
        logging.info(line)
    #"""
    
    # from scp import SCPClient #method 2
    scpclient_session = SCPClient(ssh.get_transport(), socket_timeout=15.0, progress=progress)
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



# In[4]:


# main code
# parameter definition
ip = '192.168.0.202' 
password = 'password' 
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
choice = '2'
if choice == "1":
    local_file = input("Enter local file directory：")
    remote_file = input("Enter RSE file directory：")
    ssh_scp_put(ip,port,user,password,local_file,remote_file)
    print('Uploaded successfully')

# Only use download mode
elif choice == "2":
    #remote_file = input("Enter directory of RSE data file: ")
    remote_file = '/var/testforsync/149.txt'
    #local_file = input("Enter download directory: ")
    #Edit your local folder for testing here:
    #local_file = '/Users/kaizhehou/Downloads/scpArada'    
    local_file = 'C:/Users/houkz/Desktop/kaizhe-rse-data-downloading-master/kaizhe-rse-data-downloading-master'
    ssh_scp_get(ip,port,user,password,remote_file,local_file)
    print('Downloaded successfully')

elif choice == "q":
    print ('Script exited')
    exit()

else:
    print ('Please type again')      
    



