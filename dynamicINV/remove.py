from ansible.module_utils.basic import AnsibleModule
import json
import collections
def merge_dicts(dicts):
    temp_list=[]
    result = collections.defaultdict(list)
    for d in dicts:
        for k, v in d.items():
            result[k].append(v)
    for v in dict(result):
        temp_list.append(v+"-"+",".join(result[v]))
    return temp_list

def processing(params):
    temp_list=[]
    cleansed_list=[]
    if len(params['payload']) > 0:
        for temp in params['payload']:
            temp_list.append(json.loads('{"'+temp.split("-")[0]+'":"'+temp.split("-")[1]+'"}'))
        cleansed_list=merge_dicts(temp_list)
        return 0,cleansed_list
    else:
        return 1,"Device Group is 0, Hence Exiting.."


def remove_duplicate_grp():
    module_args = dict(payload=dict(type='dict', required=True),chunk_len=dict(type='int',required=True,Default='10'),gitlab_url=dict(type='str',required=True),access_token=dict(type='str',required=True),gitlab_project_id=dict(type='int',required=True))
    result = dict(changed=False,msg='')
    module = AnsibleModule(argument_spec=module_args,supports_check_mode=False)
    status_code,status_msg=processing(module.params)
    if int(status_code) == 0:
        result['changed'] = True
        result['msg'] = status_msg
        module.exit_json(**result)
    elif int(status_code) == 2:
        result['changed'] = True
        result['msg'] = "Error while cretaing/updating gitlab pipeline schedule."
        module.fail_json(**result)
    else:
        result['changed'] = False
        result['msg'] = status_msg
        module.fail_json(**result)

if __name__ == '__main__':
    remove_duplicate_grp()
