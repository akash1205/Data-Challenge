'''
1) AS_of_YEAR: Year should be of the same format YYYY. Check for values which
doesn't follow this format and report it. Set a rule should always be in YYYY
format
2) Respondent_ID, Agency Code and Agency code description should be consistent
3) Sequence Number, Agency code, Respondent id can be used to identify a record
and they should be unique
4) Loan_Amount_000 should not be null or NA and should be numeric
5) Applicant_Income_000 same rules as Loan_Amount_000
6) Loan_Purpose should be a string, not null and without NA values and should
take only 3 values i.e. Purchase, Refinance and Home-Improvement
7) Loan_Type_Description can be conventional, government-insured or
government-guarenteed
8) Lien_Status_Description can take first or subordinate as string values
9) State_Code should be of two characters and should be unique for every state
10) State should be alphabetic, two characters and should conform to the list of
states
'''

from DataMunging import dataMunging
import seaborn as sns
import json
import numpy as np

'''
The following method gives the location of NA Values in the column for further analysis
so that the records can be imputed or dropped.
'''
def getLocationOfNAValues(dataFrame, columnName):
    naValuesIndex = dataFrame.index[dataFrame[columnName].isnull()].tolist()

    results = {"Column": columnName, "Count of Missing Values at index": len(naValuesIndex)}
    return results


'''
The following method drops the duplicate records in loan and institution data based on their
primary keys which are 'Sequence_Number', 'Agency_Code', 'Respondent_ID', 'As_of_Year' and
'Agency_Code', 'Respondent_ID', 'As_of_Year', respectively.
'''
def cleanDuplicateRecords(dataframe, dataName):
    indices = []
    loanKey = ['Sequence_Number', 'Agency_Code', 'Respondent_ID', 'As_of_Year']
    institutionKey = ['Agency_Code', 'Respondent_ID', 'As_of_Year']
    if dataName.lower() == 'loan':
        indices = dataframe.index[dataframe.duplicated(subset=loanKey, keep='first')].tolist()
    elif dataName.lower() == 'institution':
        indices = dataframe.index[dataframe.duplicated(subset=institutionKey, keep='first')].tolist()
    else:
        return "Invalid Dataframe name"

    return dataframe.drop(indices)


def getDuplicateRecords(dataframe, dataName):
    loanKey = ['Sequence_Number', 'Agency_Code', 'Respondent_ID', 'As_of_Year']
    institutionKey = ['Agency_Code', 'Respondent_ID', 'As_of_Year']
    if dataName.lower() == 'loan':
        indices = dataframe.index[dataframe.duplicated(subset=loanKey, keep='first')].tolist()
    elif dataName.lower() == 'institution':
        indices = dataframe.index[dataframe.duplicated(subset=institutionKey, keep='first')].tolist()
    else:
        return "Invalid Dataframe name"

    results = {"Duplicate Data at index": indices}

    return results

def getDuplicateRecordsinMergedData(dataframe):
    Key = ['Sequence_Number', 'Agency_Code', 'Respondent_ID', 'As_of_Year']
    indices = dataframe.index[dataframe.duplicated(subset=Key, keep='first')].tolist()

    results = {"Duplicate Data at index": indices}

    return results

def getFaultyRespondentName(dataframe):
    faultyData = {}
    key = ['Agency_Code','As_of_Year','Respondent_ID', 'Respondent_Name_TS']
    keyRespondent = ['Agency_Code','As_of_Year','Respondent_ID']
    dataframe = dataframe[['Agency_Code','As_of_Year','Respondent_ID', 'Respondent_Name_TS']]
    uniqueKeys = dataframe[key].drop_duplicates()
    indices = uniqueKeys.index[uniqueKeys.duplicated(subset=keyRespondent, keep='first')].tolist()
    results = {"Duplicate Data at index": indices}
    return results
