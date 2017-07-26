# pycron [![Build Status](https://travis-ci.org/kipe/pycron.svg?branch=master)](https://travis-ci.org/kipe/pycron)
A simple script that clones, archives and sends the project to the directory, depending on the configurations specified. 
Upon completion of the work, the script sends the report to the Slack chat.

## Installation
```
	run install.bat file
```

## Usage
	```
	python RunScripts.py configs\config.xml "*/5_*_*_*_*" #Run clone project with config.xml and start every 5 minutes
	```
	
## Help
	The formats currently supported are
	- `*/5` (for "every X" function),
	- `4-10` (for time ranges),
	- `6,8,23` (for a list of values),
	- `*` (for wildcard),
	- and of course a single number.
	
	
	Config documentation
<?xml version="1.0"?>

<!-- Config decription -->
<!-- <repository> - The tag stores all the information about the repository that will be cloning by the script -->
<!-- <config_name> - The name of the repository -->
<!-- <cloning_directory> - Directory where the project will be downloaded (temporarily) -->
<!-- <cloud_directory> - Directory where the project will be saved -->
<!-- <max_file_number> - Maximum number of files in the directory -->
<!-- <storage_size> - The maximum size of all files in the directory
			mb - megabyte  
			gb - gigabyte 
			tb - terabyte 
<!-- <url> - The address in the network where the repository is located 
							(example: username:password@github.com/username/repository.git )-->

<data>
	<max_file_number>25</max_file_number>
	<storage_size>25mb</storage_size>

    <repository>
		<config_name>ArchiveName</config_name>
		<url>username:password@github.com/username/repository.git</url>
		<cloud_directory>test_cloud_directory\</cloud_directory>
		<cloning_directory>test_cloned_directory\</cloning_directory>
    </repository>
</data>
