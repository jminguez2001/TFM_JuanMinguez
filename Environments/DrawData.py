import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
# Determinar la ruta absoluta del directorio que contiene este script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Determinar la ruta absoluta del directorio raíz del proyecto (un nivel arriba del directorio actual)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(project_root)
# Importar el módulo desde el paquete Environments
try:
    from Environments.chargeEnvironment import chargeEnv
    from Environments.chargeSetParams import charge_SetParams
except ModuleNotFoundError as e:
    print("Error al importar el módulo:", e)
    print("Por favor, verifica la ruta del módulo y asegúrate de que es correcta.")
    sys.exit(1)


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

    return results, I_results, X_results, Y_results, W_results


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
    x_labels = [date.strftime('%y-%m-%d') for date in T[1:]]  
    x = np.arange(len(x_labels))  # Label locations
    width = 0.5 / num_configs  # Width of the bars

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
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

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
    x_labels = [date.strftime('%y-%m-%d') for date in T[1:]] 
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
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend()

    # Add vertical lines to separate time periods
    for pos in range(x):
        ax.axvline(pos, color='grey', linestyle='--')

    # Show the plot
    plt.show()
    
def plot_inventory(I, time_period, T):
    """
    Genera un gráfico de barras que muestra el inventario para cada ítem en un período de tiempo dado.

    Args:
        I_results (list): Lista de diccionarios con inventarios, donde la clave es una tupla (i, t) que representa el ítem y el período de tiempo.
        time_period (int): El periodo de tiempo para el cual se desea visualizar el inventario.
        T (list): lista de periodos de tiempo

    Returns:
        None: Muestra un gráfico de barras donde el eje X representa los ítems y el eje Y representa el inventario para el período de tiempo dado.
    """

    # Filtra el inventario para el período de tiempo dado
    inventory_for_period = {i: inventory for (i, t), inventory in I.items() if t == time_period}

    # Crea listas de ítems y sus inventarios para el período de tiempo dado
    items = list(inventory_for_period.keys())
    inventories = list(inventory_for_period.values())

    # Crea la gráfica de barras
    plt.figure(figsize=(10, 6))
    plt.bar(items, inventories, color='blue')

    # Agrega títulos y etiquetas
    plt.title(f"Inventario por ítem en el período de tiempo {T[time_period].strftime('%y-%m-%d')}")
    plt.xlabel("Ítem")
    plt.ylabel("Inventario")

    # Muestra la gráfica
    plt.show()

if __name__ == "__main__":
    results, I_results, X_results, Y_results, W_results = load_results()
    BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv = chargeEnv(mode = results["Environment"].values[0])
    NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, c_invent, Q_invent, Q_fabrica, MOQ1, MOQ2, lt, ltf, I_0, alpha = charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv)
        
    

    plotNet(X_results, K3, T)
    plotNet(Y_results, K3, T)
    plotNet(I_results, K3, T)
    # #plotItem(I_results, T, 1)
    # for i in range(len(I_results)): plot_inventory(I_results[i], 0, T)
    # plot_inventory(I_results[0], 0, T)
    plot_inventory(I_results[0], 12, T)