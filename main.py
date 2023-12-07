import paramiko
from ansible.module_utils.basic import AnsibleModule
import os

def connect_ssh(hostname,username,password):
    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
    except Exception as e:
        print(format("Error while connecting to %s",hostname,"with Error:%s",e))
        exit(1)
    return client
def cleanup(tmp_file):
    try:
        os.remove(tmp_file)
    except Exception as e:
        print("Error while deleting the temp file")
        exit(1)

def processing():
    global ssh_client
    global scp_client
    tmp_path = "/tmp/" # Intermediate storage before moving to the dest
    try:
        # Required Parameters
        module_args = dict(
            dmf_hostname=dict(type='str', required=True),
            backup_hostname=dict(type='str', required=True),
            dmf_username=dict(type='str', required=True),
            dmf_password=dict(type='str', required=True),
            backup_username=dict(type='str', required=True),
            backup_password=dict(type='str', required=True),
            dmf_backup_filepath=dict(type='str', required=True),
            backup_dest_filepath=dict(type='str', required=True)
        )
        # Loading Ansible Module
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=False
        )
        tmp_path=tmp_path+os.path.basename(module.params['dmf_backup_filepath'])
        if len(module.params) == 8:
            print("Connecting to DMF")
            ssh_client=connect_ssh(module.params['dmf_hostname'],module.params['dmf_username'],module.params['dmf_password'])
            scp_client = ssh_client.open_sftp()
            scp_client.get(module.params['dmf_backup_filepath'],tmp_path)
            if os.path.exists(tmp_path):
                ssh_client = connect_ssh(module.params['dmf_hostname'], module.params['dmf_username'],
                                         module.params['dmf_password'])
                scp_client = ssh_client.open_sftp()
                scp_client.get(module.params['dmf_backup_filepath'], module.params['backup_dest_filepath'])
                cleanup(tmp_path)
                ssh_client.close()
                scp_client.close()
            else:
                print("File Download Failed")
                module.fail_json(msg='Error: SSH Connection was successful, But file download failed.',
                                 changed=False)
        else:
            module.fail_json(msg='Error: Expected parameters are not passed.Please check the ReadMe.Md file', changed=False)
    except Exception as e:
        module.fail_json(msg='Error Occurred while execution,Error Details:'+str(e), changed=False)
    finally:
        ssh_client.close()
        scp_client.close()
    module.exit_json(changed=True, result="File Copy Completed without any issues")
def main():
    processing() # Read the data from ansible - module invoke call (task execution)

if __name__ == '__main__':
    main()