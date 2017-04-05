#!/usr/bin/env python

# version 0.4
#
# changelog
#
# 0.1 start init
# 0.2 clead old codeD
# 0.3 --ask ask to user another address to continue recursion
# 0.4 minor changes
#


import argparse, time, logging

import sys, os
path = str(os.environ["DEV"])
sys.path.insert(0, path + '/libs/')

import pexpect
from termcolor import colored

import mftCustom

import pdb

class INTERACT(object):

	credentials = {}
	ip = ''
	hostname = ''
	os = ''
	telconn = ''
	
	def __init__(self, args):
		self.debug = args.debug
		self.enable = args.enable
		self.file =  args.file
			
	def authNG_user_pass(self, mode):
	
		if mode == 'global':
			self.credentials['username'] = str(os.environ["PYUSER"])
			self.credentials['password'] = str(os.environ["PYPASS"])
		elif mode == 'cpe_noradius':
			self.credentials['username'] = str(os.environ["PYUSER_CPE_NO_RADIUS"])
			self.credentials['password'] = str(os.environ["PYPASS_CPE_NO_RADIUS"])
		elif mode == 'generic':
			self.credentials['username'] = str(os.environ["PYUSER_FW"])
			self.credentials['password'] = str(os.environ["PYPASS_FW"])
		elif mode == 'lab':
			self.credentials['username'] = str(os.environ["PYUSER_LOCAL_LAB"])
			self.credentials['password'] = str(os.environ["PYPASS_LOCAL_LAB"])
		# elif mode == '...':
			# self.credentials['username'] = str(os.environ["..."])
			# self.credentials['password'] = str(os.environ["..."])
			
		logging.info( self.credentials )
				
	def authNG_enable(self, mode):
		
		if mode == 'global':
			self.credentials['enable'] = str(os.environ["PYEN"])
		elif mode == 'cpe':			
			self.credentials['enable'] = str(os.environ["PYEN_CPE"])
		elif mode == 'rr':			
			self.credentials['enable'] = str(os.environ["PYEN_RR"])
		# if mode == '...':			
			# self.credentials['enable'] = str(os.environ["..."])
			
		logging.info( self.credentials['enable'] )
		
	
	def release_control(self):	
		logging.info('press key to start interact')
		self.telconn.interact()
	
		
	def send_username_password(self):
	
		# pdb.set_trace()
	
		for loop_cred in ['global', 'cpe_noradius', 'generic', 'lab']:
			self.authNG_user_pass(loop_cred)
			
			logging.info('send username')
			self.telconn.sendline(self.credentials['username'] )
			self.telconn.expect(["sername:", "assword:", ">", "#", pexpect.TIMEOUT, pexpect.EOF], timeout=None)
				
			logging.info('send password')
			self.telconn.sendline(self.credentials['password'])
			self.ix = self.telconn.expect(["sername:", "assword:", ">", "#", pexpect.TIMEOUT, pexpect.EOF], timeout=None)
			
			if self.ix == 2 or self.ix == 3:
				logging.info('pass ok')
				self.telconn.sendline(' ')
				return True
				
	def send_enable(self):
	
		# pdb.set_trace()
			
		for loop_enable in [ 'global', 'cpe', 'rr' ]:
			
			self.authNG_enable( loop_enable )
		
			self.telconn.sendline('enable')

			self.telconn.expect(["sername:", "assword:", ">", "#", pexpect.TIMEOUT, pexpect.EOF], timeout=None)

			self.telconn.sendline(self.credentials['enable'])
			self.index = self.telconn.expect(["sername:", "assword:", ">", "#", pexpect.TIMEOUT, pexpect.EOF], timeout=None)
			
			if self.index == 3:
				logging.info('enable ok')
				self.telconn.sendline(' ')
				return True
				
	def connectV2(self, cmd):
		
		self.telconn = pexpect.spawn(cmd, maxread=4000)
		
		# telconn.logfile_read = fout
		if self.debug:
			fout = open('pyexpect.log','wb')
			# self.telconn.logfile = fout
			self.telconn.logfile_read = fout
			# self.telconn.logfile = sys.stdout

		self.telconn.delaybeforesend = 0.5
		self.telconn.setecho(False)
		
	def show_result(self, data_output):
	
		if self.file != "":
				
			with open(self.file, 'a+') as the_file:
				the_file.write('\n==========================================\n')
				the_file.write(data_output)
		else:
		
			print '================================'
			print colored(data_output, 'green')
			print '================================'
			
	def commandV2(self, cmd):
		
		logging.info('send command %s ' % (cmd))
		self.telconn.sendline(cmd)
			
	def handle_routineV2(self, result = False):
		
		# pdb.set_trace()
		self.index = self.telconn.expect(["sername:", "assword:", ">", "#", pexpect.TIMEOUT, pexpect.EOF], timeout=None)
		
		if result:
			self.show_result(self.telconn.before)
		
		if self.index == 0 or self.index == 1:
			# logging.info('01')
			logging.info('send user/pass... ')
			self.send_username_password()
			
		elif self.index == 2 and self.enable:
			
			# logging.info('2')
			logging.info('send enable... ')
			self.send_enable()
			
		elif self.index == 2:
			return True
			
		elif self.index == 3:
			# logging.info('3')
			logging.info('command execution... DONE')
			return True
			
		elif self.index == 7:
			# logging.info('7')
			logging.info('EOF... DONE')
			return True
		
	def routineV2(self, cmd, result = False):

		if self.telconn == '':
			# logging.info('1')
			self.connectV2( cmd )
		else:
			# logging.info('2')
			self.commandV2( cmd  )
		while True:
			if self.handle_routineV2(result):
				break

def command_from_file(file_cmd):

	command_full = []
	commands = []

	try:
		with open(file_cmd) as cmd_lists:
			for line in cmd_lists:
				line = line.rstrip()
				command_full.append(line)
				
		commands.extend(command_full)
		return commands
		
	except:
		print 'file \'xxxxxx.cmd\' not found'
		exit(0)

def command(args):

	if args.include:
		logging.debug('include: ')
		logging.debug(args.include)
		command_full = " ".join(args.cmd) + ' | include ' + " ".join(args.include)
	elif args.exclude:
		logging.debug('exclude: ')
		logging.debug(args.exclude)
		command_full = " ".join(args.cmd) + ' | exclude ' + " ".join(args.exclude)
	elif args.section:
		logging.debug('section: ')
		logging.debug(args.section)
		command_full = " ".join(args.cmd) + ' | section ' + " ".join(args.section)
	else:
		command_full = " ".join(args.cmd)
		
	return command_full
		
def main():

	##################### ARGPARSE Configuration

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-r','--router', required=True, default='mi-ovest-ar501')
	parser.add_argument('--enable', required=False, action='store_true', help='if found >, send enable password to switch in # mode')
	parser.add_argument('-j','--jump', required=False, default=[], nargs='+', help='define a host list where jump from -r host')
	
	parser.add_argument('--ask', required=False, action='store_true', help='wait another host to add to jump list from command output w/o exit from the application')

	parser.add_argument('-i','--include', help='| include on your command. DO NOT USE PIPE | inside', required=False, nargs='+')
	parser.add_argument('-e','--exclude', help='| exclude on your command. DO NOT USE PIPE | inside', required=False, nargs='+')
	parser.add_argument('-s','--section', help='| section on your command. DO NOT USE PIPE | inside', required=False, nargs='+')
	
	parser.add_argument('-c','--cmd', required=False, default=['sh', 'ip', 'int', 'brief', 'lo0'], help='''
		execute single command on router. 
		DO NOT USE PIPE |, use instead -i, -e, -s.
		you can specify in --cmd a file.cmd with command list''', nargs='+')
	
	parser.add_argument('-f','--file', required=False, default="", help='save command results into <file>')
	
	parser.add_argument('-d','--debug', action='store_true', required=False, help='write pyexpext debug infos into pyexpect.log')

	args = parser.parse_args()

	##################### 
	
	try:
		if args.file != '':
			os.remove(args.file)
	except:
		pass
	
	ipaddress = ''
	hostname = args.router
	
	ipaddress = mftCustom.return_target_ip(args.router)

	if mftCustom.PreChecks(ipaddress, os.environ['PYCOMM']):
		
		system_host, system_platform, system_os_type, system_ver = mftCustom.resolve_sysObjectIDNG_v02(ipaddress)
		hostname = mftCustom.stripAfterDot(system_host)
		
		print 
		print '#################################'
		print system_host
		print system_platform
		print system_os_type, '-', system_ver
		print '#################################'
		print 
	else:
		hostname = ''
	
	# logging.info(hostname)
	# logging.info(ipaddress)
	
	target = INTERACT(args)
	
	target.routineV2( 'telnet %s' % (ipaddress) )
	
	for jump in args.jump:
	
		ipaddress = mftCustom.return_target_ip(jump)
		print " .:: JUMPING into %s ::. " % (ipaddress)
		target.routineV2( 'telnet %s' % ( ipaddress ) )
		target.routineV2( 'term len 0' )
		if '.cmd' in ''.join(args.cmd):
			for command_from_list in command_from_file( ''.join(args.cmd) ):
				target.routineV2( command_from_list, result = True )
		else:
			target.routineV2( command(args), result = True )
			
		if args.ask:
			try:
				new_host = raw_input('enter new host ip address [Done]: ')
				if mftCustom.isIPADDRESS(new_host):
					args.jump.append(new_host)
				else:
					exit(0)
			except:
				exit(0)
				
		# self.release_control()
	
if __name__ == '__main__':
	main()
