def get_majority_and_minority_classes(df, target_col, vals=[0, 1]):
    df_0 = df[df[target_col] == vals[0]]
    df_1 = df[df[target_col] == vals[1]]
    df_majority = pd.DataFrame
    df_minority = pd.DataFrame

    # check which is majority class
    if df_0.shape[0] > df_1.shape[0]:
        df_majority = df_0
        df_minority = df_1
    else:
        df_majority = df_1
        df_minority = df_0

    return df_majority, df_minority