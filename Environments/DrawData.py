import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_results(folder="./Resultados"):
    results = pd.read_excel(f"{folder}/RESULTADOS.xlsx", sheet_name="resultados")
    with open(f'{folder}/I_results.pkl', 'rb') as f:
        I_results = pickle.load(f)
    with open(f'{folder}/X_results.pkl', 'rb') as f:
        X_results = pickle.load(f)
    with open(f'{folder}/Y_results.pkl', 'rb') as f:
        Y_results = pickle.load(f)
    with open(f'{folder}/W_results.pkl', 'rb') as f:
        W_results = pickle.load(f)
    with open(f'{folder}/D.pkl', 'rb') as f:
        D = pickle.load(f)
    with open(f'{folder}/item_indices.pkl', 'rb') as f:
        item_indices = pickle.load(f)
    with open(f'{folder}/customer_indices.pkl', 'rb') as f:
        customer_indices = pickle.load(f)
    with open(f'{folder}/K1.pkl', 'rb') as f:
        K1 = pickle.load(f)
    with open(f'{folder}/K2.pkl', 'rb') as f:
        K2 = pickle.load(f)
    with open(f'{folder}/K3.pkl', 'rb') as f:
        K3 = pickle.load(f)
    with open(f'{folder}/T.pkl', 'rb') as f:
        T = pickle.load(f)

    return results, I_results, X_results, Y_results, W_results, D, item_indices, customer_indices, K1, K2, K3, T


def plotNet(X_results, sets, T):
    X_values = []
    for i in sorted(sets):
        t_values = []
        for t in range(1,len(T)):
            x = []
            for j in range(len(X_results)):
                x.append(X_results[j][i,t])
            t_values.append(x)   
        X_values.append(t_values)

    num_configs = len(X_values[0][0])
    num_periods = len(T) - 1  # Exclude the first period
    net_production = np.zeros((num_configs, num_periods))

    # Calculate the net production for each configuration for each period
    for t in range(num_periods):
        for config_idx in range(num_configs):
            for item_values in X_values:
                net_production[config_idx, t] += item_values[t][config_idx]

    # Plot the net production
    x_labels = T[1:]  # Use time periods excluding the first one
    x = np.arange(len(x_labels))  # Label locations
    width = 0.8 / num_configs  # Width of the bars

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab20', num_configs)  # Change color palette

    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.bar(x + config_idx * width, values, width, label=f'Config {config_idx + 1}', color=colors(config_idx))

    # Add labels, title, and legend
    ax.set_xlabel('Time Period')
    ax.set_ylabel('Net value')
    ax.set_title('Net value for Each Configuration in Each Time Period')
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.legend()

    # Add vertical lines to separate time periods
    for pos in x:
        ax.axvline(pos + width * num_configs, color='grey', linestyle='--')

    # Show the plot
    plt.show()

def plotItem(X_results, T, item):
    X_values = []
    for t in range(1,len(T)):
        x = []
        for j in range(len(X_results)):
            x.append(X_results[j][item, t])   
        X_values.append(x)

    num_configs = len(X_values[0])
    num_periods = len(T) - 1  # Exclude the first period
    net_production = np.zeros((num_configs, num_periods))

    # Calculate the net production for each configuration for each period
    for t in range(num_periods):
        for config_idx in range(num_configs):
            net_production[config_idx, t] += X_values[t][config_idx]

    # Plot the net production
    x_labels = T[1:]  # Use time periods excluding the first one
    x = np.arange(len(x_labels))  # Label locations
    width = 0.8 / num_configs  # Width of the bars

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab20', num_configs)  # Change color palette

    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.bar(x + config_idx * width, values, width, label=f'Config {config_idx + 1}', color=colors(config_idx))

    # Add labels, title, and legend
    ax.set_xlabel('Time Period')
    ax.set_ylabel('Value')
    ax.set_title(f'Value for Each Configuration in Each Time Period for item {item}')
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.legend()

    # Add vertical lines to separate time periods
    for pos in x:
        ax.axvline(pos + width * num_configs, color='grey', linestyle='--')

    # Show the plot
    plt.show()


results, I_results, X_results, Y_results, W_results, D, item_indices, customer_indices, K1, K2, K3, T = load_results()

plotNet(X_results, K1+K3, T)
plotNet(Y_results, K2+K3, T)
plotNet(I_results, K1+K2+K3, T)
plotItem(I_results, T, 1)

