from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    module_args = dict(inventory_filename=dict(type='str', required=True), device_grp=dict(type='str', required=True))
    result = dict(changed=False, msg='')
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    try:
        data_loader = DataLoader()
        inventory = InventoryManager(loader = data_loader,sources=[module.params['inventory_filename']])
        inventory_list=inventory.get_groups_dict()[module.params['device_grp']]
        result['msg'] = inventory_list
        result['changed'] = True
        module.exit_json(**result)
    except KeyError as e:
        result['msg'] = str(e)
        result['changed'] = False
        module.fail_json(**result)
