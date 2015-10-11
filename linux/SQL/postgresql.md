# Postge SQL #

## Package ##

	linux:~ # yum install postgresql


## Service ##

	linux:~ # systemctl enable postgresql.service
	linux:~ # systemctl start postgresql.service

	# psql default port 5432
	linux:~ # netstat -luntp | grep 5432

	# config
	linux:~ # pg_config # show config
	linux:~ # ls /var/lib/pgsql/data # psql config & db folder
	linux:~ # cat /var/lib/pgsql/data/postgresql.conf # default config


## common ##

	# login
	linux:~ # su - postgres
	linux:~ $ psql

	linux:~ # psql -U username -d dbname -h host -p port -W

	postgres=# \h # help with SQL
	postgres=# \? # help with psql

	postgres=# \l # list database
	postgres=# \d # list table