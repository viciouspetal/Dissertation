def print_logistic_regression_scores(penalty, algorithm, x_test, y_test):
    print('Score for {0} is {1}'.format(penalty, algorithm.score(x_test, y_test)))
    print('Probability of classification for {0} is {1}'.format(penalty, algorithm.predict_proba(x_test)))

def run_logistic_regression(df, penalty, target_col, other_cols_to_drop):
    # run te regression
    other_cols_to_drop = np.append(other_cols_to_drop, [target_col])
    X = df.drop(other_cols_to_drop, axis='columns')  # X = features
    y = df[target_col]  # y = prediction target

    lr_l1 = LogisticRegression(penalty=penalty)
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    lr_l1.fit(x_train, y_train)
    
    # generate graph depicting coefficient impact on model
    ax.set(
        title='Coefficients for Logistic Regression with ' + penalty + ' Regularization',
        xlabel='Coefficient',
        ylabel='Value'
    );
    plt.plot(lr_l1.coef_.flatten())

    print_logistic_regression_scores(penalty, lr_l1, x_test, y_test)


def run_scaled_logistic_regression(X, penalty, y, fig_i=0):
    plt.figure(fig_i)
    lr_l1 = LogisticRegression(penalty=penalty)
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    lr_l1.fit(x_train, y_train)
    ax.set(
        title='Coefficients for Logistic Regression with ' + penalty + ' Regularization',
        xlabel='Coefficient',
        ylabel='Value'
    );
    plt.plot(lr_l1.coef_.flatten())

    score = lr_l1.score(x_test, y_test)
    proba = lr_l1.predict_proba(x_test)

    return (score, proba)