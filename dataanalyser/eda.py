import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import normaltest
from .explorer import Explorer
from .preprocess import Preprocess
#Have to deal with asking supervised or unsupervised -- how to do this it has to persist
#make them inherit from a parent class that has a variable for 

class Preprocessing(object):

	def __init__(self,data):
		self.df = data
		self.exp_obj = Explorer(self.df)

		
	def automate(self):
		self.exp_obj.print_shape()
		self.exp_obj.preprocess()
		self.columns_info()
		print(self.data_info())
		#print(self.df.describe().to_string(col_space = 2,float_format = '%.1f'))
		#print(self.df.describe(include=['object','datetime']).to_string(col_space = 2,float_format = '%.1f'))
		self.describe_data()
		self.exp_obj.drop_duplicates()
		self.exp_obj.drop_rows()
		self.exp_obj.drop_cols()

	def columns_info(self):
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
			return 'Problem with Column names -- Check for duplicate column names'

	def describe_data(self):
		print('\t\t**Description of Numeric Variables**')
		print(self.df.describe())
		print('\t\t**Description of Categoric Variables**')
		print(self.df.describe(include=['object','datetime']))

class Visual(object):
	def __init__(self,data,target=None):
		self.df = data
		self.target = target
		self.exp_obj = Explorer(self.df)

	
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
			if Preprocess().get_col_type(self.df,self.target) == 'categoric':
				self.boxplot_category()
				self.contingency_table()

			#TO DO deal with datetime later


	def correlation_plot(self):
		"""Correlation between all numeric variables"""
		#numeric_vars = self.exp_obj.column_types()['numeric']
		self.exp_obj.correlation()
		print('\t\t**Correlation Ceofficient**')
        #TO DO: Correlation of Categoric Variables


	def pairplot(self):
		"""Pairplot of numeric varialbles with each other"""
		numeric_vars = self.exp_obj.column_types()['numeric']
		g = sns.PairGrid(self.df[numeric_vars].sample(100))
		g.map_diag(plt.hist)
		g.map_offdiag(plt.scatter)
		plt.figure()
		print('\t\t**Pairplot**')

	def histogram(self):
		"""Frequency distribution of all variables"""
		#deals with numeric variables
		self.df.hist(figsize=(30,30))
		print('\t\t**Distribution of all columns**')

	def boxplot_category(self):
		"""Boxplot of categoric target with al numeric variables"""
		numeric_vars = self.exp_obj.column_types()['numeric']
		for col in numeric_vars:
			sns.catplot(x=self.target,y=col,data=self.df)

	def boxplot_numeric(self):
		"""Boxplot of numeric target with different categoric variables"""
		categoric_vars = self.exp_obj.column_types()['categoric']
		for col in categoric_vars:
			sns.catplot(x=col,y=self.target,data=self.df)

	def corr_numeric(self):
		print(self.df.corrwith(self.df[self.target]))

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
		self.exp_obj.impute()

class Testing(object):
	def __init__(self,data):
		self.df = data
		self.exp_obj = Explorer(self.df)

	def automate(self):
		self.normality()

	def normality(self):
		numeric_vars = self.exp_obj.column_types()['numeric']
		statistic = []
		pvalue = []
		for var in numeric_vars:
			v,p = normaltest(self.df[var])
			statistic.append(v)
			pvalue.append(p)
		result = pd.DataFrame({'statistic':statistic,'p-value':pvalue},index=numeric_vars)
		print(result)


