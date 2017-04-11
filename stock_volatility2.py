import pandas as pd
import numpy as np
import glob


def vol(df, mode):
    '''

    :param df: before or after stock data frame
    :param mode: 1 - before
                 0 - after
    :return: return the std for the data frame
    '''

    #intvl_list = [5, 10, 30, 60, 120]
    intvl_list = np.arange(120)

    dic = {}

    for i in intvl_list:
        if mode:
            dic[str(-i)] = df.iloc[-i:, 7].std()
        else:
            dic[str(i)] = df.iloc[:i, 7].std()

    return dic


def auto_vol(df):

    data = df.copy()
    output = pd.DataFrame(columns=[str(i) for i in np.arange(-120, 121)])

    for date in set(data.loc[:, 'release_script']):

        temp_df1 = data.loc[data.release_script == date, :]

        df_before = temp_df1.loc[temp_df1.timestamp < temp_df1.release_script, :]

        df_after = temp_df1.loc[temp_df1.timestamp > temp_df1.release_script, :]

        dic = {**vol(df_before, 1), **vol(df_after, 0)}

        for key in dic.keys():
            output.loc[date, key] = dic[key]

    return output


files = glob.glob('final_data/*.csv')

data = pd.DataFrame()

for file in files:
    try:
        ticker = file[file.rfind('_')+1:-4]
        df = pd.read_csv(file, index_col=None, header=0)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['release_script'] = pd.to_datetime(df['release_script'])

        temp_df = auto_vol(df)
        temp_df.loc[:, 'ticker'] = ticker

        data = pd.concat([data,temp_df])
    except:
        print(file)

data.to_csv('stock_vol_240.csv')

