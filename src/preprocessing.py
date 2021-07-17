import validation


class PreprocessingPipeline:

    def __init__(self, df_train, df_test, split_type, n_splits, shuffle, random_state):

        self.df_train = df_train.copy(deep=True)
        self.df_test = df_test.copy(deep=True)
        self.split_type = split_type
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def _get_folds(self):

        if self.split_type == 'stratified':
            validation.get_stratified_folds(
                df_train=self.df_train,
                n_splits=self.n_splits,
                shuffle=self.shuffle,
                random_state=self.random_state
            )
        elif self.split_type == 'group':
            validation.get_group_folds(
                df_train=self.df_train,
                n_splits=self.n_splits
            )

    def transform(self):

        self._get_folds()

        return self.df_train, self.df_test