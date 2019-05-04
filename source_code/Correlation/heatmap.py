def correlation_graph(df_correlation, graph_title, is_mask_on=True):
    mask = np.zeros_like(df_correlation, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots()
    ax.set(title=graph_title)
    cmap = sb.diverging_palette(220, 10, as_cmap=True)
    filenameToBeSavedAs= graph_title.replace(' ', '_')
    if is_mask_on:
        sb.heatmap(df_correlation, mask=mask, cmap=cmap, vmax=1,square=True, linewidths=.5, cbar_kws={"shrink": .8}, ax=ax);
    else:
        sb.heatmap(df_correlation, cmap=cmap, vmax=1,square=True, linewidths=.5, cbar_kws={"shrink": .8}, ax=ax);
    plt.savefig(default_figure_out_path+'/'+filenameToBeSavedAs+default_figure_ext, bbox_inches='tight')