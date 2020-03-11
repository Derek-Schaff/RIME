#!/bin/bash

container_name="rimereqs:0.1"
user_name=$USER

clear
echo "Starting Docker container..."
echo -ne '###########               (50%)\r'
sleep 1
echo -ne '######################    (100%)\r'
echo

#echo 'docker container run -it -v ~/RIME:/usr/RIME --rm rimereqs:0.1 /bin/bash -c "clear && python3 /usr/RIME/back_end/python/rime.py $1 $2 $3"'
sudo docker container run -it -v ~/pilot_test/RIME:/usr/pilot_test/RIME:rw --rm rimereqs:0.1 /bin/bash -c "/back_end/python && python3 rime.py $*"

#sudo ./x11docker --share /home/$user_name/RIME/ $container_name python3 /home/$user_name/RIME/back_end/python/rime.py

