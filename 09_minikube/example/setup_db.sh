#!/bin/bash

projects=`ls project`


for project in ${projects}; do
    mysql_host=`kubectl get services | grep ${project}-mysql | awk '{ print $3 }'`
    if [ "${mysql_host}" != "" ]; then
        echo ""
        echo "****************************************"
        echo "* setup ${project}-mysql: ${mysql_host}"
        echo "****************************************"
        echo ""
        mysql --host=${mysql_host} --port=3306 --user=root --password=mypassword \
        < project/${project}/setup.sql
    fi
done