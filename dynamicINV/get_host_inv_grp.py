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

- name: Download the code from the inventory
      uri:
        url: "{{gitlab_url}}api/v4/projects/{{gitlab_projectid}}/packages/generic/AristaInventory/LATEST/inventory_new.ini"
        method: GET
        headers:
          PRIVATE-TOKEN: 'glpat-hSdAURpV5FWwRq4dpjx9'
        status_code: 200
        return_content: true
      register: data
    - name: Write to the File
      lineinfile:
        path: "inventory_new.ini"
        line: "{{ data.content }}"
        state: present
        create: true
    - name: Get Inventory by Group
      get_hosts_inv_grp:
        inventory_filename: "inventory_new.ini"
        device_grp: "{{device_grp}}"
      register: result
    - debug:
        var: result
