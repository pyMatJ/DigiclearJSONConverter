from setuptools import setup, find_packages

setup(
   name='DigiclearJSONConverter',
   version='0.0',
   description='Converts JSON history files from digiclear',
   url='',
   author='Mathieu Jeannin, Paul Goulain',
   packages=find_packages(),
   install_requires=['PyQt5', 'reportlab', 'requests', 'lxml'],
   entry_points={'console_scripts': ['DigiclearJSONConverter = scripts.GUIConverter:main']},
)