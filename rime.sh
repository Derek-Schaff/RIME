#!/bin/bash

docker run --rm \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	        -v $(pwd):/usr/RIME \
            --ipc=host \
	    -i -t \
            --user $(id -u):$(id -g) \
            --cap-drop=ALL \
            --security-opt=no-new-privileges \
            rimereqs:0.1 /bin/bash -c "cd /usr/RIME/ && python3 rime_main.py $*"
