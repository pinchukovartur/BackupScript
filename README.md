# Backup Script 
A script that clones a repository from a git in a slanted folder creates a project archive and deletes the project folder, checks to see if there is enough space for the archive to move the archive to the cloud. At the end, it sends a notification to the Slask chat.

## Installation
```
1. Install python version no less than 3.6
2. Run install bat file to install all the necessary libraries
3. Create a slack token to send a message http://php.net/manual/en/class.mongocollection.php
4. Add a token to the slack_config.xml configuration
5. Create a repository configuration.xml in the configs folder
6. Run the script with the required parameters
```

## Usage
```
python run.py <config_name.xml> <cron_command> <slack_config.data>

Example
python RunScripts.py config.xml "*/5 * * * *"  #Run clone project with config.xml and start every 5 minutes
```

# Features
1. Default value:

	<slack_config.data> - Without entering the configuration is slack, messages are not sent;
	
	<cron_command> - If you do not enter the kroon parameters, the script will run indefinitely;
	
	<config_name.xml> - Required parameter for input.
	
2. If all parameters are empty, script configurations are output.

	
# Algorithm


![alt tag](https://pp.userapi.com/c841637/v841637180/a42a/dLeO3KRGjoc.jpg "Algorithm of the script")
	
## Cron Help
    * * * * * Running command
    - - - - -
    | | | | |
    | | | | ----- Day of the week (0 - 7) (Sunday =0 или =7)
    | | | ------- Month (1 - 12)
    | | --------- Day (1 - 31)
    | ----------- Hour (0 - 23)
    ------------- Minute (0 - 59)

	The formats currently supported are
	- `*/5` (for "every X" function),
	- `4-10` (for time ranges),
	- `6,8,23` (for a list of values),
	- `*` (for wildcard),
	- and of course a single number.
	
	
## Config Help
```
Config decription
<repository> - The tag stores all the information about the repository that will be cloning by the script.
<config_name> - The name of the repository.
<cloning_directory> - Directory where the project will be downloaded (temporarily).
<cloud_directory> - Directory where the project will be saved.
<max_file_number> - Maximum number of files in the directory.
<storage_size> - The maximum size of all files in the directory:
			mb - megabyte  
			gb - gigabySte 
			tb - terabyte
<url> - The address in the network where the repository is located (example: username:password@github.com/username/repository.git )
```

```
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
```
