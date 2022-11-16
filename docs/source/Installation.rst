.. default-domain:: py

.. _installation:

Installation instructions
===========================

For most users, the converter can be used by simply running a standalone executable file requiring no installation. 
Alternatively you can install the python module. This gives you access to the converter but also more options to batch process many files, and fine tune some details. 
Finally, if you wish t contribute, feel free to do so and share it !


Standalone Usage
-----------------

For Windows and Linuw users, you can download the standalone executable file here: <Figure out where to put it>
MacOS users, I need a good soul to do some compilation work. Alternatively, you can install the python module and run it through python (see below). 

Running the standalone version will open the GUI. See :ref:`GUIUsage` for a quick use guide. 

Python installation
--------------------

On any operating system, you can download the source code here <Figure out where to put it>. 
Open a command line interface, and go to the DigiclearJSONConverter root folder. You can then simply::

	pip install .
	
Note that the ``.`` is important. This calls ``pip`` to run the ``setup.py`` file. This should automatically install the module and its dependencies. 
The installer also creates a command line alias ``DigiclearJSONConverter`` which allows you to start the GUI converter from the command line. 

See :doc:`Basic Usage` for a quick use guide using either GUI or python scripts. 