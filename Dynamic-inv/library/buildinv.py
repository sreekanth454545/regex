#!/usr/bin/python

from ansible.module_utils.basic import *
import itertools


def chunk_list(my_list, chunk_size):
    f_list=[]
    while my_list:
        chunk, my_list = my_list[:chunk_size], my_list[chunk_size:]
        f_list.append(chunk)
    return f_list
  


def main():
    
    content=""
    fields = {
        "sql_results": {"default": True,"type": "list"},
        "chunk_len": {"default": True,"type": "int"},
        "device_grp": {"default": True,"type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    try:
        sql_results=list(itertools.chain.from_iterable(module.params['sql_results']))
        f_list=chunk_list(,module.params['chunk_len'])
        if len(f_list) >= 0 :
            for i in range(0,len(f_list)):
                content=content+'''['''+str(module.params['device_grp'])+str(i+1)+''']\n'''
                for item in f_list[i]:
                    content=content+item+"\n"
            module.exit_json(changed=True,result=content)        
        else:
            module.fail_json(msg="List with 0 index",changed=False )
    except Exception as e:
        print("Error:",str(e))
        module.fail_json(msg=str(e),changed=False )

if __name__ == '__main__':
    main()