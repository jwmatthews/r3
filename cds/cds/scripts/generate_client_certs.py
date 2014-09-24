#! /usr/bin/python

import sys
from ConfigParser import SafeConfigParser
from pulp.cds.repo_auth.repo_cert_utils import RepoCertUtils
from optparse import OptionParser

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("--ca", dest="ca_cert",
                  help="repo ca cert")	
	parser.add_option("--client", dest="client_cert",
                  help="repo client cert")	
	parser.add_option("--id", dest="repo_id",
                  help="repo id")	
	parser.add_option("--path", dest="relative_path",
                  help="relative path")	

	(options, args) = parser.parse_args()

	if options.ca_cert is None or options.repo_id is None:
		print "Must specify --ca, --client and --is options"
		sys.exit(1)

	config_filename = "/etc/pulp/repo_auth.conf"
	config = SafeConfigParser()
    	config.read(config_filename)
	rcu = RepoCertUtils(config)
	#bundle = {"ca": options.ca_cert, "cert": options.client_cert}
	bundle = {"ca": options.ca_cert, "cert": None}
	rcu.write_consumer_cert_bundle(options.repo_id, bundle)

	# update protected file
	fh = open('/etc/pki/pulp/content/pulp-protected-repos', 'a')
	fh.write('%s,%s' % (options.relative_path, options.repo_id))
	fh.close()
