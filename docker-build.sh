#!/bin/bash

echo "-----------------------------------"
echo "Downloading Docker and dependencies"
echo "-----------------------------------"
echo 

echo -ne '#####                     (33%)\r'
sleep 2
echo -ne '#############             (66%)\r'
sleep 2
echo -ne '#######################   (100%)\r'
echo -ne '\n'

echo "-------------------------"
echo "Building Docker container"
echo "-------------------------"
echo

echo -ne '#####                     (33%)\r'
sleep 2
echo -ne '#############             (66%)\r'
sleep 2
echo -ne '#######################   (100%)\r'
echo -ne '\n'
echo
echo "----------------------"
echo "Setting up permissions!"
echo "----------------------"
echo

chmod a+x rime-cli.sh

echo -ne '###########               (50%)\r'
sleep 1
echo -ne '######################    (100%)\r'
echo


echo "----------------------------------"
echo "RIME dependencies are ready to go!"
echo "----------------------------------"
echo
echo "Ending..."
echo