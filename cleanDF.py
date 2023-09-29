import pandas as pd


class cleanDF:

    def bug_classification_cleanup(self,cleanUp, df):
            pd.options.mode.copy_on_write = True
            newColumn = cleanUp + "A"
            df_new = df[[cleanUp, 'index']]       #get a subset of same columns into another df
            df_new.loc[:, newColumn] = 'NaN'
            #print(df_new)
            col_value = []                  #declare a required variable list 
            length = len(df_new.columns)
            for index, row in df_new.iterrows():        #loop to create required list
                value = []
                for col in range(len(df_new.columns)):
                    if col >= 0 and df_new.columns[col] == cleanUp:
                        col_value = ''
                        if not pd.isna(df_new.iloc[index,col]):
                            col_value=df_new.iloc[index,col]
                            df_new.loc[index,[newColumn]] = col_value

            duplicate_cols = df_new.columns[df_new.columns.duplicated()]
            df_new.drop(columns=duplicate_cols, inplace=True)       
            df_new.rename(columns= {newColumn: cleanUp}, inplace= True )

            return df_new