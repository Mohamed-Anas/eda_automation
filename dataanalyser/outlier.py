from .plotter import Plotter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype


class OutlierDetector(object):
    def __init__(self):
        """Parameters used by the methods."""
        
        self.columns = None
        self.data = None
        self.method = 'iqr'
        
    def set_params(self,df,**kwargs):
        """Setting the parameters."""
        
        self.data = df
        if 'columns' in kwargs:
            self.columns= kwargs['columns']
        else:
            self.columns = df.columns.values
        if 'method' in kwargs:
            self.method = kwargs['method']

#Option:
    
    def outlier_detection(self,df,**kwargs):
        """Method that calls relevant outlier detection methods. """
        self.set_params(df,**kwargs)
        
        print('Outliers will be detected for all numeric variables')
        print('Method used to detect outliers ',self.method)
        print('Other methods: zscore,iqr')
        
        #User Input
        opt = input('Detect Outliers(y or n c to change method)')
        if opt=='n':
            return
        if opt=='c':
            self.method = input('Enter method: ')
        
        #Calling relevant methods
        if self.method == 'iqr':
            self.iqr(df)
        elif self.method == 'zscore':
            self.zscore(df)
        
        
    def iqr(self,df):
        """Outlier detection using Inter-Quantile Range."""
        
        df = self.data
        for column in self.columns:
            try:
                #If the column is of 'string' or 'object' type --> then continue
                if not is_numeric_dtype(df[column]):
                    continue

            #Calculating the left and right boundaries beyond which
            #values are treated as outliers.
                q1 = df[column].quantile(0.25)
                q3 = df[column].quantile(0.75)
                iqr = q3-q1
                whisk1 = q1-1.5*iqr
                whisk2 = q3+1.5*iqr
            
                #show boxplots for outliers or kind 
                #Category has any effect on predicton of target
                #ANOVA done for each category - less than 10
                #Boxplots based on percentage - ii
                #ordinal or not - uer input 
                #calculating number of rows having outliers
                rows = df[(df[column]<=whisk1)|(df[column]>=whisk2)].shape[0]
                if rows>int(df.shape[0]/3):
                    continue
                if rows!=0:
                    print('Column: ',column,' has outliers in ',rows,' rows')
                    Plotter().boxplot(df,[column])

            except:
                #Handle General Errors
                print(column,' not Processed.')
                continue
                
    def zscore(self,df):
        """Outlier Detection using z-score."""
        
        df = self.data
        for column in self.columns:
            try:
                #If the column is of 'string' or 'object' type --> then continue
                #-->f
                if not is_numeric_dtype(df[column]) or df[column].nunique()<=5 :
                    #print(column,' is not numeric varible or it is oridinal variable')
                    continue

            #Calculating the left and right boundaries beyond which
            #values are treated as outliers.

                mean = df[column].mean()
                std = df[column].std()
                #show boxplots for outliers or kind 
                #Category has any effect on predicton of target
                #ANOVA done for each category - less than 10
                #Boxplots based on percentage - ii
                #ordinal or not - uer input 
                #calculating number of rows having outliers
                rows = (df[column]> mean+3*std).sum()
                rows+= (df[column]<mean-3*std).sum()
                if rows!=0:
                    print('Column: ',column,' has outliers in ',rows,' rows')
                    Plotter().boxplot(df,[column])

            except:
                #Handle General Errors
                print(column,' not Processed.')
                continue
                
#Cokk's Distance

    def outlier_pca(self,df,**kwargs):
        """Outlier Detection using PCA"""
        
        self.set_params(df,**kwargs)
        
        from sklearn.decomposition import PCA

        n_components = len(self.columns) #200
        
        whiten = False
        random_state = 2018

        pca = PCA(n_components=n_components, whiten=whiten, \
              random_state=random_state)
        X_train = df[self.columns]
        X_train_PCA = pca.fit_transform(X_train)
        X_train_PCA = pd.DataFrame(data=X_train_PCA, index=X_train.index)

        X_train_PCA_inverse = pca.inverse_transform(X_train_PCA)
        X_train_PCA_inverse = pd.DataFrame(data=X_train_PCA_inverse, \
                                       index=X_train.index)
        anomalyScoresPCA = self.anomalyScores(X_train, X_train_PCA_inverse)
        plt.plot(anomalyScoresPCA)
        plt.show()
        print('Number of possible outliers: ',(anomalyScoresPCA > 0.4).sum())
    
    def anomalyScores(self,originalDF, reducedDF):
        """Helper method for outlier_pca."""
        
        loss = np.sum((np.array(originalDF)-np.array(reducedDF))**2, axis=1)
        loss = pd.Series(data=loss,index=originalDF.index)
        loss = (loss-np.min(loss))/(np.max(loss)-np.min(loss))
        return loss
