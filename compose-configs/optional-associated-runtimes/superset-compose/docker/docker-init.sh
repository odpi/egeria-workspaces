#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -e

#
# Always install local overrides first
#
/app/docker/docker-bootstrap.sh

STEP_CNT=4

echo_step() {
cat <<EOF

######################################################################


Init Step ${1}/${STEP_CNT} [${2}] -- ${3}


######################################################################

EOF
}
ADMIN_PASSWORD="admin"

# Initialize the database
echo_step "1" "Starting" "Applying DB migrations"
superset db upgrade
echo_step "1" "Complete" "Applying DB migrations"

# Create an admin user
echo_step "2" "Starting" "Setting up admin user ( admin / $ADMIN_PASSWORD )"
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password $ADMIN_PASSWORD

superset fab create-admin \
              --username pdr \
              --firstname trouble \
              --lastname maker \
              --email dan.wolfson@pdr-associates.com  \
              --password pdr4egeria
echo_step "3" "Complete" "Setting up admin & pdr user"
# Create default roles and permissions
echo_step "4" "Starting" "Setting up roles and perms"
superset init
echo_step "5" "Complete" "Setting up roles and perms"

if [ "$SUPERSET_LOAD_EXAMPLES" = "yes" ]; then
    # Load some data to play with
    echo_step "6" "Starting" "Loading examples"
    # If Cypress run which consumes superset_test_config – load required data for tests
    superset load_examples --force

    echo_step "7" "Complete" "Loading examples"
fi

echo_step "8" "Setup the Nanny Dashboard(s)"
superset import-dashboards -u pdr -p ./docker/atlas_nanny_dashboard.zip

