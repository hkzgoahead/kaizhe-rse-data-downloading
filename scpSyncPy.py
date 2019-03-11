
# only use download mode (ssh_scp_get)

import paramiko
from scp import SCPClient #method 2
import logging
import sys

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# Upload files to RSE
'''
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
'''

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
# Reading RSE group into RSE_list
''' 
Instructions:
RSE_group.config (csv file) stores info of available rse devices
RSE_list[0:5]=['RSE_ID', 'RSE_IP', 'RSE_PW', 'RSE_SS', 'SAVLOC']
RSE_SS=SPaT data Status; 0=unavailable; 1=available
SAVLOC=Saving location on the remote computer MJ****F5
RSE_list[5]=['10001', '10.20.2.29', 'CV2SaveLivescst109', '0', 'NA']
ip = RSE_list[i][1]; pw = RSE_list[i][2]; spatStatus = RSE_list[i][3]
'''
RSE_list = ''
with open('RSE_group.config', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if RSE_list == '':
            RSE_list = row
        else:
            RSE_list.append(row)

for info in RSE_list:
	#skip header
	if len(info)!=5:
		continue
	elif info[3] == '0':
		continue
	else:
		#IP & password & SAVLOC input
		ip = info[1]
		password = info[2]
		port = 22
		user = 'root'
		print("IP =", ip, ",Password =", password)
		#"Enter directory of RSE SPaT data file:
		remote_file = '/tmp/usb/spatDataRecording.csv'
		
		#Edit your local folder for testing here:  
		#local_file = 'C:/Users/tonqiu/Downloads/ljc/SpatDataSutoArchiveSyncFolder/SpatDataAutoArchive/10023_23ave_119st'
		local_file = info[4]
		#run scp connection
		ssh_scp_get(ip,port,user,password,remote_file,local_file)
		print('Downloaded successfully')

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
"""   



