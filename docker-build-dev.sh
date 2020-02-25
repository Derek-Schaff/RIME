#!/bin/bash

container_name="rimereqs:0.1"
user_name=$USER

sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y


curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

sudo apt update
sudo apt install docker-ce

echo "Building Docker container..."
docker image build -t $container_name .

