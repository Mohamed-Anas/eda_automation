import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import normaltest
from .explorer import Explorer
from .preprocess import Preprocess
#Have to deal with asking supervised or unsupervised -- how to do this it has to persist
#make them inherit from a parent class that has a variable for 

import os

#function for making directory
def mkdir_if_not_exist(path):
    if not isinstance(path, str):
        path = os.path.join(*path)
    if not os.path.exists(path):
        os.makedirs(path)

target = None

class Preprocessing(object):

	def __init__(self,data):
		self.df = data
		self.exp_obj = Explorer(self.df)
		#Create a report file here
		#mkdir_if_not_exist('./datay')
		
	def automate(self):
		self.exp_obj.print_shape()
		self.exp_obj.preprocess()
		self.columns_info()
		display(self.data_info())
		#print(self.df.describe().to_string(col_space = 2,float_format = '%.1f'))
		#print(self.df.describe(include=['object','datetime']).to_string(col_space = 2,float_format = '%.1f'))
		self.describe_data()
		self.exp_obj.drop_duplicates()
		self.exp_obj.drop_rows()
		self.exp_obj.drop_cols()
		self.is_supervised()

	def is_supervised(self):

		global target
		print('\t\t**Target Information**\n')
		type_of_analysis = input("Supervised or Unsupervised Analysis:(s for supervised,u for unsupervised: ")
		while type_of_analysis == 's':
			column = input('Enter Target Variable: ')
			if column in self.df.columns.values:
				target = column
				break
			else:
				print('Target varible not found in list of columns')


	def columns_info(self):
		"""Gives data types of the columns"""
		print('\t\t**Columns Information**')
		data_dict = self.exp_obj.column_types()
		for key in data_dict:
			print(key,':\t',len(data_dict[key]))
		for key in data_dict:
			print(key,':\t',data_dict[key])

	def data_info(self):
		print('\t\t**Data Information**')
		try:
			df = self.df
			df_info = pd.DataFrame(df.isna().sum(),columns = ['Null_count'])
			df_info['Non_Null_count'] = df_info.index.map(df.notna().sum())
			df_info['N_unique'] = df_info.index.map(df.nunique())
			df_info['D_types'] = df_info.index.map(df.dtypes)
			#df_info['Blank_count'] = df_info.index.map((df=='').sum())
			return df_info
		except:
			return 'Data Info failed: \nProblem with Column names -- Check for duplicate column names'

	def describe_data(self):
		print('\t\t**Description of Numeric Variables**')
		display(self.df.describe())
		print('\t\t**Description of Categoric Variables**')
		display(self.df.describe(include=['object','datetime']))

class Visual(object):
	def __init__(self,data):
		global target
		self.df = data
		self.target = target
		self.exp_obj = Explorer(self.df)
		"""
		f = open('../report/visual_report.html','w')
		f.close()
		f = open('../report/visual_report.html','a')
		self.file = f
		"""

	
	def automate(self):
		self.pairplot()
		self.correlation_plot()
		self.histogram()
		if self.target is not None:
			#get type of variable -- then decide
			print('\t\t**Plots with Target Variable**')
			if Preprocess().get_col_type(self.df,self.target) == 'numeric':
				self.corr_numeric()
				self.boxplot_numeric()
				self.scatterplot()
			if Preprocess().get_col_type(self.df,self.target) == 'categoric':
				self.boxplot_category()
				self.contingency_table()

			#TO DO deal with datetime later
		#self.file.close()


	def correlation_plot(self):
		"""Correlation between all numeric variables"""
		#numeric_vars = self.exp_obj.column_types()['numeric']
		print('\t\t**Correlation Ceofficient**')
		plot = sns.heatmap(self.df.corr())
		"""
		fig = plot.get_figure()
		
		fig.savefig('../report/correlation.png')
		filename = 'correlation.png'
		self.file.write('<img src="'+filename+'" />\n')
        #TO DO: Correlation of Categoric Variables
        """


	def pairplot(self):
		"""Pairplot of numeric varialbles with each other"""
		#Nothing to change here only thing is that I may need to 
		numeric_vars = self.exp_obj.column_types()['numeric']
		g = sns.PairGrid(self.df[numeric_vars].sample(100))
		g.map_diag(plt.hist)
		g.map_offdiag(plt.scatter)
		plt.figure()
		print('\t\t**Pairplot**')

	def scatterplot(self):
		numeric_vars = self.exp_obj.column_types()['numeric']
		for var in numeric_vars:
			if var==self.target:
				continue
			#filename = 'scatterplot'+col+'.png'
			my = sns.relplot(x=var,y=self.target,data=self.df)
			"""
			fig = my.fig
			fig.savefig('../report/'+filename)
			self.file.write('<img src="'+filename+'" />\n')
			"""

	def histogram(self):
		"""Frequency distribution of all variables"""
		#deals with numeric variables
		plot = self.df.hist(figsize=(30,30))
		fig = plot[0][0].get_figure()
		"""
		fig.savefig('../report/histogram.png')
		filename = 'histogram.png'
		self.file.write('<img src="'+filename+'" />\n')
		"""


		print('\t\t**Distribution of all columns**')

	def boxplot_category(self):
		"""Boxplot of categoric target with al numeric variables"""
		numeric_vars = self.exp_obj.column_types()['numeric']
		for col in numeric_vars:
			#filename = 'pairplot'+col+'.png'
			my = sns.catplot(x=self.target,y=col,kind='box',data=self.df)
			"""
			fig = my.fig
			fig.savefig('../report/'+filename)
			self.file.write('<img src="'+filename+'" />\n')
			"""

	def boxplot_numeric(self):
		"""Boxplot of numeric target with different categoric variables"""
		categoric_vars = self.exp_obj.column_types()['categoric']
		for col in categoric_vars:
			#filename = 'catplot'+col+'.png'
			my = sns.catplot(x=col,y=self.target,kind='box',data=self.df)
			"""
			fig = my.fig
			fig.savefig('../report/'+filename)
			self.file.write('<img src="'+filename+'" />\n')
			"""


	def corr_numeric(self):
		display(pd.DataFrame(self.df.corrwith(self.df[self.target]),columns=['correlation-coefficient']))

	def contingency_table(self):
		"""If target is categoric then contigency table for categoric variables"""
		pass

class Outlier(object):
	def __init__(self,data):
		self.df = data
		self.exp_obj = Explorer(self.df)

	def automate(self):
		#just show the iqr range and the number of 
		self.exp_obj.outlier_detection()
		self.outlier_categoric()

	def outlier_categoric(self):
		pass

class Imputation(object):
	def __init__(self,data):
		self.df=data
		self.exp_obj = Explorer(self.df)
	#may be add a pointer to self.impute in explorer where you can mention the columns
	def automate(self):
		#Imputes null values - no 
		self.exp_obj.impute()

class Testing(object):
	def __init__(self,data):
		global target
		self.df = data
		self.exp_obj = Explorer(self.df)
		self.target = target

	def automate(self):
		self.normality()
		if self.target is not None and Preprocess().get_col_type(self.df,self.target) == 'numeric':
			self.anova()

	def normality(self):
		#Caution: May give null values if all are NA
		print('\t\t**Normality Testing**\n')
		numeric_vars = self.exp_obj.column_types()['numeric']
		statistic = []
		pvalue = []
		for var in numeric_vars:
			if(self.df[var].isna().sum()!=0):
				print(var,' :null values_found')
				statistic.append(0)
				pvalue.append(0)
				continue
			v,p = normaltest(self.df[var])
			statistic.append(v)
			pvalue.append(p)
		result = pd.DataFrame({'statistic':statistic,'p-value':pvalue},index=numeric_vars)
		display(result)

	def anova(self):
		self.exp_obj.anova(self.target)
#chi-squared test of independence for category vs category
#anova test for category vs numeric
"""
When I create a html file - remember I am going to autogenerate a html file
I will have one file that will be inside the report directory I create. every time I write ssomething I write there.
"""