"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class docker_criu(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches) 
		#                                    - Returns True if any lines in output match any of 
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		# 
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of 
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		if shutit.file_exists('/tmp/docker_criu',directory=True):
			if not shutit.get_input('Want me to try to start the existing instance up (y), or wipe the existing one (n)',boolean=True):
				shutit.send('cd /tmp/docker_criu')
				shutit.send('vagrant destroy -f')
				shutit.send('cd -')
				shutit.send('rm -rf /tmp/docker_criu')
		shutit.send('mkdir -p /tmp/docker_criu')
		shutit.send('cd /tmp/docker_criu')
		shutit.send('vagrant init larryli/vivid64')
		shutit.send('vagrant up --provider virtualbox')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su')
		shutit.install('docker.io')
		shutit.install('build-essential git criu')
		shutit.send('mkdir code')
		# Had to do this to get the git downloads to work - failed in ubuntus with signal 13
		shutit.send("""docker run -v /tmp/docker_criu/code:/tmp centos:centos7 bash -c 'yum install -y git && cd /tmp && git clone git://kernel.ubuntu.com/ubuntu/ubuntu-vivid.git && cd ubuntu-vivid && git remote add torvalds  git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git && git remote update'""")
		#shutit.send('git clone --depth 10 git://kernel.ubuntu.com/ubuntu/ubuntu-vivid.git')
		#shutit.send('cd ubuntu-vivid')
		#shutit.send('git remote add torvalds  git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git')
		#shutit.send('git remote update')
		shutit.send('cd code')
		shutit.send('git config --local user.email "a@b.com"')
		shutit.send('git config --local user.name "Ian Miell"')
		shutit.send('git cherry-pick 155e35d4da')
		shutit.send('git cherry-pick df1a085af1')
		shutit.send('git cherry-pick f25801ee46')
		shutit.send('git cherry-pick 4bacc9c923')
		shutit.send('git cherry-pick 9391dd00d1')
		shutit.logout()
		shutit.send('cp /boot/config-$(uname -r) .config')
		shutit.send('make olddefconfig')
		shutit.send('make -j 8 bzImage modules')
		shutit.send('sudo make install modules_install')
		shutit.send('sudo reboot')
		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is 
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return docker_criu(
		'shutit.docker_criu.docker_criu.docker_criu', 1228489603.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)

