import numpy as np
import pandas as pd
from tqdm import tqdm

import path_utils
import preprocessing_utils


def get_all_book_statistics(df):

    """
    Calculate means and stds of book sequences on entire training set after forward filling

    Parameters
    ----------
    df [pandas.DataFrame of shape (n_samples, 3)]: Training set

    Returns
    -------
    means (dict): Means of specified features on entire training set
    stds (dict): Stds of specified features on entire training set
    """

    book_features = [
        #'bid_price1', 'ask_price1', 'bid_price2', 'ask_price2',
        #'bid_size1', 'ask_size1', 'bid_size2', 'ask_size2',
        #'bid_price1_absolute_log_returns', 'ask_price1_absolute_log_returns', 'bid_price2_absolute_log_returns', 'ask_price2_absolute_log_returns',
        'bid_size1_absolute_log_returns', 'ask_size1_absolute_log_returns', 'bid_size2_absolute_log_returns', 'ask_size2_absolute_log_returns',
        'wap1', 'wap2', 'wap3',
        'wap1_absolute_log_returns', 'wap2_absolute_log_returns', 'wap3_absolute_log_returns'
    ]
    df_books = pd.DataFrame(columns=book_features)

    for stock_id in tqdm(sorted(df['stock_id'].unique())):

        df_book = preprocessing_utils.read_book_data('train', stock_id, sort=True, forward_fill=True)

        df_book['bid_price1_absolute_log_returns'] = np.abs(np.log(df_book['bid_price1'] / df_book.groupby('time_id')['bid_price1'].shift(1)))
        df_book['ask_price1_absolute_log_returns'] = np.abs(np.log(df_book['ask_price1'] / df_book.groupby('time_id')['ask_price1'].shift(1)))
        df_book['bid_price2_absolute_log_returns'] = np.abs(np.log(df_book['bid_price2'] / df_book.groupby('time_id')['bid_price2'].shift(1)))
        df_book['ask_price2_absolute_log_returns'] = np.abs(np.log(df_book['ask_price2'] / df_book.groupby('time_id')['ask_price2'].shift(1)))
        df_book['bid_size1_absolute_log_returns'] = np.abs(np.log(df_book['bid_size1'] / df_book.groupby('time_id')['bid_size1'].shift(1)))
        df_book['ask_size1_absolute_log_returns'] = np.abs(np.log(df_book['ask_size1'] / df_book.groupby('time_id')['ask_size1'].shift(1)))
        df_book['bid_size2_absolute_log_returns'] = np.abs(np.log(df_book['bid_size2'] / df_book.groupby('time_id')['bid_size2'].shift(1)))
        df_book['ask_size2_absolute_log_returns'] = np.abs(np.log(df_book['ask_size2'] / df_book.groupby('time_id')['ask_size2'].shift(1)))

        df_book['wap1'] = (df_book['bid_price1'] * df_book['ask_size1'] + df_book['ask_price1'] * df_book['bid_size1']) /\
                          (df_book['bid_size1'] + df_book['ask_size1'])
        df_book['wap2'] = (df_book['bid_price2'] * df_book['ask_size2'] + df_book['ask_price2'] * df_book['bid_size2']) /\
                          (df_book['bid_size2'] + df_book['ask_size2'])
        df_book['wap3'] = ((df_book['bid_price1'] * df_book['ask_size1'] + df_book['ask_price1'] * df_book['bid_size1']) +
                           (df_book['bid_price2'] * df_book['ask_size2'] + df_book['ask_price2'] * df_book['bid_size2'])) /\
                          (df_book['bid_size1'] + df_book['ask_size1'] + df_book['bid_size2'] + df_book['ask_size2'])

        df_book['wap1_absolute_log_returns'] = np.abs(np.log(df_book['wap1'] / df_book.groupby('time_id')['wap1'].shift(1)))
        df_book['wap2_absolute_log_returns'] = np.abs(np.log(df_book['wap2'] / df_book.groupby('time_id')['wap2'].shift(1)))
        df_book['wap3_absolute_log_returns'] = np.abs(np.log(df_book['wap3'] / df_book.groupby('time_id')['wap3'].shift(1)))

        df_books = pd.concat([df_books, df_book.loc[:, book_features]], axis=0, ignore_index=True)

    df_books.fillna(0, inplace=True)
    means = df_books.mean(axis=0).to_dict()
    stds = df_books.std(axis=0).to_dict()
    return means, stds


def get_all_trade_statistics(df):

    """
    Calculate means and stds of trade sequences on entire training set after zero filling

    Parameters
    ----------
    df [pandas.DataFrame of shape (n_samples, 3)]: Training set

    Returns
    -------
    means (dict): Means of specified features on entire training set
    stds (dict): Stds of specified features on entire training set
    """

    trade_features = ['price', 'size', 'order_count']
    df_trades = pd.DataFrame(columns=trade_features)

    for stock_id in tqdm(sorted(df['stock_id'].unique())):

        df_trade = preprocessing_utils.read_trade_data(df, 'train', stock_id, sort=True, zero_fill=True)
        df_trades = pd.concat([df_trades, df_trade.loc[:, trade_features]], axis=0, ignore_index=True)

    df_trades.fillna(0, inplace=True)
    means = df_trades[df_trades['price'] != 0].mean(axis=0).to_dict()
    stds = df_trades[df_trades['price'] != 0].std(axis=0).to_dict()
    return means, stds


def get_stock_book_statistics(df):

    """
    Calculate means and stds of book sequences of every stock after forward filling

    Parameters
    ----------
    df [pandas.DataFrame of shape (n_samples, 3)]: Training set

    Returns
    -------
    df_stock_means [pandas.DataFrame of shape (n_stocks, n_features)]: Means of features for every every stock
    df_stock_stds [pandas.DataFrame of shape (n_stocks, n_features)]: Stds of features for every every stock
    """

    book_features = [
        'bid_price1', 'ask_price1', 'bid_price2', 'ask_price2',
        'bid_size1', 'ask_size1', 'bid_size2', 'ask_size2',
        'bid_price1_absolute_log_returns', 'ask_price1_absolute_log_returns', 'bid_price2_absolute_log_returns', 'ask_price2_absolute_log_returns',
        'bid_size1_absolute_log_returns', 'ask_size1_absolute_log_returns', 'bid_size2_absolute_log_returns', 'ask_size2_absolute_log_returns',
        'wap1', 'wap2', 'wap3',
        'wap1_absolute_log_returns', 'wap2_absolute_log_returns', 'wap3_absolute_log_returns'
    ]
    df_stock_means = pd.DataFrame(columns=['stock_id'] + book_features)
    df_stock_stds = pd.DataFrame(columns=['stock_id'] + book_features)

    for stock_id in tqdm(sorted(df['stock_id'].unique())):

        df_book = preprocessing_utils.read_book_data('train', stock_id, sort=True, forward_fill=True)
        df_book['bid_price1_absolute_log_returns'] = np.abs(np.log(df_book['bid_price1'] / df_book.groupby('time_id')['bid_price1'].shift(1)))
        df_book['ask_price1_absolute_log_returns'] = np.abs(np.log(df_book['ask_price1'] / df_book.groupby('time_id')['ask_price1'].shift(1)))
        df_book['bid_price2_absolute_log_returns'] = np.abs(np.log(df_book['bid_price2'] / df_book.groupby('time_id')['bid_price2'].shift(1)))
        df_book['ask_price2_absolute_log_returns'] = np.abs(np.log(df_book['ask_price2'] / df_book.groupby('time_id')['ask_price2'].shift(1)))
        df_book['bid_size1_absolute_log_returns'] = np.abs(np.log(df_book['bid_size1'] / df_book.groupby('time_id')['bid_size1'].shift(1)))
        df_book['ask_size1_absolute_log_returns'] = np.abs(np.log(df_book['ask_size1'] / df_book.groupby('time_id')['ask_size1'].shift(1)))
        df_book['bid_size2_absolute_log_returns'] = np.abs(np.log(df_book['bid_size2'] / df_book.groupby('time_id')['bid_size2'].shift(1)))
        df_book['ask_size2_absolute_log_returns'] = np.abs(np.log(df_book['ask_size2'] / df_book.groupby('time_id')['ask_size2'].shift(1)))

        df_book['wap1'] = (df_book['bid_price1'] * df_book['ask_size1'] + df_book['ask_price1'] * df_book['bid_size1']) /\
                          (df_book['bid_size1'] + df_book['ask_size1'])
        df_book['wap2'] = (df_book['bid_price2'] * df_book['ask_size2'] + df_book['ask_price2'] * df_book['bid_size2']) /\
                          (df_book['bid_size2'] + df_book['ask_size2'])
        df_book['wap3'] = ((df_book['bid_price1'] * df_book['ask_size1'] + df_book['ask_price1'] * df_book['bid_size1']) +
                           (df_book['bid_price2'] * df_book['ask_size2'] + df_book['ask_price2'] * df_book['bid_size2'])) /\
                          (df_book['bid_size1'] + df_book['ask_size1'] + df_book['bid_size2'] + df_book['ask_size2'])

        df_book['wap1_absolute_log_returns'] = np.abs(np.log(df_book['wap1'] / df_book.groupby('time_id')['wap1'].shift(1)))
        df_book['wap2_absolute_log_returns'] = np.abs(np.log(df_book['wap2'] / df_book.groupby('time_id')['wap2'].shift(1)))
        df_book['wap3_absolute_log_returns'] = np.abs(np.log(df_book['wap3'] / df_book.groupby('time_id')['wap3'].shift(1)))

        stock_means = df_book.loc[:, book_features].mean().to_dict()
        stock_means['stock_id'] = stock_id
        stock_stds = df_book.loc[:, book_features].std().to_dict()
        stock_stds['stock_id'] = stock_id
        df_stock_means = df_stock_means.append(stock_means, ignore_index=True)
        df_stock_stds = df_stock_stds.append(stock_stds, ignore_index=True)

    df_stock_means['stock_id'] = df_stock_means['stock_id'].astype(np.uint8)
    df_stock_stds['stock_id'] = df_stock_stds['stock_id'].astype(np.uint8)
    return df_stock_means, df_stock_stds


def get_stock_trade_statistics(df):

    """
    Calculate means and stds of trade sequences of every stock after zero filling

    Parameters
    ----------
    df [pandas.DataFrame of shape (n_samples, 3)]: Training set

    Returns
    -------
    df_stock_means [pandas.DataFrame of shape (n_stocks, n_features)]: Means of features for every every stock
    df_stock_stds [pandas.DataFrame of shape (n_stocks, n_features)]: Stds of features for every every stock
    """

    trade_features = ['price', 'size', 'order_count']
    df_stock_means = pd.DataFrame(columns=['stock_id'] + trade_features)
    df_stock_stds = pd.DataFrame(columns=['stock_id'] + trade_features)

    for stock_id in tqdm(sorted(df['stock_id'].unique())):

        df_trade = preprocessing_utils.read_trade_data(df, 'train', stock_id, sort=True, zero_fill=True)

        stock_means = df_trade.loc[df_trade['price'] != 0, trade_features].mean().to_dict()
        stock_means['stock_id'] = stock_id
        stock_stds = df_trade.loc[df_trade['price'] != 0, trade_features].std().to_dict()
        stock_stds['stock_id'] = stock_id
        df_stock_means = df_stock_means.append(stock_means, ignore_index=True)
        df_stock_stds = df_stock_stds.append(stock_stds, ignore_index=True)

    df_stock_means['stock_id'] = df_stock_means['stock_id'].astype(np.uint8)
    df_stock_stds['stock_id'] = df_stock_stds['stock_id'].astype(np.uint8)
    return df_stock_means, df_stock_stds


if __name__ == '__main__':

    df_train = pd.read_csv(f'{path_utils.DATA_PATH}/train.csv')

    statistics_type = 'global'

    if statistics_type == 'global':

        book_global_means, book_global_stds = get_all_book_statistics(df_train)
        trade_global_means, trade_global_stds = get_all_trade_statistics(df_train)

        print(f'Book Global Means\n{book_global_means}\n')
        print(f'Book Global Stds\n{book_global_stds}\n')
        print(f'Trade Global Means\n{trade_global_means}\n')
        print(f'Trade Global Stds\n{trade_global_stds}\n')

    elif statistics_type == 'local':

        df_book_stock_means, df_book_stock_stds = get_stock_book_statistics(df_train)
        df_book_stock_means.to_csv('book_stock_means.csv', index=False)
        df_book_stock_stds.to_csv('book_stock_stds.csv', index=False)
        df_trade_stock_means, df_trade_stock_stds = get_stock_trade_statistics(df_train)
        df_trade_stock_means.to_csv('trade_stock_means.csv', index=False)
        df_trade_stock_stds.to_csv('trade_stock_stds.csv', index=False)
