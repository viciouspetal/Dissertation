def graph_variance_bar_plot(data, key, isUpsampled, graph_size='ml', rows_to_drop=['file_age_in_sec'], fig_i=0):

    set_graph_size(graph_size)
    tmp_df = pd.DataFrame(data[key]).drop(rows_to_drop, axis='rows')
    unstacked = tmp_df.T.unstack().to_frame()
    plt.figure(fig_i)
    ax = sb.barplot(
        x=unstacked.index.get_level_values(0),
        y=unstacked[0]);

    ax.set(title='High Variance Columns Plot', xlabel='Column Name', ylabel='Variance Value')

    # make x-axis labels vertical
    for item in ax.get_xticklabels():
        item.set_rotation(90)
    
    # checking which label is appropriate for the graph name depending on the dataset provided, 
    # e.g. upsample vs downsample    
    resample_direction=''
    if isUpsampled:
        resample_direction = ' upsampled '
    else:
        resample_direction = ' downsampled '
    path = default_figure_out_path+'/variance'
    save_graph('Comparison of variance per column for ' + key + resample_direction+'dataset', path)
    fig_i=fig_i+1