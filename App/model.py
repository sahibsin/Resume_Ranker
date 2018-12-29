
import numpy as np
import pandas as pd
from time import strptime
import calendar
import time
from dateutil import relativedelta

tm=calendar.month_abbr[int(time.strftime("%m"))]
ty=time.strftime("%Y")
curMY=tm+ty

train_sent=pd.read_csv("TrainData.csv")
train_date = train_sent[train_sent.Col3 == 'DATE']["Col1"]

def main():
    df= train_date.values
    df1= train_date.iloc[::2]
    df1= df1.reset_index(drop=True)
    df2= train_date.iloc[1::2]
    df2= df2.reset_index(drop=True)
    df4= pd.Series(df1.str.cat(df2, sep=''))
    df44= pd.Series(df1.str.cat(df2, sep=' '))


    df1.replace({'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'June': 'Jun', 'July':'Jul', 'August':'Aug', '^September|Sept':'Sep', 'October':'Oct', 'November':'Nov', 'December':'Dec'}, regex=True, inplace=True)
    df5= df4.replace('^TillDate.|tilldate|tilldate.|Tilldate', curMY, regex=True)


    df6=pd.Series.to_frame(df5)
    df6 = df6.apply(pd.to_datetime)
    df6['RefDate']=pd.Series(df1.str.cat(df2,sep=' '))
    df6['DatesRanked'] = df6['Col1'].rank(ascending=1, method='dense')


    df20= df44.iloc[::2]
    df20= df20.reset_index(drop=True)
    df21= df44.iloc[1::2]
    df21= df21.reset_index(drop=True)
    df22= pd.concat([df20, df21], axis=1)
    df22.rename(index=str, columns={"Col1": "Start", "Col1": "End"})
    df23= df6.iloc[::2]
    df23= df23.reset_index(drop=True)
    df24= df6.iloc[1::2]
    df24= df24.reset_index(drop=True)
    df25= pd.concat([df23, df24], axis=1)
    df25.columns = ['Joining_Date','Joining_Date_in_CV','JoinDate_Rank','Leaving_Date','Leaving_Date_in_CV','LeavingDate_Rank']
    pd.DatetimeIndex(df25.Joining_Date).normalize()
    pd.DatetimeIndex(df25.Leaving_Date).normalize()

    for i in range(len(df25)):
        r = relativedelta.relativedelta(df25.Leaving_Date.iloc[i], df25.Joining_Date.iloc[i])
        tot_months=r.months+r.years*12
        df25.loc[i, 'Duration_in_months'] = tot_months
    html_df= df25.to_html(index=False)
    Html_file = open("./templates/htmlData.html", "w")
    Html_file.write(html_df)
    Html_file.close()

    return html_df



