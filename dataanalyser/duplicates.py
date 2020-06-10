import pandas as pd

class Duplicates(object):
    
    def __init__(self):
        pass
    
    def drop_duplicates(self,df):
        
        #dropping duplicate methods
        self.drop_duplicate_rows(df)
        self.drop_duplicate_columns(df)
        
    def drop_duplicate_rows(self,df):
        """Drops duplicate rows"""
        dups = df.shape[0]-df.drop_duplicates().shape[0]
        print('Duplicate rows detected: ',dups)
        
        #user-input
        opt = input('Drop Duplicate rows(y or n): ')
        if opt == 'n':
            return
        
        #drop duplicates
        df.drop_duplicates(inplace=True)
        print('Rows removed: ',dups)
        
#more messages

    def drop_duplicate_columns(self,df):
        """Drops duplicate columns or renames them."""
        duplicate_columns = df.columns.values[df.columns.duplicated()]
        print('Columns with duplicate names')
        print(duplicate_columns)
        if duplicate_columns:
            print(df[duplicate_columns])

        #user input
        opt = input('Drop Duplicate columns(y or n): ')
        
        if opt=='n':
            opt = input('Rename Duplicate columns(y or n): ')
            if opt=='n':
                return
            
            #rename the columns
            final_columns = df.columns.values
            for column in duplicate_columns:
                nos = 0
                for i in range(len(final_columns)):
                    if final_columns[i] == column:
                        final_columns[i]  = column+str(nos)
                        nos+=1
                if nos!=0:
                    print(column,' has be converted to ',[column+str(i) for i in range(nos)])
            df.columns = final_columns
            return
        
        #drop the columns
        print('Warning: Columns Dropped ',duplicate_columns)
        for column in duplicate_columns:
            temp  = pd.Series(df[column].iloc[:,0])
            df.drop(columns = [column],axis=1,inplace = True)
            df[column] = temp
