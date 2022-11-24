Digiclear JSON converter
========================

Documentation
-------------
A full documentation is available [here](https://odin-doc.c2n.u-psud.fr/doc/DigiclearJSONConverter) (accesible only from C2N internal network). This readme aims at giving you a jumpstart.

Installation
-------------
The easiest way to install the package is to download all the files (Code -> Download zip), or if you have git installed:

	git clone https://github.com/pyMatJ/DigiclearJSONConverter.git

Open a command prompt and `cd` to the root of the directory. You can then install everything using:

	pip install .
	
Note the `.` after `install`. This stores the relevant python files in the appropriate directory, usually this is `wherever your python is`/Lib/site-package. This will also install required dependencies, such as [lxml](https://lxml.de/installation.html), [requests](https://requests.readthedocs.io/en/latest/), and [Reportlab](https://www.reportlab.com/opensource/). 

This also creates a shell command alias 

	DigiclearJSONConverter
	
that will start the graphical user interface of the program. 

Stand alone executable
-----------------------

If you do not care about scripting, and just want a graphical interface tool to quickly convert JSON files, stand alone executables should be available for download in the [releases](https://github.com/pyMatJ/DigiclearJSONConverter/releases) section[^1]. Just download the executable that matches your OS (Windows, Linux or Mac) and report to the section [Using the graphical user interface (GUI)](#Using-the-graphical-user-interface-(GUI)). Note that this feature is experimental, if it does not work please use the python version.

Converting JSON files
---------------------

Two methods are possible to convert JSON files. 

### Using a script

The most flexible and powerful one is to use the example script provided in the examples/ directory and fill in the correct login information: 

	username = 'prenom.nom' ### your digiclear username
	password = 'password' ### your digiclear password

If you have multiple JSON files located in a directory, just copy-paste the location in the following line: 

	sourcedirectory = Path(r'directory_with_jsonfiles')
	
and all JSON files will be converted to PDFs in that same directory. 

### Using the graphical user interface (GUI)

The GUI can be started in multiple ways:

1. From a command line, typing `DigiclearJSONConverter`
2. By executing the GUI script located in DicgiclearJSONConverter/gui/GUIConverter.py
3. From the executable

It opens a window where you can drag and drop files you want to convert. Enter your digiclear username and password in the appropriate fields, and click convert. If everything goes well, this should produce a PDF document for each JSON file you attached, in the same directory where they are located. You can then close the window.

[^1] This feature is experimental so far and relies on automatic build from github VMs. It might only work for up-to-date OS versions. The safest way to run the code reliably is still to run it through python. 
