import pandas as pd
from DataMunging import dataMunging
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

dm = dataMunging()
fd = dm.hmda_init()

def getdata(states = None, years = None, county = None):
    queryString = []
    selectedState = []
    selectedYear = []
    selectedCounty = []
    finalDatae = pd.DataFrame()
    if((years != "All") & (type(years)== str)):
        years = int(years)
    selectedState.append(states)
    selectedYear.append(years)
    selectedCounty.append(county)
    if((('All' in selectedState) & ('All' in selectedYear) & ('All' in selectedCounty))| (('All' in selectedState) & ('All' in selectedYear)) | (('All' in selectedState) & ('All' in selectedCounty)) | (('All' in selectedYear) & ('All' in selectedCounty))):
        finalDatae = fd
    else:
        if((type(states) == str)&('All' not in selectedState)):
            queryString.append('State in ' + str(selectedState))
        if((type(years) == int)&('All' not in selectedYear)):
            queryString.append('As_of_Year in '+str(selectedYear))
        if((type(county) == str)&('All' not in selectedCounty)):
            queryString.append('County_Name in '+str(selectedCounty))
        finalQuery = (" & ").join(queryString)
        finalDatae = fd.query(finalQuery)

    return finalDatae



def CreatCountyWiseBusinessPlot(States, County):
    finalData = getdata(states=States, county=County)
    f, axes = plt.subplots(3,2, figsize = (20,30))
    ((ax1, ax2), (ax3, ax4),(ax5, ax6)) = axes
    finalData = finalData[~pd.isnull(finalData['County_Name'])]
    countbyRespondent = finalData.groupby(['County_Name']).count().reset_index().sort('Agency_Code', ascending = False)
    countbyRespondentx = countbyRespondent.iloc[:10]
    top10Respondentx = countbyRespondent.iloc[:10,0]
    countbyRespondent = finalData.groupby(['County_Name', 'Loan_Purpose_Description']).count().reset_index().sort(['County_Name', 'Agency_Code'], ascending = [False, False])
    finalDataSet = pd.DataFrame(columns = countbyRespondent.columns)

    for respondent in top10Respondentx:
        finalDataSet = finalDataSet.append(countbyRespondent[countbyRespondent['County_Name'] == respondent])
    plt.suptitle('Loan Business by County and State', fontsize=40)
    sns.barplot(x='County_Name', y='Agency_Code', data = countbyRespondentx, ax = ax1)
    ax1.set_title("Total Number of Applications by County")
    ax1.set_ylabel("Count of Applications")

    sns.barplot(x='County_Name', y='Agency_Code', data = finalDataSet, hue = 'Loan_Purpose_Description', ax = ax2)
    ax2.set_title("Total Number of Applications under each County by Loan Purpose Description")
    ax2.set_ylabel("Count of Applications")
    sns.barplot(x='County_Name', y = 'Loan_Amount_000', data=finalDataSet, estimator = np.sum, ax = ax3)
    ax3.set_title("Revenue by County")
    ax3.set_ylabel("Revenue in Dollars 000")
    sns.barplot(x='County_Name', y = 'Loan_Amount_000', data=finalDataSet, estimator = np.median, ax = ax4)
    ax4.set_title("Median Loan Amount by County")
    ax4.set_ylabel("Median Loan Amount 000")
    sns.pointplot(x=finalData.As_of_Year.value_counts().index, y= finalData.groupby('As_of_Year').count()['Loan_Amount_000'], ax = ax5)
    ax5.set_title("Trend of Loan Market")
    ax5.set_ylabel("Count of Applications")
    sns.pointplot(x=finalData.groupby(['As_of_Year', 'Loan_Purpose_Description']).count().reset_index()['As_of_Year'], y= finalData.groupby(['As_of_Year', 'Loan_Purpose_Description']).count().reset_index()['Loan_Amount_000'], hue = finalData.groupby(['As_of_Year', 'Loan_Purpose_Description']).count().reset_index()['Loan_Purpose_Description'], ax = ax6)
    ax6.set_title("Trend of Loan Market by Loan Purpose")
    ax6.set_ylabel("Count of Applications")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    left  = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.4
    wspace = 0.2
    hspace = 0.2

    for ax in axes.flatten():
        for label in ax.get_xticklabels():
            label.set_rotation(30)


def createCompetitorPlots(States, Years):
    finalData = getdata(States, Years)
    f, axes = plt.subplots(2,2, figsize = (20,30))
    ((ax1, ax2), (ax3, ax4)) = axes
    countbyRespondent = finalData.groupby(['Respondent_Name_TS']).count().reset_index().sort('Agency_Code', ascending = False)
    countbyRespondentx = countbyRespondent.iloc[:10]
    top10Respondentx = countbyRespondent.iloc[:10,0]
    countbyRespondent = finalData.groupby(['Respondent_Name_TS', 'Loan_Purpose_Description']).count().reset_index().sort(['Respondent_Name_TS', 'Agency_Code'], ascending = [False, False])
    finalDataSet = pd.DataFrame(columns = countbyRespondent.columns)
    for respondent in top10Respondentx:
        finalDataSet = finalDataSet.append(countbyRespondent[countbyRespondent['Respondent_Name_TS'] == respondent])
    plt.suptitle('Top Competetors by Region and by Time', fontsize=40)
    sns.barplot(x=countbyRespondentx.Respondent_Name_TS, y=countbyRespondentx.Agency_Code, data = countbyRespondentx, ax = ax1)
    ax1.set_title("Total Number of Applications under Respondent Name")
    ax1.set_ylabel("Count of Applications")
    sns.barplot(x='Respondent_Name_TS', y='Agency_Code', data = finalDataSet, hue = 'Loan_Purpose_Description', ax = ax2)
    ax2.set_title("Total Number of Applications under Respondent Name by Loan Purpose Description")
    ax2.set_ylabel("Count of Applications")
    sns.barplot(x='Respondent_Name_TS', y = 'Loan_Amount_000', data=finalDataSet, estimator = np.sum, ax = ax3)
    ax3.set_title("Revenue by Respondent Name")
    ax3.set_ylabel("Revenue in Dollars 000")
    sns.barplot(x='Respondent_Name_TS', y = 'Loan_Amount_000', data=finalDataSet, estimator = np.median, ax = ax4)
    ax4.set_title("Median Loan Amount by Respondent Name")
    ax4.set_ylabel("Median Loan Amount 000")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    left  = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.4
    wspace = 0.2
    hspace = 0.2

    for ax in axes.flatten():
        for label in ax.get_xticklabels():
            label.set_rotation(30)
