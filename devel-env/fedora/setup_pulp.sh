#!/bin/bash
yum install -y mongodb mongodb-server
systemctl enable mongod
systemctl start mongod

yum install -y qpid-cpp-server
systemctl enable qpidd 
systemctl start qpidd

yum install -y wget
wget http://repos.fedorapeople.org/repos/pulp/pulp/fedora-pulp.repo -O /etc/yum.repos.d/fedora-pulp.repo
yum --disablerepo="pulp-v2-stable" --enablerepo="pulp-v2-testing" -y groupinstall pulp-server pulp-admin
sudo -u apache pulp-manage-db

./config_pulp.sh 

systemctl enable pulp_workers.service
systemctl start pulp_workers.service 

systemctl enable pulp_celerybeat.service
systemctl start pulp_celerybeat.service

systemctl enable pulp_resource_manager.service
systemctl start pulp_resource_manager.service

systemctl enable httpd
systemctl start httpd

echo ""
echo "======="
echo "To ssh into your development environment you may either:"
echo " ssh vagrant@172.31.2.53    (username and password are both 'vagrant') "
echo " vagrant ssh     (from your host machine, this command will ssh automatically into the VM)"
echo "  Note:  on the VM, the git checkout is shared with the host at the path '/vagrant'"
echo ""
