from ansible.module_utils.basic import AnsibleModule
import os
def get_inv_group(inv_filename,device_grp):
    device_list=[]
    try:
        if os.path.isfile(inv_filename):
            file=open(inv_filename,"r")
            content=file.readlines()
            for i in range(0, len(content)):
                if str(content[i].strip()) == device_grp:
                    for j in range(i + 1, len(content)):
                        if str(content[j].strip()) != "":
                            if str(content[j].strip()[0]) == "[" and str(content[j].strip()) != device_grp:
                                return 0,device_list
                            else:
                                device_list.append(content[j].strip())
            file.close()
            if len(device_list) >= 0:
                return 1, "No Matching Device Group Found"
            else:
                return 0,device_list
        else:
            raise FileNotFoundError("{} not found".format(inv_filename))
    except Exception as e:
        return 1,str(e)
    finally:
        file.close()

if __name__ == '__main__':
    module_args = dict(inventory_filename=dict(type='str', required=True), device_grp=dict(type='str', required=True))
    result = dict(changed=False, msg='')
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    try:
        status_code,inv=get_inv_group(module.params['inventory_filename'],module.params['device_grp'])
        if status_code == 0:
            result['msg'] = set(inv)
            result['changed'] = True
            module.exit_json(**result)
        elif status_code == 1:
            result['msg'] = "Error While reading the inventory for grp {},Error:{}".format(module.params['device_grp'],inv)
            result['changed'] = False
            module.fail_json(**result)
    except KeyError as e:
        result['msg'] = str(e)
        result['changed'] = False
        module.fail_json(**result)
