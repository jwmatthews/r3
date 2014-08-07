TEST_DIR="/var/lib/pulp/published/yum/https/repos/content/dist/rhel/rhui/server/6/6Server/x86_64/os/"
OUTPUT_FILE="rsync_rhel6_x86_64.txt"

time ./generate_rsync_list.py -s ${TEST_DIR} -o ${OUTPUT_FILE}


