# interactNG

Jump (through a specified device with -r extension) to single (or more) device and execute one or more commands with python pexpect library.

Credentials (user/pass and enable secrets) are taken from ENVIRONMET var list and all of them are inserted once the right one will be succesfully accepted.

main script extensions:

-r jump device (like bastion host) 
-j 1.1.1.1 [, 2.2.2.2, 3.3.3.3, ...]
--cmd <command> or xxxx.cmd (contains a list of commands to execute)

for additional infos user --help

'''
$ python interactNG.py -r tp-test-6500 -d -j 192.168.55.2 192.168.124.2 --cmd show ver -i IOS
WARNING: No route found for IPv6 destination :: (no default route?)
DEBUG:root:10.123.123.12 is succesfully icmp reachable!
DEBUG:root:10.123.123.12 test snmp community '****' succesfully done!
DEBUG:root:10.123.123.12 is succesfully icmp reachable!
DEBUG:root:10.123.123.12 test snmp community '****' succesfully done!

#################################
tp-test-6500
cat6509 (ent.9.1.283)
ios - 15.3(3)S6
#################################

INFO:root:send user/pass...
INFO:root:{'username': '*****', 'password': '*****'}
INFO:root:send username
INFO:root:send password
INFO:root:pass ok
 .:: JUMPING into 192.168.55.2 ::.
INFO:root:send command telnet 192.168.55.2
INFO:root:send user/pass...
INFO:root:{'username': '*****', 'password': '*****'}
INFO:root:send username
INFO:root:send password
INFO:root:pass ok
INFO:root:send command term len 0
DEBUG:root:include:
DEBUG:root:['IOS']
INFO:root:send command show ver | include IOS
================================
show ver | include IOS
Cisco IOS Software, 7200 Software (C7200P-ADVENTERPRISEK9-M), Version 15.2(4)M6, RELEASE SOFTWARE (fc2)
================================
 .:: JUMPING into 192.168.124.2 ::.
INFO:root:send command telnet 192.168.124.2
INFO:root:send user/pass...
INFO:root:{'username': '*****', 'password': '*****'}
INFO:root:send username
INFO:root:send password
INFO:root:pass ok
INFO:root:send command term len 0
DEBUG:root:include:
DEBUG:root:['IOS']
INFO:root:send command show ver | include IOS
================================
show ver | include IOS
Cisco IOS Software, 7200 Software (C7200P-ADVENTERPRISEK9-M), Version 15.2(3)M, RELEASE SOFTWARE (fc2)
================================
'''
