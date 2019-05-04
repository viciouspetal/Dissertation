def print_class_balance(df): 
    bug_row_count = len(df.index[df['is_bug'] == True].tolist())
    non_bug_row_count = len(df.index[df['is_bug'] == False].tolist())
    bug_percent = get_percent(bug_row_count / df.shape[0])
    non_bug_percent = get_percent(non_bug_row_count / df.shape[0])
    
    print('The number of bug records is, {0}, {1}\%. Non bug records count {2}, {3}\%'.format(bug_row_count, bug_percent, non_bug_row_count, non_bug_percent))