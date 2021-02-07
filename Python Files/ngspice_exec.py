import os,subprocess
run_command = "ls"
subprocess.call('ngspice', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
