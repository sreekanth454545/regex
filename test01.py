devices = {
    'device_type': 'generic',
    'host': host,
    'username': username,
    'password': password,
          }
    
conn = netmiko.ConnectHandler(**devices)

command = 'show status'
command2 = 'show network eth0'

print(f'Processing for {host}')

output = conn.send_command(command, expect_string=r'admin:', delay_factor=10)
output2 = conn.send_command(command2, expect_string=r'admin:', delay_factor=10)
