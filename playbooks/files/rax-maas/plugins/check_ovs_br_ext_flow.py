import argparse
import subprocess
from maas_common import metric_bool
from maas_common import print_output

def check(args):
    """check if there's an ext flow in the
       ovs bridge"""

    #define the name of the check
    name = "ovs-br_ext_flow_status"

    #define the command to run to check the flow
    ovs_br_ext_flow_cmd = "sudo ovs-ofctl dump-flows %s | head -n2 | tail -n1" % args.bridge

    #define the regex to search; this should be common
    #for all versions; we want to search if the line
    #ends with the below regex to raise the alar
    ext_flow_regex = "actions=drop"

    #try to run the command
    try:
        #reason for running this with shell=True is we need
        #to use pipe, head and tail commands
        output = subprocess.check_output(ovs_br_ext_flow_cmd, shell=True)
        ovs_br_ext_flow = output.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        #return False to metric_bool if the command fails
        metric_bool(name, False)
        #return from the function if the command fails
        return

    #check for the regex
    if ext_flow_regex not in ovs_br_ext_flow:
        #no match found, flow is fine; return True to metric_bool
        metric_bool(name, True)
    else:
        #match found return False to metric_bool
        metric_bool(name, False)

def main(args):
    check(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check if ext flow exists in ovs bridge')
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
