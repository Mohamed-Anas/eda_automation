# Datacleaner
## For installing follow instructions from README.txt
### Steps to Use
1. Clone the Repository
2. Copy the '**dataanalyser**' folder into the current directory of your jupyter noteook.
3. Initiate a notebook
4. Load the data you want to analyze in a pandas dataframe.
5. Then do analysis by importing the **Explorer** class by
  * from dataanalyser import Explorer
  * Create a Explorer Object
  * dataframe = pd.read_csv('filename.csv')
  * cl = Explorer(dataframe)
  * cl.automate() -- to automate the analysis
