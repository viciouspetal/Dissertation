def run_scaled_decision_tree_classification(X, y):
    x_train, x_test, y_train, y_test = train_test_split(X, y)

    dt = DecisionTreeClassifier()
    dt.fit(x_train, y_train)
    dt_predict = dt.predict(x_test)

    dt_acc_score = accuracy_score(y_test, dt_predict)

    return dt_acc_score
    
fig_i = 0 # ensuring that each coefficient graph exists in its own file
for method in scaled_data_ref_map_downscaled.keys():
    score = run_scaled_decision_tree_classification(
        scaled_data_ref_map_downscaled[method], y)
    print('For {0} score is: {1} '.format(method, format_dec(score*100)))