from setuptools import setup

setup(name='dataanalyser',
	version='0.0.1',
	description='Automates Exploratory Data Analysis',
	author = 'Mohamed Anas',
	author_email='anasmd890@gmail.com',
	packages=['dataanalyser'],
	install_requires=['pandas>=1.0.3',
					'seaborn>=0.10.0',
					'sklearn',
					'numpy>=1.18.3',
					'scipy>=1.4.1',
					'matplotlib>=3.2.1',
					'python-dateutil','setuptools'])