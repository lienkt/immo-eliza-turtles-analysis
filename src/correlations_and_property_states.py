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

    fig, ax = plt.subplots(figsize=(8, 8))

    corr = numerical.corr(method='spearman')
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, ax=ax, mask=mask, cmap='RdBu_r', center=0, vmin=-1, vmax=1, annot=True, fmt='.2f',
                linewidths=0.5, annot_kws={'size': 8}, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation matrix')
    
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, './images/correlation_matrix.png'), dpi=130, bbox_inches='tight')
    plt.close(fig=fig)

def price_vs_property_states(df, base_dir, PALETTE):
    """
    Function creating a grouped bar chart of price per 
    property states and saves it
    :params: pandas.DataFrame
    :params: string root folder path
    :params: list of string hex colours 
    """
    property_state = df.groupby('property_state', observed=True)["price"].agg(["count", "median", "mean"])
    new_row_order = ['Excellent', 'New', 'Fully renovated', 'Normal', 'To renovate', 'To restore', 'To demolish', 'Under construction']
    property_state = property_state.reindex(new_row_order)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    property_state[["median", "mean"]].plot(kind='bar', ax=axes[0], color=PALETTE, edgecolor='white', width=0.75, rot=45)

    axes[0].set_title('Cheaper price can mean work ahead')
    axes[0].set_ylabel('Prices €')
    axes[0].set_xlabel('Property states')
    axes[0].legend(title='Agg', fontsize=8)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'€{x/1000:.0f}k'))

    for container in axes[0].containers:
        labels = [f"{v.get_height()/1000:.0f}k" for v in container]
        axes[0].bar_label(
            container, 
            padding=4, 
            fontsize=9,
            labels=labels
        )

    property_state[["count"]].plot(kind='bar', ax=axes[1], color=PALETTE, edgecolor='white', width=0.75, rot=45)

    axes[1].set_title('Too few demolitions and constructions')
    axes[1].set_ylabel('Entries')
    axes[1].set_xlabel('Property states')

    for container in axes[1].containers:
        axes[1].bar_label(
            container, 
            padding=4, 
            fontsize=9
        )

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, './images/price_vs_property_states.png'), dpi=130, bbox_inches='tight')
    plt.close(fig=fig)