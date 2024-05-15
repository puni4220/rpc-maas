import argparse
import os
import subprocess
from maas_common import metric_bool
from maas_common import print_output

def check(args):
    """check if a physical port exists in ovs bridge
       provided as an argument"""

    #define the name for the check
    name = "ovs-bridge_physical_port_status"
    #list the contents of the directory /sys/class/net
    os_physdev_dir_path = "/sys/class/net"
    os_physdev_list = os.listdir(os_physdev_dir_path)

    #define the command to run to list the ports in ovs bridge
    ovs_port_list_cmd = ['sudo', 'ovs-vsctl', 'list-ports', args.bridge]

    #try to run the command to list the ports
    try:
        output = subprocess.check_output(ovs_port_list_cmd)
        #convert the output to list of strings
        ovs_br_ports = output.decode('utf-8').strip().split('\n')
    except subprocess.CalledProcessError:
        #if the command fails we need to return false to metric_bool
        metric_bool(name, False)
        #return from the function once the command fails 
        return

    #iterate over the list of devices on the node
    for os_physdev in os_physdev_list:
        #check if os_physdev is present in the list of bridge port
        if os_physdev in ovs_br_ports:
            #there is a match return true to metric_bool
            metric_bool(name, True)
            #return from the function as a match is found
            return 

    #if there is no match return false to metric_bool
    metric_bool(name, False)

def main(args):
    check(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check if there is a physical port in ovs bridge')
    parser.add_argument('--telegraf-output',
                        action='store_true',
                        default=False,
                        help='Set the output format to telegraf')
    parser.add_argument('--bridge',
                        default='br-ex',
                        help='name of the ovs bridge')
    args = parser.parse_args()
    with print_output(print_telegraf=args.telegraf_output):
        main(args)
