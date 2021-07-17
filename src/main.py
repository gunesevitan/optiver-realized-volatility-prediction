import yaml
import pandas as pd

import preprocessing_utils
from preprocessing import PreprocessingPipeline
from trainer import Trainer


if __name__ == '__main__':

    config = yaml.load(open('../config.yaml', 'r'), Loader=yaml.FullLoader)
    df_train = pd.read_csv(
        '../data/train.csv',
        dtype=preprocessing_utils.train_test_dtypes['train']
    )
    df_test = pd.read_csv(
        '../data/test.csv',
        usecols=['stock_id', 'time_id'],
        dtype=preprocessing_utils.train_test_dtypes['test']
    )

    preprocessing_pipeline = PreprocessingPipeline(
        df_train,
        df_test,
        **config['preprocessing']
    )
    df_train, df_test = preprocessing_pipeline.transform()

    print(f'\nProcessed Training Set Shape: {df_train.shape}')
    print(f'Processed Training Set Memory Usage: {df_train.memory_usage().sum() / 1024 ** 2:.2f} MB')
    print(f'Processed Test Set Shape: {df_test.shape}')
    print(f'Processed Test Set Memory Usage: {df_test.memory_usage().sum() / 1024 ** 2:.2f} MB')

    trainer = Trainer(
        model_name=config['model_name'],
        model_path=None,
        model_parameters=config['model'],
        training_parameters=config['training']
    )
    trainer.train_and_validate(df_train)