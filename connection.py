import paramiko
host_list = open("list.txt")
port = 22
username = "root"
password = "VerintESX"
#command = "/usr/lib/vmware/vmkmgmt_keyval/vmkmgmt_keyval -d"
hosts = []
for host in host_list.readlines():
        hosts.append(host.replace("\n", ''))

hba_list = open("hba_list.txt", "w")


for host in hosts:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    command = "/usr/lib/vmware/vmkmgmt_keyval/vmkmgmt_keyval -d"
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    if "vmhba0/vmw_ahci" in lines[-2]:
        line = lines[-3]
    elif "vmhba0" in lines[-2]:
        line = lines[-2]
    elif "vmhba1" in lines[-2]:
        line = lines[-2]
    elif "vmhba1" in lines[-1]:
        line = lines[-1]
    elif "qedf0" in lines[-2]:
        line = lines[-2]
    elif "vmhba2" in lines[-3]:
        line = lines[-3]
    elif "vmnic" in lines[-2]:
        line = lines[-1]
    hba = line[20::]
    hba = hba.replace("\n", '')
    command = f"/usr/lib/vmware/vmkmgmt_keyval/vmkmgmt_keyval -l -i {hba}"
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    hba_list.write(f"{host} - {hba} - {lines}\n")
host_list.close()
hba_list.close()