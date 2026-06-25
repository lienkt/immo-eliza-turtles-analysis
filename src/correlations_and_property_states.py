import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os
import seaborn as sns

def correlations_matrix(df, base_dir):
    """
    Function creating a correlation matrix and saves it
    :params: pandas.DataFrame
    :params: string root folder path
    """
    numerical = df[['price', 'price_per_m2','livable_surface', 'total_surface', 'bedroom_count', 'swimming_pool', 'property_state', 'build_year', "energy_consumption_kWh/m2/year", 'nearest_city_distance_km', "preschool_distance_m", "train_station_distance_m", "supermarket_distance_m"]]

    numerical['nearest_city_distance_km'] = numerical['nearest_city_distance_km'].round().astype("Int64")

    states_dict = {"Excellent": 5, "Fully renovated": 3, "New": 4, "Normal": 2, "To demolish": None, "To renovate": 1, "To restore": None, "Under construction": None}
    numerical['property_state'] = numerical['property_state'].map(states_dict)

    sns.set_theme(style='white', palette='muted', font_scale=1.1)
    fig, ax = plt.subplots(figsize=(10, 9))

    corr = numerical.corr(method='spearman')
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, ax=ax, mask=mask, cmap='RdBu_r', center=0, vmin=-1, vmax=1, annot=True, fmt='.2f',
                linewidths=1.5, linecolor='white',annot_kws={'size': 9, 'weight': 'medium'}, cbar_kws={'shrink': 0.7, 'label': 'Spearman Correlation'})
    ax.set_title('Correlation matrix', fontsize=16, pad=25, fontweight='bold', loc='left')

    ax.set_xticklabels([label.get_text().replace('_', ' ').title() for label in ax.get_xticklabels()], rotation=45, horizontalalignment='right', fontsize=10)
    ax.set_yticklabels([label.get_text().replace('_', ' ').title() for label in ax.get_yticklabels()], rotation=0, fontsize=10)

    ax.tick_params(left=False, bottom=True)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, './images/correlation_matrix.png'), dpi=130, bbox_inches='tight')
    plt.close(fig=fig)

def price_vs_property_states(df, base_dir, PALETTE):
    """
    Function creating a grouped bar chart of price per meter squared in 
    relation to property states and saves it
    :params: pandas.DataFrame
    :params: string root folder path
    :params: list of string hex colours 
    """
    property_state = df.groupby('property_state', observed=True)["price_per_m2"].agg(["count", "median", "mean"])
    new_row_order = ['New', 'Excellent', 'Fully renovated', 'Under construction', 'Normal', 'To renovate', 'To restore', 'To demolish']
    property_state = property_state.reindex(new_row_order)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Cheaper prices can hide "work ahead"', fontweight='bold', fontsize=20)
    property_state["median"].plot(kind='bar', ax=axes[0], color=PALETTE[0], edgecolor='white', width=0.75, rot=45)

    axes[0].set_title('Property state seems to influence prices', fontsize=16, pad=20)
    axes[0].set_ylabel('Median Prices / m$^{2}$', fontweight='bold')
    axes[0].set_xlabel('Property states', fontweight='bold')
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'€{x/1000:.1f}k'))

    for container in axes[0].containers:
        labels = [f"{v.get_height():.0f}" for v in container]
        axes[0].bar_label(
            container, 
            padding=4, 
            fontsize=9,
            fontweight='bold',
            labels=labels
        )

    axes[1].barh(property_state.index[::-1], property_state['count'].values[::-1],
                color=PALETTE[1], alpha=0.85, edgecolor='white')

    for i, (state, val) in enumerate(zip(property_state.index[::-1], property_state["count"].values[::-1])):
        axes[1].text(val + 1, i, str(val), va='center', fontsize=9, fontweight='bold')

    axes[1].set_xlabel('Number of Entries', fontweight='bold')
    axes[1].set_title('Very few properties to restore, demolish or in contruction', fontsize=16, pad=20)

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, './images/price_vs_property_states.png'), dpi=130, bbox_inches='tight')
    plt.close(fig=fig)