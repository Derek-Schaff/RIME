# RIME
RIME is a specialized conversion software used to translate binary satellite files into standardized NetCDF4, HDF5, and GeoTIFF formats.
## Prerequisites
Linux/GNU based operating system
Docker

## Usage instructions
### Step 1
**Clone Git Repository**

Enter this command into the terminal to clone this Git repository, checking out the development branch:

`git clone -b test_branch https://github.com/Turkishdisko/RIME.git`

### Step 2
**Change the current directory to the cloned RIME directory**

We need to now enter the directory containing the repository we just cloned:

`cd RIME`

### Step 3
**Give permission to allow execution to the install script**

To allow us to run the script which will install all of the needed software (Docker) and prepare the Docker container with our RIME requirements.  Run the following command:

`chmod a+x ./docker-build.sh`

### Step 4
**Prepare Docker image**

Run the script which will build the Docker image, putting all of the needed dependencies inside of a container:

`./docker-build.sh`

### Step 5
**Start RIME**

Finally, start the command line interface of RIME by typing:

`./rime-cli.sh`

This will give you the usage parameters needed to run RIME.

Great job, you have downloaded & installed several software applications and hundreds of libraries necessary for running RIME, all in _5_ steps!
