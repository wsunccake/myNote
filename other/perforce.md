# Perforce


## Configure

	rhel:~ # cat ~/.bashrc
	...
	export P4CONFIG=~/.p4config

	rhel:~ # cat ~/.p4config
	P4PORT=perforce:1666
	P4USER=user
	P4ROOT=/$HOME/Perforce/user_host
	P4CLIENT=user_host


## Command


### syntax

	rhel:~ # p4 [-u <user>] [-P <password>] [-p perforce:1666] <command>


### help

	rhel:~ # p4 help simple
	rhel:~ # p4 help commands


### login / logout

	rhel:~ # p4 login
	rhel:~ # p4 logout


### workspace / client

	rhel:~ # p4 clients                             # list work space
	rhel:~ # p4 client <workspace>                  # create work space
	rhel:~ # p4 client -d <workspace>               # delete work space


### file/dir

	rhel:~ # p4 files //depot/*                     # list file
	rhel:~ # p4 dirs //depot/*                      # list dir


### sync code

	rhel:~ # p4 sync //depot/release/...#head       # sync code
	rhel:~ # p4 sync -f //depot/release/...#head    # force sync


p4 info

