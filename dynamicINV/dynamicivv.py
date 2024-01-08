import gitlab
from ansible.module_utils.basic import AnsibleModule
import traceback
import sys
import itertools
import numpy as np

def chunk_list(my_list, chunk_size):
    f_list=[]
    while my_list:
        chunk, my_list = my_list[:chunk_size], my_list[chunk_size:]
        f_list.append(chunk)
    return f_list


def check_gitlab_schedule(current_device_grp,params):
    # Cron Schedule Config
    days=[2] # Schedules every day on tuesday and wednesday (picked randomly)
    hours=np.arange(1,5) # Schedule betsween 2am to 6 am (picked randomly)
    existing_device_grp=[]
    cur_pipeline_details=[]
    try:
        gl = gitlab.Gitlab(url=params['gitlab_url'], private_token=params['access_token'])
        gl.auth()
        project = gl.projects.get(params['gitlab_project_id'])
        pipline_sche = project.pipelineschedules.list()
        if len(pipline_sche) <= 250:
            for schedule in pipline_sche:
                sch_details = project.pipelineschedules.get(schedule.id)
                if sch_details.attributes['active'] == True:
                    variables=sch_details.attributes['variables']
                    for variable in variables:
                        if variable['key'] == 'device_grp':
                            existing_device_grp.append(variable['value'])
                            cur_pipeline_details.append(dict(pipeline_id=schedule.id,device_grp=variable['value']))
            delete_schedules=set(existing_device_grp)-set(current_device_grp)
            for delete in delete_schedules:
                for details in cur_pipeline_details:
                    if delete in details['device_grp']:
                        sched = project.pipelineschedules.get(details['pipeline_id'])
                        sched.delete()
            create_schedules =  set(current_device_grp) - set(existing_device_grp)
            for schedule in create_schedules:
                   cron_schedule=str(np.random.randint(0,60))+" "+str(hours[np.random.randint(3)])+" * * "+str(days[np.random.randint(1)])
                   pipeline_schedule_details=dict(
                            ref='main',
                            description="Pipeline Schedule for Arista Device Group:"+str(schedule),
                            cron=cron_schedule,
                            active='true'
                   )
                   sched = project.pipelineschedules.create(pipeline_schedule_details)
                   sch_var=dict(key='device_grp',value=schedule)
                   sched.variables.create(sch_var)
                   sched.take_ownership()
                   sched.save()
            return 0,"All Pipeline Schedules are updated as per the current inventory"
        else:
            print("error:" + "Unexpexted amount of pipeline schedules found.Hence exiting")
            file = open("gitlab_error.log", "w")
            file.write(str("Unexpexted amount of pipeline schedules found.Hence exiting"))
            file.close()
            return 1, "Unexpexted amount of pipeline schedules found.Hence exiting"
    except Exception as e:
        print("error:"+str(e))
        file=open("gitlab_error.log","w")
        file.write(str(e))
        file.close()
        return 1,"Error While Creating/Updating schedules.Error"+str(e)

def processing(params):
    content = ""
    total_device_grp=[]
    if params['payload'] is not None:
        try:
            data=params['payload']
            for d in data['results']:
                device_grp=d['item'].split("-")[0]
                sql_results = list(itertools.chain.from_iterable(d['query_results'][0][0]))
                f_list = chunk_list(sql_results,params['chunk_len'])
                if len(f_list) >= 0:
                    for i in range(0, len(f_list)):
                        content = content + '''[''' + str(device_grp) + str(i + 1) + ''']\n'''
                        for item in f_list[i]:
                            content = content + item + "\n"
                        total_device_grp.append(str(device_grp) + str(i + 1))
            status,status_message=check_gitlab_schedule(total_device_grp,params)
            if status == 0:
                return 0,content
            else:
                return 2,content
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
        return 1,str(''.join(tb.format_exception_only()))
    else:
        return 1,"No Payload Found."
def dynamic_inv():
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
        result['msg'] = "Error while creating/updating gitlab pipeline schedule."
        module.fail_json(**result)
    else:
        result['changed'] = False
        result['msg'] = status_msg
        module.fail_json(**result)

if __name__ == '__main__':
    dynamic_inv()
