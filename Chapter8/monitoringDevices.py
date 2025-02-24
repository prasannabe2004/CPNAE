from netmiko import ConnectHandler
import psutil
import time

def gather_processing_metrics(device):
    """ Monitoring CPU and Memory utilization """
    connection = ConnectHandler(**device)
    cpu_out = connection.send_command('show processes cpu')
    mem_out = connection.send_command('show processes memory')
    return cpu_out, mem_out

def gather_config_data(device):
    """ Collect device configuation info """
    connection = ConnectHandler(**device)
    running_config = connection.send_command('show running-config')
    interfaces = connection.send_command('show interfaces')
    return running_config, interfaces

def gather_time_metrics(device):
    """ Monitoring time-based metrics like uptime and response time """
    connection = ConnectHandler(**device)
    uptime = connection.send_command('show version | include uptime')
    response_times = []
    for _ in range(5):
        start_time = time.time()
        connection.send_command('show clock')
        end_time = time.time()
        response_times.append(end_time - start_time)
    return uptime, sum(response_times)/len(response_times)

