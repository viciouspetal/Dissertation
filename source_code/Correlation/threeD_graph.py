def create_3d_graph(x_col,y_col,z_col, df,title, colour='skyblue', graph_size='m'):
    df_3d_graph=pd.DataFrame({'X': df[x_col], 'Y': df[y_col], 'Z': df[z_col] })

    # plot
    set_graph_size(graph_size)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df_3d_graph['X'], df_3d_graph['Y'], df_3d_graph['Z'], c='skyblue', s=60)
    ax.view_init(30, 185)
    ax.set(
            title=title,
            xlabel=x_col,
            ylabel=y_col,
            zLabel=z_col
        );
    save_graph('Correlation_between_attributes_'+x_col+'_'+y_col+'_'+z_col, default_figure_out_path+'/3d')
    plt.show()