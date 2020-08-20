FROM theshadowx/qt5:18.04

########################################################
# Essential packages for remote building/compiling, debugging, and logging in
########################################################

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    apt-utils gcc g++ openssh-server cmake build-essential gdb gdbserver rsync vim \
    libglu1-mesa-dev python3-pip libfontconfig libxrender1 ca-certificates  libudunits2-0 \
    libnetcdf-dev libnetcdff-dev

RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get install -y \
    gdal-bin python3-gdal

RUN mkdir /var/run/sshd

########################################################
# TODO: Change this over to key pair authentication for increased security
# https://blog.jetbrains.com/clion/2019/03/webinar-recording-remote-development-with-clion/

RUN echo 'root:root' | chpasswd
########################################################

##########
# From https://docs.docker.com/engine/examples/running_ssh_service/#environment-variables
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
ENV QT_GRAPHICSSYSTEM="native"

RUN echo "export VISIBLE=now" >> /etc/profile
########

# 22 for ssh server. 7777 for gdb server.
EXPOSE 22 7777

RUN useradd -ms /bin/bash debugger
RUN echo 'debugger:pwd' | chpasswd

########################################################
# More C/Python Libraries go after here (eg. HDF5 libraries)
########################################################

RUN pip3 install PySide2 numpy==1.18 h5py GDAL cfchecker

RUN cp /usr/lib/x86_64-linux-gnu/libnetcdf.so /lib/x86_64-linux-gnu/libnetcdf.so.15

CMD ["/bin/bash"]
#CMD ["/usr/sbin/sshd", "-D"]


