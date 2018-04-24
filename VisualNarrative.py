import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')




def createLoanAmountPlotByTimeAndLoanPurpose(dataframe):
    f, axes = plt.subplots(2,2, figsize = (25,15))
    ((ax1, ax2), (ax3, ax4)) = axes
    plt.suptitle('Market Size by Year and Loan Purpose', fontsize=40)
    sns.barplot(x=dataframe.groupby(['As_of_Year']).count().reset_index()['As_of_Year'], y= dataframe.groupby(['As_of_Year']).count().reset_index()['Loan_Amount_000'], ax = ax1)
    sns.pointplot(x='As_of_Year', y= "Loan_Amount_000", data = dataframe, estimator = np.sum, ax = ax2)
    sns.barplot(x=dataframe.groupby(['As_of_Year','Loan_Purpose_Description']).count().reset_index()['As_of_Year'], y= dataframe.groupby(['As_of_Year','Loan_Purpose_Description']).count().reset_index()['Loan_Amount_000'], hue = dataframe.groupby(['As_of_Year','Loan_Purpose_Description']).count().reset_index()['Loan_Purpose_Description'], ax = ax3)
    sns.pointplot(x='As_of_Year', y= "Loan_Amount_000", data = dataframe, estimator = np.sum, hue = 'Loan_Purpose_Description', ax = ax4)
    ax1.set_title("Total Number of Applications by Year", fontsize=20)
    ax1.set_ylabel("Count of Applications")
    ax2.set_title("Total Revenue of Applications by Year", fontsize=20)
    ax2.set_ylabel("Revenue")
    ax3.set_title("Total Number of Applications by Year and Loan Purpose", fontsize=20)
    ax3.set_ylabel("Count of Applications")
    ax4.set_title("Total Revenue of Applications by Year and Loan Purpose", fontsize=20)
    ax4.set_ylabel("Revenue")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    left  = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.4
    wspace = 0.2
    hspace = 0.2


def createLoanAmountPlotByStateAndLoanPurpose(dataframe):
    f, axes = plt.subplots(2,2, figsize = (25,15))
    ((ax1, ax2), (ax3, ax4)) = axes
    plt.suptitle('Market Size by State and Loan Purpose', fontsize=40)
    sns.countplot(x=dataframe.State, ax = ax1)
    sns.barplot(x=dataframe.State, y= dataframe.Loan_Amount_000, estimator = np.sum, ax = ax2)
    sns.countplot(x=dataframe.State, hue = dataframe.Loan_Purpose_Description, ax = ax3)
    sns.barplot(x=dataframe.State, y= dataframe.Loan_Amount_000, estimator = np.sum, hue = dataframe.Loan_Purpose_Description, ax = ax4)
    ax1.set_title("Total Number of Applications by State", fontsize=20)
    ax1.set_ylabel("Count of Applications")
    ax2.set_title("Total Revenue of Applications by State", fontsize=20)
    ax2.set_ylabel("Revenue")
    ax3.set_title("Total Number of Applications by State and Loan Purpose", fontsize=20)
    ax3.set_ylabel("Count of Applications")
    ax4.set_title("Total Revenue of Applications by State and Loan Purpose", fontsize=20)
    ax4.set_ylabel("Revenue")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    left  = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.4
    wspace = 0.2
    hspace = 0.2



def createLoanAmountPlotByStateAndTime(dataframe):
    f, axes = plt.subplots(1,2, figsize = (25,8))
    (ax1, ax2) = axes
    plt.suptitle('Market Size by State and Time', fontsize=40)
    sns.barplot(x=dataframe.groupby(['As_of_Year','State']).count().reset_index()['As_of_Year'], y= dataframe.groupby(['As_of_Year','State']).count().reset_index()['Loan_Amount_000'], hue = dataframe.groupby(['As_of_Year','State']).count().reset_index()['State'], ax = ax1)
    sns.pointplot(x='As_of_Year', y= "Loan_Amount_000", data = dataframe, estimator = np.sum, ax = ax2, hue = 'State')
    ax1.set_title("Total Number of Applications by State and Time", fontsize=20)
    ax1.set_ylabel("Count of Applications")
    ax2.set_title("Total Revenue of Applications by State and Time", fontsize=20)
    ax2.set_ylabel("Revenue")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    left  = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.4
    wspace = 0.2
    hspace = 0.2



def createMarketShareByBuckets(dataframe):
    f, axes = plt.subplots(2,2, figsize = (25,15))
    ((ax1, ax2), (ax3, ax4)) = axes
    plt.suptitle('Market Size by Buckets', fontsize=40)
    sns.countplot(x=dataframe.LoanBuckets, ax = ax1)
    sns.barplot(x=dataframe.LoanBuckets, y= dataframe.Loan_Amount_000, estimator = np.sum, ax = ax2)
    sns.countplot(x=dataframe.LoanBuckets, hue = dataframe.Loan_Purpose_Description, ax = ax3)
    sns.countplot(x=dataframe.LoanBuckets, hue = dataframe.Conventional_Conforming_Flag, ax = ax4)
    ax1.set_title("Total Number of Applications by Buckets", fontsize=20)
    ax1.set_ylabel("Count of Applications")
    ax2.set_title("Total Revenue of Applications by Buckets", fontsize=20)
    ax2.set_ylabel("Revenue")
    ax3.set_title("Total Number of Applications by Buckets and Loan Purpose", fontsize=20)
    ax3.set_ylabel("Count of Applications")
    ax4.set_title("Total Number of Applications by Buckets and Application Type", fontsize=20)
    ax4.set_ylabel("Count of Applications")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    left  = 0.125
    right = 0.9
    bottom = 0.1
    top = 0.4
    wspace = 0.2
    hspace = 0.2
