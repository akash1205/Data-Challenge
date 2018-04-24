import pandas as pd
import os
from os import walk
import numpy as np
import datetime as dt
import json


'''
Firstly, the structure and datatypes are defined for all the columns
because when loading the loan data using read_csv function, a datatype
warning will be thrown stating that columns 3, 4, 5 ,7, 8, 9, 12 have mixed
datatypes. This also implies that going further, there can be issues with the data quality.
Hence, given metadata should be used to define the datatypes. Also, reading csv file
with LoanDataStructure gives a conversion type error because of the NA values.
So, they should be taken under consideration while loading the file.
'''

LoanDataStructure = {'As_of_Year': 'int64',
                     'Agency_Code': 'str',
                     'Agency_Code_Description': 'str',
                     'Respondent_ID': 'str',
                     'Sequence_Number': 'int64',
                     'Loan_Amount_000': 'float64',
                     'Applicant_Income_000': 'float64',
                     'Loan_Purpose_Description': 'str',
                     'Loan_Type_Description': 'str',
                     'Lien_Status_Description': 'str',
                     'State_Code': 'str',
                     'State': 'str',
                     'Country_Code': 'str',
                     'MSA_MD': 'str',
                     'MSA_MD_Description': 'str',
                     'Census_Tract_Number': 'str',
                     'FFIEC_Median_Family_Income': 'float64',
                     'Tract_to_MSA_MD_Income_Pct': 'float64',
                     'Number_of_Owner_Occupied_Units': 'str',
                     'County_Name': 'str',
                     'Conforming_Limit_000': 'float64',
                     'Conventional_Status': 'str',
                     'Conforming_Status': 'str',
                     'Conventional_Conforming_Flag': 'str'
                     }

InstitutionalDataStructure = {'As_of_Year': 'int64',
                              'Agency_Code': 'str',
                              'Respondent_ID': 'str',
                              'Respondent_Name_TS': 'str',
                              'Respondent_City_TS': 'str',
                              'Respondent_State_TS': 'str',
                              'Respondent_ZIP_Code': 'str',
                              'Parent_Name_TS': 'str',
                              'Parent_City_TS': 'str',
                              'Parent_State_TS': 'str',
                              'Parent_ZIP_Code': 'str',
                              'Assets_000_Panel': 'int64'
                              }


class dataMunging(object):
    '''
    The following constructor searches for the file by name in the system and loads it
    up based on the schema defined above.
    '''
    def __init__(self):
        naValues = ['NA ', 'NA  ', 'NA   ', 'NA    ', 'NA     ', 'NA      ']
        fileNames = ["2012_to_2014_institutions_data.csv", "2012_to_2014_loans_data.csv"]
        fileAddress = []
        rootAddress = os.path.abspath(os.sep)
        for fileName in fileNames:
            for root, dirs, files in walk(rootAddress):
                if fileName in files:
                    fileAddress.append(os.path.join(root, fileName))
                    break

        self.institutionalData = pd.read_csv(fileAddress[0], dtype=InstitutionalDataStructure, na_values=naValues)
        self.loanData = pd.read_csv(fileAddress[1], dtype=LoanDataStructure, na_values=naValues)

    '''
    The following method buckets the Loan_Amount_000 into categories based on the quantiles
    because Loan_Amount_000 follows a log normal distribution when whole data is
    considered. Hence, categorization of loan data can be done on its log normal form.
    Following methods were considered in coming up with this conclusion.
    sns.distplot(testdata.Loan_Amount_000)
    sns.distplot(np.log(testdata.Loan_Amount_000))
    ((np.log(testdata.Loan_Amount_000))).describe()
    sns.boxplot(y = (np.log(testdata.Loan_Amount_000)))
    Bucketing Strategy:
    Extra Small : These are the loans which comes under the first quantile of the loan distribution.
                  These are safe loans with a very low loan amount and thus, are less riskier.
                  Range: (1 <= Loan_Amount_000 < 152)
    Small :       These are the loans which comes under the interquantile region of the loan distribution.
                  These are safe loans with a very semi moderate loan amount have high popularity and exhibit high revenue
                  generation. Range :  (152 <= Loan_Amount_000 <= 347)
    Medium :      These are the loans which comes after the 3rd quantile region of the loan distribution.
                  These have moderate loan amount and safe because majority of them come with the backing
                  of being conventional and conforming. Range :  (348 <= Loan_Amount_000 <= 550)
    Large :       These are the loans which comes after the 3rd quantile region of the loan distribution.
                  These have high loan amount and are comparitively riskier because inconjuction of being high on loan
                  amount very few of them are conventional and conforming. Range : (Loan_Amount_000 > 551)
    '''
    def bucketLoanAmount(loanAmount):
        loanAmount = np.log(loanAmount)
        if loanAmount < 5.030:
            return 'Extra Small'
        elif ((loanAmount >= 5.030) & (loanAmount <= 5.850)):
            return "Small"
        elif ((loanAmount >= 5.850) & (loanAmount < 6.310)):
            return "Medium"
        else:
            return "Large"

    '''
    Since, the dataset has 'As_of_Year', 'Respondent_ID', 'Agency_Code'  as primary keys,
    they are merged using these attributes to generate the merged data.
    '''
    def hmda_init(self):
        #self.bucketLoanAmount()
        commonColumns = list(self.loanData.columns.intersection(self.institutionalData.columns))
        finalDataFrame = pd.merge(self.loanData, self.institutionalData[['As_of_Year', 'Respondent_ID', 'Agency_Code', 'Respondent_Name_TS']], how='left', on = commonColumns)
        finalDataFrame['LoanBuckets'] = finalDataFrame.Loan_Amount_000.apply(dataMunging.bucketLoanAmount)
        return finalDataFrame


    '''
    The following function filters the data based on the columns provided and saves
    them in a json file. This function is defined to explicitly filter data based on states
    and the conventional_conforming_flag but it can also filter the data
    based on any of the columns passed.
    Note: The columns passed except states and conventional_conforming_flag should
    actually match the name of the columns present in the dataset and should pass the
    values to filter on as a list.
    '''
    def hdma_to_json(self, data, states=None, conventional_Conforming=None, **kwags):
        queryString = []
        self.data = data
        if (type(states) is list):
            queryString.append('State in ' + str(states))
        if (type(conventional_Conforming) is list):
            queryString.append('Conventional_Conforming_Flag in '+str(conventional_Conforming))
        if(len(kwags.keys())) > 0:
            for key, value in kwags.items():
                if(key in self.data.columns):
                    queryString.append(key + ' in ' + str(value))
                else:
                    continue
        finalQuery = (" & ").join(queryString)
        if(len(finalQuery) != 0):
            finalData = self.data.query(finalQuery)
        else:
            finalData = self.data
        fileName = "Queried_Data_"+str(dt.datetime.now())+".json"
        finalData = finalData.to_dict(orient = 'records')
        with open(fileName, "w+") as outputFile:
            outputFile.write(json.dumps(finalData, indent = 1))
