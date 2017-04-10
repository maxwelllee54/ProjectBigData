import numpy as np
import pandas as pd

def volatility(df, intvl=5):
    '''

    :param df: stock data frame, columns must have ['date', 'time', 'price']
    :param int: time interval, unit in minute
    :return: return a new data frame with its volatility
    '''

    data = df.copy()
    output = pd.DataFrame()

    for date in set(df.loc[:, 'date']):
        temp_df1 = data.loc[data.date == date, :]
        temp_df1['ind'] = temp_df1.index

        temp_df1 = temp_df1.groupby(temp_df1.index // intvl).mean()
        temp_df2 = temp_df1.set_index('ind')
        temp_df2.loc[:, 'time'] = df.loc[temp_df2.index, 'time']

        s_i = temp_df2['price']
        s_i_1 = temp_df2['price'].shift(1)
        temp_df2['u_sequence'] = np.log(s_i / s_i_1)
        s = temp_df2['u_sequence'].rolling(window=len(set(temp_df1.index // intvl)), center=False).std()
        # data.loc[data.date == date, str(intvl)+'_min_vol']
        temp_df2.loc[:, str(intvl) + '_min_vol'] = s * np.sqrt(len(set(temp_df1.index // intvl)))

        output = pd.concat([output, temp_df2])
    output.reset_index(drop=True, inplace=True)
    return output

if __name__ == '__main__':

    df = pd.read_csv('~/Downloads/GS_1m.csv',sep=";",decimal=',', index_col=None, header=0)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df['date'] = [d.date() for d in df['timestamp']]
    df['time'] = [d.time() for d in df['timestamp']]
    df['price'] = df['close']
    volatility(df).to_csv('GS_volatility.csv')