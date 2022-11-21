.. default-domain:: py

.. _installation:

Installation instructions
===========================

The best way to run this converter is to have a running python installation. This gives you access to the converter but also more options to batch process many files, and fine tune some details. 
For other users, the converter can be used by simply running a standalone executable file requiring no installation, albeit with greater support complexity. 
Finally, if you wish to contribute, feel free to do so and share it !


Standalone Usage
-----------------

Compiled, standalone executable files are available in the `releases <https://github.com/pyMatJ/DigiclearJSONConverter/releases>`_ section. 
Please know that they are automatically compiled on github VMs, which does not give a full control over the generated executable. It might only run smoothly on up-to-date operating systems. The most reliable way to run this module remains to use a python installation. 

Running the standalone version will open the GUI. See :ref:`GUIUsage` for a quick use guide. 

Python installation
--------------------

On any operating system, you can download the source code here <Figure out where to put it>. 
Open a command line interface, and go to the DigiclearJSONConverter root folder. You can then simply::

	pip install .
	
Note that the ``.`` is important. This calls ``pip`` to run the ``setup.py`` file. This should automatically install the module and its dependencies. 
The installer also creates a command line alias ``DigiclearJSONConverter`` which allows you to start the GUI converter from the command line. 

See :doc:`Basic Usage` for a quick use guide using either GUI or python scripts. 