To install the package 'dataanalyser'
1. Enter this folder through terminal
2. pip install -r requirements.txt
3. pip install .

To use the package 'dataanalyser'
	from dataanalyser import Explorer
	import pandas as pd
	dataframe = pd.read_csv('filename')
	cl = Explorer(dataframe)
	cl.automate()
