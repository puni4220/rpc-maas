import argparse
import re
import subprocess
from maas_common import metric_bool
from maas_common import print_output 

def check(args):
    """check if the canary flow exists in
       br-int bridge"""

    #define the name for the check
    name = "br-int_canary_flow_status"
       
    #define the canary flow regex which matches
    #output produced by subprocess.check_output()
    #this canary flow regex syntax is tested with
    #openstack version 24.6.2 (Xena) and openstack
    #version 22.4.4 (Victoria)
    canary_flow_regex = ".*, table=23, n_packets=\d+, n_bytes=\d+, .*, priority=0 actions=drop$"

    #define the command to run
    ovs_canary_flow_cmd = ['timeout', '59', 'sudo', 'ovs-ofctl', 
                              'dump-flows', 'br-int', 'table=23']

    #run the command to check the canary flow
    try:
        output = subprocess.check_output(ovs_canary_flow_cmd)
        br_int_canary_flow = output.decode('utf-8').strip().split('\n')[1]
    except subprocess.CalledProcessError:
        #if the command fails return False to metric_bool
        metric_bool(name, False)
        #return from the function if the command fails
        return

       
    #check if the canary flow matches the regex
    if re.match(canary_flow_regex, br_int_canary_flow):
        #if match is found return True to metric_bool
        metric_bool(name, True)
    else:
        #if the canary flow doesn't match the regex
        #return False to metric_bool
        metric_bool(name, False)

def main(args):
    check(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check if canary flow is found in br-int bridge')
    parser.add_argument('--telegraf-output',
                        action='store_true',
                        default=False,
                        help='Set the output format to telegraf')
    args = parser.parse_args()
    with print_output(print_telegraf=args.telegraf_output):
        main(args)
