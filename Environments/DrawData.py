import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import datetime as dt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


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
    """Lee los archivos de los resultados y los devuelve como listas

    Args:
        folder (str, optional): path de los archivos con los resultados.

    Returns:
        tuple: listas con los resultados.
    """
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

   
def plot_inventory(I, time_period, T):
    """
    Genera un gráfico de barras que muestra el inventario para cada ítem en un periodo de tiempo dado.

    Args:
        I (dict): Diccionario con inventarios, donde la clave es una tupla (i, t) que representa el ítem y el periodo de tiempo.
        time_period (int): El periodo de tiempo para el cual se desea visualizar el inventario.
        T (list): Lista de periodos de tiempo.

    Returns:
        None: Muestra un gráfico de barras donde el eje X representa los ítems y el eje Y representa el inventario para el periodo de tiempo dado.
    """
    if time_period!= 0:
        # Filtra el inventario para el periodo de tiempo dado
        inventory_for_period = {i: inventory for (i, t), inventory in I.items() if t == time_period}
    else:
        inventory_for_period = {i: inventory for i, inventory in I.items()}


    # Separa el inventario del ítem 62 del resto
    inventory_62 = inventory_for_period.pop(62)
    items_except_62 = list(inventory_for_period.keys())
    inventories_except_62 = list(inventory_for_period.values())

    # Crea la gráfica de barras
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Grafica los ítems excepto el 62 en el eje principal
    ax1.bar(items_except_62, inventories_except_62, color='lightblue', label='Otros ítems')

    # Configuración del primer eje
    ax1.set_xlabel("Ítem")
    ax1.set_ylabel("Inventario")
    ax1.set_title(f"Inventario por ítem en el periodo de tiempo {T[time_period].strftime('%d-%m-%y')}")

    # Crear un segundo eje para el ítem 62
    ax2 = ax1.twinx()
    ax2.bar([62], [inventory_62], color='blue', label='Ítem 62')
    ax2.set_ylabel('Inventario Ítem 62', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylim(bottom = 0)
    if inventory_62 == 0:
        ax2.set_ylim(bottom = 0, top = 1000)

    # Agregar leyendas
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Muestra la gráfica
    plt.show()

def plot_inventory_vs_cost(I, time_period, T, c_std):
    """
    Genera un gráfico de líneas que muestra el inventario para cada ítem en un periodo de tiempo dado, junto con el coste comprometido en un gráfico de barras.

    Args:
        I (dict): Diccionario con inventarios, donde la clave es una tupla (i, t) que representa el ítem y el periodo de tiempo.
        time_period (int): El periodo de tiempo para el cual se desea visualizar el inventario.
        T (list): Lista de periodos de tiempo.
        c_std (dict): Costes estándar por ítem.

    Returns:
        None: Muestra un gráfico de líneas para el inventario y un gráfico de barras para el coste comprometido.
    """
    # Filtra el inventario y el coste para el periodo de tiempo dado
    if time_period != 0:
        inventory_for_period = {i: inventory for (i, t), inventory in I.items() if t == time_period}
        inventory_cost_for_period = {i: inventory * c_std[i] for (i, t), inventory in I.items() if t == time_period}
    else:
        inventory_for_period = {i: inventory for i, inventory in I.items()}
        inventory_cost_for_period = {i: inventory * c_std[i] for i, inventory in I.items()}

    items = list(inventory_for_period.keys())
    inventory_values = list(inventory_for_period.values())
    cost_values = list(inventory_cost_for_period.values())

    x = np.arange(len(items))  # Posiciones en el eje X

    # Crea la gráfica
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Grafica el inventario como barras en el eje principal
    ax1.bar(x, inventory_values, color='lightblue', label='Inventario')

    # Configuración del primer eje
    ax1.set_xlabel("Ítem", fontsize = 16)
    ax1.set_ylabel("Inventario", fontsize = 16)
    ax1.tick_params(axis='y', size = 12)
    # ax1.set_title("Inventario e Inventario comprometido por ítem")
    ax1.set_xticks(x)
    ax1.set_xticklabels(items)

    # Ajustar los xticks para que aparezcan cada 5 ítems
    ax1.set_xticks(np.arange(0, len(items), 5))

    # Crear un segundo eje para el coste del inventario
    ax2 = ax1.twinx()
    ax2.plot(x, cost_values, marker='o', linestyle='--', color='red', alpha=0.6, label='Capital comprometido')
    ax2.set_ylabel('Euros', color='red', fontsize = 16)
    ax2.tick_params(axis='y', labelcolor='red', size = 12)
    ax2.set_ylim(bottom=0)

    # Agregar leyendas
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Muestra la gráfica
    plt.show()


def plot_demand_satisfaction(D, w, T, LEVEL0, R, item_indices, customer_indices):
    """
    Crea un gráfico de barras que muestra la demanda satisfecha y no satisfecha por artículo.

    Args:
        D (list): Lista de matrices de demanda, que representa la demanda de unidades del artículo i por el cliente r en el periodo t.
        w (dict): Diccionario que indica si el artículo i pedido por el cliente r en el periodo t está satisfecho (1) o no (0).
        T (list): Conjunto de periodos.
        LEVEL0 (list): Conjunto de ítems a nivel 0.
        R (list): Conjunto de clientes.
        item_indices (dict): mapea los ítems i, con los indices de D
        customer_indices (dict): mapea los customer r, con los indices de D
    """
    
    # Inicializar la demanda total y la demanda satisfecha para cada artículo
    total_demand = {i: 0 for i in LEVEL0}
    fulfilled_demand = {i: 0 for i in LEVEL0}

    # Calcular la demanda total y la demanda satisfecha para cada artículo
    for t in range(1,len(T)):
        for i in LEVEL0:
            for r in R:
                total_demand[i] += D[t][item_indices[i], customer_indices[r]]
                fulfilled_demand[i] +=D[t][item_indices[i], customer_indices[r]] * w[i,r,t]

    # Calcular la demanda no satisfecha para cada artículo
    unfulfilled_demand = {i: total_demand[i] - fulfilled_demand[i] for i in LEVEL0}

    # Preparar los datos para el gráfico
    labels = [f'{i}' for i in LEVEL0]
    fulfilled = [fulfilled_demand[i] for i in LEVEL0]
    unfulfilled = [unfulfilled_demand[i] for i in LEVEL0]

    x = np.arange(len(labels))  # ubicaciones de las etiquetas
    width = 0.35  # ancho de las barras

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    bars1 = ax.bar(x, fulfilled, width, label='Satisfecho')
    bars2 = ax.bar(x, unfulfilled, width, bottom=fulfilled, label='No Satisfecho')

    # Ajustar los límites del eje y para asegurar que todas las barras sean visibles
    max_height = max([f + u for f, u in zip(fulfilled, unfulfilled)])
    ax.set_ylim(0, max_height * 1.1)
    
    # Añadir etiquetas y título
    ax.set_xlabel('Ítems a nivel 0')
    ax.set_ylabel('Unidades')
    ax.set_title('Demanda Satisfecha y No Satisfecha por Ítem')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir valores en la parte superior de las barras
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate('{}'.format(height),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # Desplazamiento vertical de 3 puntos
                            textcoords="offset points",
                            ha='center', va='bottom')

    add_labels(bars1)
    add_labels(bars2)

    plt.show()
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
    x_labels = [i for i in range(1, len(T))]  
    x = np.arange(len(x_labels))  # Label locations
    width = 0.7 / num_configs  # Width of the bars

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab20', num_configs)  # Change color palette

    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.bar(x + config_idx * width, values, width, label=f'Escenario {config_idx}', color=colors(config_idx))

    # Add labels, title, and legend
    ax.set_xlabel('Periodo', fontsize = 16)
    ax.set_ylabel('Unidades', fontsize = 16)
    ax.set_title('Unidades fabricadas por periodo', fontsize = 18)
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.legend()

    # Add vertical lines to separate time periods
    for pos in x:
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

    # Show the plot
    plt.show()

def plotNet_Costes(X_results, sets, T, c):
    X_values = []
    for i in sorted(sets):
        t_values = []
        for t in range(1, len(T)):
            x = []
            for j in range(len(X_results)):
                x.append(X_results[j][i,t]*c[i])
            t_values.append(x)   
        X_values.append(t_values)

    num_configs = len(X_values[0][0])
    num_periods = len(T)-1 
    net_production = np.zeros((num_configs, num_periods))

    # Calculate the net production for each configuration for each period
    for t in range(num_periods):
        for config_idx in range(num_configs):
            for item_values in X_values:
                net_production[config_idx, t] += item_values[t][config_idx]

    # Plot the net production
    x_labels = [i for i in range(1, len(T))]  
    x = np.arange(len(x_labels))  # Label locations
    width = 0.7 / num_configs  # Width of the bars

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab20', num_configs)  # Change color palette

    
    labels_PLANINV = ['0', 'HC=0, Q=1', 'HC=0, Q=0.75', 'HC=0, Q=0.5', 'HC=1, Q=1', 'HC=1, Q=0.75', 'HC=1, Q=0.5']
    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.bar(x + config_idx * width, values, width
               , label  =  labels_PLANINV[config_idx]
               # ,label=f'Escenario {config_idx}'
               ,color=colors(config_idx))

    # Add labels, title, and legend
    ax.set_xlabel('Periodo de Tiempo', fontsize = 16)
    ax.set_ylabel('Valor en Euros', fontsize = 16)
    # ax.set_title('Inversión en cada periodo de tiempo', fontsize = 18)
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.legend(loc = 'upper right')

    # Add vertical lines to separate time periods
    for pos in x:
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

    # Show the plot
    plt.show()
    
def plotNet_CostesLines(X_results, sets, T, c):
    X_values = []
    for i in sorted(sets):
        t_values = []
        for t in range(1, len(T)):
            x = []
            for j in range(len(X_results)):
                x.append(X_results[j][i,t]*c[i])
            t_values.append(x)   
        X_values.append(t_values)

    num_configs = len(X_values[0][0])
    num_periods = len(T)-1 
    net_production = np.zeros((num_configs, num_periods))

    # Calculate the net production for each configuration for each period
    for t in range(num_periods):
        for config_idx in range(num_configs):
            for item_values in X_values:
                net_production[config_idx, t] += item_values[t][config_idx]

    # Plot the net production
    x_labels = [i for i in range(1, len(T))]  
    x = np.arange(len(x_labels))  # Label locations
    width = 0.7 / num_configs  # Width of the bars

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab20', num_configs)  # Change color palette

    
    labels_PLANINV = ['0', 'HC=0, Q=1', 'HC=0, Q=0.75', 'HC=0, Q=0.5', 'HC=1, Q=1', 'HC=1, Q=0.75', 'HC=1, Q=0.5']
    colors_PLANINV = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.545),  (0.0, 0.0, 1.0), (0.678, 0.847, 0.902), (0.545, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.5, 0.5)]
    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.plot(x + config_idx * width, values, marker = 'o',linestyle = '--'
               , label  =  labels_PLANINV[config_idx]
               # ,label=f'Escenario {config_idx}'
               # ,color=colors(config_idx)
               ,color= colors_PLANINV[config_idx]
               )

    # Add labels, title, and legend
    ax.set_xlabel('Periodo de Tiempo', fontsize = 16)
    ax.set_ylabel('Valor en Euros', fontsize = 16)
    # ax.set_title('Inversión en cada periodo de tiempo', fontsize = 18)
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.legend(loc = 'upper right')

    # Add vertical lines to separate time periods
    for pos in x:
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

    # Show the plot
    plt.show()

    
def plotNetI_comprometido(X_results, sets, T, c_std):
    X_values = []
    for i in sorted(sets):
        t_values = []
        for t in range(len(T)):
            x = []
            for j in range(len(X_results)):
                x.append(X_results[j][i,t]*c_std[i]/1e6)
            t_values.append(x)   
        X_values.append(t_values)

    num_configs = len(X_values[0][0])
    num_periods = len(T)
    net_production = np.zeros((num_configs, num_periods))

    # Calculate the net production for each configuration for each period
    for t in range(num_periods):
        for config_idx in range(num_configs):
            for item_values in X_values:
                net_production[config_idx, t] += item_values[t][config_idx]

    # Plot the net production
    x_labels = [i for i in range(len(T))]  
    x = np.arange(len(x_labels))  # Label locations
    width = 0.7 / num_configs  # Width of the bars

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab10', num_configs)  # Change color palette

    labels_PLANINV = ['0', 'HC=0, Q=1', 'HC=0, Q=0.75', 'HC=0, Q=0.5', 'HC=1, Q=1', 'HC=1, Q=0.75', 'HC=1, Q=0.5']
    labels_PLANMOQVAR = ['I0=F0,rF=1,rC=1', 'I0=F0,rF=0.75,rC=1', 'I0=F0,rF=0.5,rC=1', 'I0=F0,rF=0.33,rC=1', 'I0=F0,rF=0,rC=1',
                         'I0=F1,rF=1,rC=1', 'I0=F1,rF=0.75,rC=1', 'I0=F1,rF=0.5,rC=1', 'I0=F1,rF=0.33,rC=1', 'I0=F1,rF=0,rC=1']
    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.bar(x + config_idx * width, values, width
            #    , label=f'Escenario {config_idx}'
            #    , label=labels_PLANINV[config_idx]
               , label=labels_PLANMOQVAR[config_idx]
               , color=colors(config_idx))

    # Add labels, title, and legend
    ax.set_xlabel('Periodo de Tiempo', fontsize = 16)
    ax.set_ylabel('Valor en millones de Euros', fontsize = 16)
    # ax.set_title('Inventario Comprometido en cada periodo de Tiempo', fontsize = 18)
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.legend()

    # Add vertical lines to separate time periods
    for pos in x:
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

    # Show the plot
    plt.show()    


def plotItem(X_results, T, item, titulo):
    X_values = []
    for t in range(1,len(T)):
        x = []
        for j in range(len(X_results)):
            x.append(X_results[j][item, t])   
        X_values.append(x)

    num_configs = len(X_values[0])
    num_periods = len(T) - 1  
    net_production = np.zeros((num_configs, num_periods))

    for t in range(num_periods):
        for config_idx in range(num_configs):
            net_production[config_idx, t] += X_values[t][config_idx]

    x_labels = [date.strftime('%d-%m-%y') for date in T[1:]] 
    x = np.arange(len(x_labels)) 
    width = 0.8 / num_configs  

    fig, ax = plt.subplots()
    colors = plt.get_cmap('tab20', num_configs) 

    for config_idx in range(num_configs):
        values = net_production[config_idx]
        ax.bar(x + config_idx * width, values, width
               #, label=f'Config {config_idx + 1}'
               , color=colors(config_idx))

    ax.set_xlabel('Periodo')
    ax.set_ylabel('Unidades')
    ax.set_title(titulo)
    ax.set_xticks(x + width * (num_configs - 1) / 2)
    ax.set_xticklabels(range(1,len(T)))
    # ax.legend()

    for pos in x:
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

    plt.show()


def plot_demand_by_period(D, w, T, LEVEL0, R, item_indices, customer_indices, add_second_bar=True, start_period=0):
    """
    Crea un gráfico de barras apiladas por periodo de tiempo, con la opción de añadir una segunda barra que subdivida en demanda satisfecha y no satisfecha.

    Args:
        D (list): Lista de matrices de demanda, que representa la demanda de unidades del artículo i por el cliente r en el periodo t.
        w (dict): Diccionario que indica si el artículo i pedido por el cliente r en el periodo t está satisfecho (1) o no (0).
        T (list): Conjunto de periodos.
        LEVEL0 (list): Conjunto de ítems a nivel 0.
        R (list): Conjunto de clientes.
        item_indices (dict): Mapea los ítems i con los índices de D.
        customer_indices (dict): Mapea los clientes r con los índices de D.
        add_second_bar (bool): Indica si se debe añadir una segunda barra para subdividir la demanda satisfecha y no satisfecha.
        start_period (int): Periodo a partir del cual se empiezan a mostrar las barras apiladas.
    """
    # Función para añadir valores en la parte superior de las barras
    def add_labels(bars, ax):
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Solo añadir etiquetas si el valor es mayor que 0
                ax.annotate('{}'.format(int(height)),
                            xy=(bar.get_x() + bar.get_width() / 2, bar.get_y() + height),
                            xytext=(0, 3),  # Desplazamiento vertical de 3 puntos
                            textcoords="offset points",
                            ha='center', va='bottom')
                
    # Inicializar los datos
    period_demand = {i: {t: 0 for t in range(start_period, len(T))} for i in LEVEL0}
    period_fulfilled = {i: {t: 0 for t in range(start_period, len(T))} for i in LEVEL0}

    # Calcular la demanda total y la demanda satisfecha para cada artículo en cada periodo
    for t in range(start_period, len(T)):
        for i in LEVEL0:
            for r in R:
                period_demand[i][t] += D[t][item_indices[i], customer_indices[r]]
                period_fulfilled[i][t] += D[t][item_indices[i], customer_indices[r]] * w[i, r, t]

    x = np.arange(len(LEVEL0))  # ubicaciones de las etiquetas
    width = 0.35  # ancho de las barras
    separation = 0.4 if add_second_bar else 0  # separación entre las barras

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    

    bottom = np.zeros(len(LEVEL0))

    # Crear barras apiladas por periodo de tiempo desde el periodo start_period
    for t in range(start_period, len(T)):
        total = [period_demand[i][t] for i in LEVEL0]
        bars = ax.bar(x, total, width, bottom=bottom, label=f'Periodo {t}')
        bottom += total

    # Añadir una segunda barra para subdividir la demanda satisfecha y no satisfecha
    if add_second_bar:
        for i in range(len(LEVEL0)):
            x_pos = x[i] + separation
            bottom = 0
            for t in range(start_period, len(T)):
                fulfilled = period_fulfilled[LEVEL0[i]][t]
                unfulfilled = period_demand[LEVEL0[i]][t] - fulfilled

                bars1 = ax.bar(x_pos, fulfilled, width, bottom=bottom, color='blue', label='_nolegend_')
                bottom += fulfilled
                bars2 = ax.bar(x_pos, unfulfilled, width, bottom=bottom, color='red', label='_nolegend_')
                bottom += unfulfilled

                # Añadir valores en la parte superior de las barras subdivididas
                # add_labels(bars1, ax)
                # add_labels(bars2, ax)

    # Ajustar los límites del eje y para asegurar que todas las barras sean visibles
    max_height = max(sum(period_demand[i][t] for t in range(start_period, len(T))) for i in LEVEL0)
    ax.set_ylim(0, max_height * 1.1)

    # Añadir etiquetas y título
    ax.set_xlabel('Ítems a nivel 0', fontsize = 16)
    ax.set_ylabel('Unidades', fontsize = 16)
    # ax.set_title('Demanda por Ítem y Periodo de Tiempo')
    ax.set_xticks(x + (separation if add_second_bar else 0) / 2)
    ax.set_xticklabels([f'{i}' for i in LEVEL0])
    ax.legend()
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    


    plt.show()
    

def plot_balance_over_time(D, B, w, c1, c2, x, y, item_indices, customer_indices, LEVEL0, R, K1, K2, K3, T):
    """
    Calcula y grafica el balance, los ingresos (beneficios), los costos y los beneficios máximos posibles para cada periodo de tiempo.

    Args:
        D (list of numpy arrays): Matrices de demanda.
        B (list of numpy arrays): Matrices de cantidad.
        w (dict): Diccionario de pesos.
        c1 (dict): Costos para x.
        c2 (dict): Costos para y.
        x (dict): Diccionario de valores x.
        y (dict): Diccionario de valores y.
        item_indices (dict): Índices de los ítems.
        customer_indices (dict): Índices de los clientes.
        LEVEL0 (list): Lista de ítems en el nivel 0.
        R (list): Lista de clientes.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
        T (list): Lista de periodos de tiempo.
    """

    # Inicializar listas para guardar los balances, ingresos, costos y beneficios máximos
    balances = []
    revenues = []
    costs = []
    max_revenues = []
    
    # Inicializar las listas para el primer periodo
    revenue = np.sum([D[1][item_indices[i], customer_indices[r]] * B[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R for i in LEVEL0])/1e6
    cost_x = np.sum([float(c1[i]) * x[i, 1] for i in K1 + K3])/1e6
    cost_y = np.sum([float(c2[i]) * y[i, 1] for i in K2 + K3])/1e6
    cost = cost_x + cost_y
    balance = revenue - cost
    max_revenue = np.sum([D[1][item_indices[i], customer_indices[r]] * B[1][item_indices[i], customer_indices[r]] for r in R for i in LEVEL0])
        
    balances.append(balance)
    revenues.append(revenue)
    costs.append(cost)
    max_revenues.append(max_revenue)


    # Calcular el balance, los ingresos, los costos y los beneficios máximos para cada periodo
    for t in range(2, len(T)):
        revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R for i in LEVEL0])/1e6
        cost_x = np.sum([float(c1[i]) * x[i, t] for i in K1 + K3])/1e6
        cost_y = np.sum([float(c2[i]) * y[i, t] for i in K2 + K3])/1e6
        cost = cost_x + cost_y
        balance = revenue - cost
        max_revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] for r in R for i in LEVEL0])
        
        balances.append(balance+balances[t-2])
        revenues.append(revenue+revenues[t-2])
        costs.append(cost+costs[t-2])
        max_revenues.append(max_revenue+max_revenues[t-2])

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, len(T)), balances, marker='o', linestyle='-', color='b', label='Balance')
    ax.plot(range(1, len(T)), revenues, marker='x', linestyle='--', color='g', label='Ingresos')
    ax.plot(range(1, len(T)), costs, marker='s', linestyle='-.', color='r', label='Costes')
    # ax.plot(range(1, len(T)), max_revenues, marker='d', linestyle=':', color='m', label='Ingresos si se satisface toda la demanda')

    # Configurar la cuadrícula en el fondo
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(1, len(T)))

    # Crea una lista de ticks con el rango deseado y el paso que quieras
    yticks = np.arange(-1, 8, step=0.5)  # Aquí puedes ajustar el paso como desees
    # Aplica los nuevos ticks al eje y
    plt.yticks(yticks, fontsize = 12)
    # Añadir etiquetas y título
    plt.xlabel('Periodo de Tiempo', fontsize = 16)
    plt.ylabel('Valor monetario en millones de Euros', fontsize = 16)
    # plt.title('Evolución del Balance de Ingresos y Costes', fontsize = 18)
    plt.legend()

    # Mostrar el gráfico
    plt.show()

def plot_inventory_average(I, I0, T, NN):
    """
    Calcula y grafica el inventario promedio por ítem en cada periodo, dividido entre el ítem 62 y los demás.

    Args:
        I (dict): Diccionario que representa el inventario de cada ítem en cada periodo.
        I_0 (dict): Diccionario que representa el inventario inicial de cada ítem.
        T (list): Lista de periodos de tiempo.
        NN (list): Lista de ítems.
    """

    # Inicializar listas para los inventarios promedio
    inventory_62 = []
    inventory_avg_others = []

    # Calcular el inventario promedio por ítem para cada periodo
    for t in range(len(T)):
        if t == 0:
            val_62 = I0[62]  # Rodillos, por lo que su inventario es mucho mayor 
            avg_others = np.mean([I0[i] for i in NN if i != 62])
        else:
            val_62 = I[62, t] 
            avg_others = np.mean([I[i, t] for i in NN if i != 62])
        
        inventory_62.append(val_62)
        inventory_avg_others.append(avg_others)

    # Crear el gráfico de líneas con dos ejes Y
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax2 = ax1.twinx()
    ax1.plot(range(len(T)), inventory_avg_others, marker='x', linestyle='--', color='g', label='Inventario Promedio (Demás Items)')
    ax2.plot(range(len(T)), inventory_62, marker='o', linestyle='-', color='b', label='Inventario Item 62 (Rodillos)')

    # Configurar la cuadrícula en el fondo
    ax1.set_axisbelow(True)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(len(T)))
    
    # Añadir etiquetas y título
    ax1.set_xlabel('Periodo de Tiempo', fontsize = 16)
    ax1.set_ylabel('Inventario Promedio (Ítem 62 excluido)', color='g', fontsize = 16)
    ax2.set_ylabel('Inventario Ítem 62 (Rodillo)', color='b', fontsize = 16)
    plt.title('Evolución del Inventario Promedio', fontsize = 18)

    # Añadir leyendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    # Mostrar el gráfico
    plt.show()

def plot_cost_comparison(c1, c2, x, y, T, K1, K2, K3):
    """
    Grafica una comparación entre los costos de producción (c1 * x) y los costos de compra (c2 * y) para los ítems en cada periodo.

    Args:
        c1 (dict): Costos de producción.
        c2 (dict): Costos de compra.
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Inicializar listas para los costos totales por periodo
    production_costs = []
    purchase_costs = []

    # Calcular los costos para cada periodo
    for t in range(1, len(T)):
        total_production_cost = np.sum([c1[i] * x[i, t] for i in K1+K3])
        total_purchase_cost = np.sum([c2[i] * y[i, t] for i in K2+K3])
        production_costs.append(total_production_cost)
        purchase_costs.append(total_purchase_cost)

    # Crear el gráfico de líneas con ejes Y diferentes
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Mes', fontsize=16)
    ax1.set_ylabel('Costes de Fabricación (Euros)', fontsize=16, color='b')
    ax1.plot(range(1, len(T)), production_costs, marker='o', linestyle='-', color='b', label='Costes de Fabricación')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # Instancia un segundo eje que comparte el mismo eje x
    ax2.set_ylabel('Costes de Compra (Euros)', fontsize=16, color='g')
    ax2.plot(range(1, len(T)), purchase_costs, marker='x', linestyle='--', color='g', label='Costes de Compra')
    ax2.tick_params(axis='y', labelcolor='g')

    # fig.suptitle('Comparación de Costes de Fabricación y Compra por Periodo', fontsize=18)

    # Añadir las etiquetas del eje X para todos los periodos
    plt.xticks(range(1, len(T)))

    # Sincronizar las cuadrículas de los dos ejes y establecer la cuadrícula
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax2.set_axisbelow(True)
    
    # Añadir las leyendas para ambos ejes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

    # Mostrar el gráfico
    plt.show()
    
def plot_FabricaCompra_comparison(x, y, T, K1, K2, K3):
    """
    Grafica una comparación entre la producción y los costos la compra para los ítems en cada periodo.

    Args:
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Inicializar listas para los costos totales por periodo
    production_costs = []
    purchase_costs = []

    # Calcular los costos para cada periodo
    for t in range(1, len(T)):
        total_production_cost = np.sum([x[i, t] for i in K1+K3])
        total_purchase_cost = np.sum([y[i, t] for i in K2+K3])
        production_costs.append(total_production_cost)
        purchase_costs.append(total_purchase_cost)

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(range(1, len(T)), production_costs, marker='o', linestyle='-', color='b', label='Unidades Producidas')
    ax.plot(range(1, len(T)), purchase_costs, marker='x', linestyle='--', color='g', label='Unidades Compradas')

    # Configurar la cuadrícula en el fondo
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(1, len(T)))
    
    # Añadir etiquetas y título
    plt.xlabel('Periodo de Tiempo')
    plt.ylabel('Unidades')
    plt.title('Comparación de las unidades producidas y compradas')
    plt.legend()

    # Mostrar el gráfico
    plt.show()

def plot_pie_chart_costs(c1, c2, x, y, T, K1, K2, K3):
    """
    Crea un gráfico circular con los costes totales de compra y de producción.

    Args:
        c1 (dict): Costos de producción.
        c2 (dict): Costos de compra.
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Calcular el neto de producción y el neto de compra
    net_production = np.sum([c1[i] * x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    net_purchase = np.sum([c2[i] * y[i, t] for t in range(1, len(T)) for i in K2 + K3])

    # Datos para el gráfico de pastel
    labels = 'Total\nProducción', 'Total\nCompra'
    sizes = [net_production, net_purchase]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # Resalta el primer segmento
    
    def autopct_format(values):
        def my_format(pct):
            total = float(round(pct*sum(values),2)/100)
            return '{:.1f}%\n{:.2f} Euros'.format(pct, total)
        return my_format
    
    # Crear el gráfico de pastel
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=autopct_format(sizes),
           shadow=True, startangle=90, textprops={'fontsize': 18})
    ax.axis('equal')  # Igualar el eje para asegurar que el gráfico de pastel es circular

    # Añadir título
    plt.title('Distribución de costes de Producción y Compra', fontsize = 20)

    # Mostrar el gráfico
    plt.show()

def plot_pie_chart_invent(x, y, T, K1, K2, K3):
    """
    Crea un gráfico circular con el neto de compra y neto de producción.

    Args:
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems para fabricacion.
        K2 (list): Lista de ítems para compra.
        K3 (list): Lista de ítems para ambos.
    """

    # Calcular el neto de producción y el neto de compra
    net_production = np.sum([x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    net_purchase = np.sum([y[i, t] for t in range(1, len(T)) for i in K2 + K3])

    # Datos para el gráfico de pastel
    labels = 'Unidades\nFabricadas', 'Unidades\nCompradas'
    sizes = [net_production, net_purchase]
    colors = ['#ff9999', '#66b3ff']
    explode = (0, 0)  # Resalta el primer segmento

    # Función para mostrar tanto el porcentaje como el valor neto
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{:.1f}%\n{:d} Unidades'.format(pct, val)
        return my_format

    # Crear el gráfico de pastel
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=autopct_format(sizes),
           shadow=True, startangle=180, textprops={'fontsize': 18})
    ax.axis('equal') # Igualar el eje para asegurar que el gráfico de pastel es circular

    # Añadir título
    plt.title('Distribución de las unidades Fabricadas y Compradas', fontsize = 20)

    # Mostrar el gráfico
    plt.show()
    
    
def plot_route_production_comparison(routeProduction, x_values_list, T, K1, K3):
    """
    Genera un gráfico de barras para comparar el valor neto de x por ruta para cada configuración,
    considerando solo los ítems en K1 y K3.

    Args:
        routeProduction (dict): Diccionario donde las claves son MyBOMITEMID y los valores son LINEROUTEID.
        x_values_list (list of dict): Lista de diccionarios donde las claves son MyBOMITEMID y los valores son los valores netos de x.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems en K1.
        K3 (list): Lista de ítems en K3.
    """
    # Unir K1 y K3
    K1_K3 = set(K1 + K3)

    # Inicializar un diccionario para almacenar los valores de x por ruta y por configuración
    route_config_values = {route: [0] * len(x_values_list) for route in set(routeProduction.values())}

    # Sumar los valores de x en todas las configuraciones
    for config_idx, x_values in enumerate(x_values_list):
        for item, route in routeProduction.items():
            route_config_values[route][config_idx] += np.sum([x_values[item,t] for t in range(1, len(T))])

    # Crear listas para el gráfico de barras
    routes = sorted(list(route_config_values.keys()))
    n_configs = len(x_values_list)
    width = 0.5 / n_configs  # Ancho de las barras

    # Configurar el tamaño de la figura
    plt.figure(figsize=(12, 8))

    # Obtener una paleta de colores
    cmap = plt.get_cmap('tab20')

    labels_PLANINV = ['0', 'HC=0, Q=1', 'HC=0, Q=0.75', 'HC=0, Q=0.5', 'HC=1, Q=1', 'HC=1, Q=0.75', 'HC=1, Q=0.5']
    labels_PLANMOQVAR = ['I0=F0,rF=1,rC=1', 'I0=F0,rF=0.75,rC=1', 'I0=F0,rF=0.5,rC=1', 'I0=F0,rF=0.33,rC=1', 'I0=F0,rF=0,rC=1',
                         'I0=F1,rF=1,rC=1', 'I0=F1,rF=0.75,rC=1', 'I0=F1,rF=0.5,rC=1', 'I0=F1,rF=0.33,rC=1', 'I0=F1,rF=0,rC=1',
                         ]
    # Crear el gráfico de barras
    for config_idx in range(n_configs):
        config_values = [route_config_values[route][config_idx] for route in routes]
        plt.bar(np.arange(len(routes)) + config_idx * width, config_values, width=width, color=cmap(config_idx % cmap.N), align='center'
                # , label=f'Escenario {config_idx}'
                # , label = labels_PLANINV[config_idx]
                , label = labels_PLANMOQVAR[config_idx]
                )

    # Etiquetas y título del gráfico
    plt.xlabel('Línea de producción', fontsize = 16)
    plt.ylabel('Unidades totales fabricadas', fontsize = 16)
    # plt.title('Comparación de la cantidad total de unidades fabricadas por linea de producción')
    # plt.title('Cantidad total de unidades fabricadas por linea de producción', fontsize = 18)
    plt.xticks(np.arange(len(routes)) + width * (n_configs - 1) / 2, routes)
    plt.legend(loc = 'upper left')

    # Mostrar el gráfico
    plt.show()

def plot_route_production_comparison_perT(routeProduction, x_values_list, T, K1, K3):
    """
    Genera un gráfico de barras para comparar el valor neto de x por ruta para cada configuración,
    considerando solo los ítems en K1 y K3.

    Args:
        routeProduction (dict): Diccionario donde las claves son MyBOMITEMID y los valores son LINEROUTEID.
        x_values_list (list of dict): Lista de diccionarios donde las claves son MyBOMITEMID y los valores son los valores netos de x.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems en K1.
        K3 (list): Lista de ítems en K3.
    """
    # Unir K1 y K3
    K1_K3 = set(K1 + K3)

    # Inicializar un diccionario para almacenar los valores de x por ruta y por configuración y por tiempo
    route_config_values = {route: np.zeros((len(x_values_list), len(T)-1)) for route in set(routeProduction.values())}

    # Sumar los valores de x en todas las configuraciones y periodos de tiempo
    for config_idx, x_values in enumerate(x_values_list):
        for item, route in routeProduction.items():
            if item in K1_K3:
                for t in range(1, len(T)):
                    route_config_values[route][config_idx, t-1] += x_values[item, t]

    # Crear listas para el gráfico de barras
    routes = sorted(list(route_config_values.keys()))
    n_configs = len(x_values_list)
    n_periods = len(T) - 1
    width = 0.05  # Ancho de las barras para cada configuración

    # Configurar el tamaño de la figura
    plt.figure(figsize=(12, 8))

    # Obtener una paleta de colores
    cmap = plt.get_cmap('tab20')

    # Crear el gráfico de barras apiladas por periodo de tiempo
    for config_idx in range(n_configs):
        bottom = np.zeros(len(routes))
        for t in range(n_periods):
            config_values = [route_config_values[route][config_idx, t] for route in routes]
            bars = plt.bar(np.arange(len(routes)) + config_idx * (width + 0.02), config_values, width=width, color=cmap(t % cmap.N), bottom=bottom, align='center')
            bottom += config_values
        # Etiquetas de configuración arriba de cada barra
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, bottom[i], f'{config_idx}', ha='center', va='bottom')

    # Cambiar el estilo de la rejilla
    # plt.grid(True, linestyle='--')

    # Etiquetas y título del gráfico
    plt.xlabel('Línea de producción', fontsize=16)
    plt.ylabel('Cantidad Total de Producción', fontsize=16)
    plt.title('Comparación de la cantidad total de unidades fabricadas por línea de producción', fontsize=18)
    
    # Asegurar que las xticks estén en el centro del grupo de barras
    plt.xticks(np.arange(len(routes)) + width * (n_configs - 1), routes)

    # Aumentar el número de marcas en el eje y
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(nbins=20))

    # Crear leyenda para los periodos de tiempo
    handles = [plt.Rectangle((0,0),1,1, color=cmap(t % cmap.N)) for t in range(n_periods)]
    labels = [f'Periodo {t+1}' for t in range(n_periods)]
    plt.legend(handles, labels, title="Periodos de Tiempo", loc='upper left')

    # Mostrar el gráfico
    plt.show()
def plot_I_compromised(c_std, I, I_0, T, K1, K2, K3):
    """
    Grafica el inventario comprometido en cada periodo.

    Args:
        c_std (dict): Costos estándar.
        I_0 (dict): Inventario inicial.
        I (dict): Inventario a lo largo de los diferentes periodos de tiempo.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Inicializar listas para los costos totales por periodo
    Icompromised = []
    Icompromised.append(np.sum([c_std[i] * I_0[i]/1e6 for i in K1+K2+K3]))
    # Calcular los costos para cada periodo
    for t in range(1, len(T)):
        total_production_cost = np.sum([c_std[i] * I[i, t]/1e6 for i in K1+K2+K3])
        Icompromised.append(total_production_cost)

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(range(len(T)), Icompromised, marker='o', linestyle='--', color='green', label='Capital comprometido')

    # Configurar la cuadrícula en el fondo
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(1, len(T)))
    
    # Añadir etiquetas y título
    plt.xlabel('Periodo de Tiempo', fontsize = 16)
    plt.ylabel('Valor en millones de Euros', fontsize = 16)
    # plt.title('Capital comprometido por Periodo', fontsize = 18)
    plt.legend()

    # Mostrar el gráfico
    plt.show()
    
def plot_I_compromised_MultipleEnv(c_std, I_list, T, K1, K2, K3):
    """
    Grafica el inventario comprometido en cada periodo para cada escenario en I_list.

    Args:
        c_std (dict): Costos estándar.
        I_list (list of dicts): Lista donde cada elemento es un diccionario de inventarios para diferentes escenarios.
        T (list): Lista de periodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Inicializar listas para los costos totales por periodo para cada escenario
    Icompromised_list = []

    # Iterar sobre cada escenario de inventario en I_list
    for I in I_list:
        Icompromised = []
        # Calcular los costos para cada periodo
        for t in range(len(T)):
            total_production_cost = np.sum([c_std[i] * I[i, t]/1e6 for i in K1 + K2 + K3])
            Icompromised.append(total_production_cost)

        # Agregar la lista de costos comprometidos para este escenario a la lista principal
        Icompromised_list.append(Icompromised)

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 6))

    colors_PLANINV = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.545),  (0.0, 0.0, 1.0), (0.678, 0.847, 0.902), (0.545, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.5, 0.5)]
    labels_PLANINV = ['0', 'HC=0, Q=1', 'HC=0, Q=0.75', 'HC=0, Q=0.5', 'HC=1, Q=1', 'HC=1, Q=0.75', 'HC=1, Q=0.5']
    # Plotear los datos para cada escenario
    for idx, Icomp in enumerate(Icompromised_list):
        ax.plot(range(len(T)), Icomp, marker='o', linestyle='--'
                , label = labels_PLANINV[idx]
                , color = colors_PLANINV[idx]
                # , label=f'Escenario {idx+1}'
                )

    # Configurar la cuadrícula en el fondo
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(len(T)))

    # Añadir etiquetas y título
    plt.xlabel('Periodo de Tiempo', fontsize=16)
    plt.ylabel('Valor en millones de Euros', fontsize=16)
    # plt.title('Inventario comprometido por Periodo', fontsize=18)
    plt.legend()

    # Mostrar el gráfico
    plt.show()

def plot_Opt_c2Mult(c2_mult, Optimo, Xtotal):
    """Genera un gráfico del optimo de la funcion objetivo y la cantidad total de fabrica frente al multiplicador de c2.

    Args:
        c2_mult (list): Lista de multiplicadores de c2.
        Óptimo (list): Lista de valores óptimos de la función objetivo (izquierdo).
        Xtotal (list): Lista de cantidades totales de fabrica (derecho).

    Raises:
        ValueError: Si las listas c2_mult, Optimo y Xtotal no tienen la misma longitud.
    """
    # Verificar que todas las listas tengan el mismo tamaño
    if len(c2_mult) != len(Optimo) or len(c2_mult) != len(Xtotal):
        raise ValueError("Las listas c2_mult, Optimo y Xtotal deben tener la misma longitud")

    # Crear la figura y el eje principal
    fig, ax1 = plt.subplots()

    OptimoMillones = [x / 1e6 for x in Optimo]
    
    # Graficar Optimo en el eje Y izquierdo
    ax1.set_xlabel('Factor de reducción', fontsize = 16)
    ax1.set_ylabel('Valor monetario en millones de euros', color='tab:blue', fontsize = 16)
    ax1.plot(c2_mult, OptimoMillones, linestyle='-',color='tab:blue', label='Valor Óptimo del Beneficio')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax1.set_xlim(ax1.get_xlim()[::-1])

    # Crear un segundo eje Y para graficar Xtotal
    ax2 = ax1.twinx()
    ax2.set_ylabel('Unidades totales fabricadas', color='tab:red', fontsize = 16)
    ax2.plot(c2_mult, Xtotal, linestyle='-', color='tab:red', label='Fabricación total')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='center left')
    
    ax1.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(nbins=13))
    ax2.yaxis.set_major_locator(plt.MaxNLocator(nbins=13))
    ax1.tick_params(axis='both', which='major', labelsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=10)

    # Mostrar el gráfico resultante
    # plt.title('Evolución del óptimo de la función objetivo y la producción total', fontsize = 18)
    plt.show()

def generar_graficos_sectores_por_mes(df):
    """
    Genera una matriz de gráficos de sectores para cada mes en el DataFrame dado.
    
    Cada gráfico muestra la distribución del número de unidades solicitadas 
    para cada MyBOMITEMID en un mes específico.

    Args:
    df (pd.DataFrame): DataFrame con las columnas MyBOMITEMID, ITEMID, ORDERTYPE, 
                       QUANTITY, CUSTOMERID, UNITPRICE_EUR y END_DATE.
    """
    # Agregar una columna para el mes
    df['MONTH'] = df['END_DATE'].dt.month + 6

    # Agrupar por mes y MyBOMITEMID y sumar las cantidades
    grouped = df.groupby(['MONTH', 'MyBOMITEMID'])['QUANTITY'].sum().reset_index()

    # Calcular el total de unidades solicitadas por cada MyBOMITEMID
    total_quantity = grouped.groupby('MyBOMITEMID')['QUANTITY'].sum().reset_index()

    # Ordenar los items por el total de unidades solicitadas en orden descendente
    total_quantity = total_quantity.sort_values(by='QUANTITY', ascending=False)

    # Lista de meses de interés
    months = [7, 8, 9, 10, 11, 12]

    # Obtener lista de items únicos en el orden de total_quantity
    unique_items = total_quantity['MyBOMITEMID'].tolist()

    # Generar colores únicos para cada item usando 'tab20b' y 'tab20c'
    num_items = len(unique_items)
    half_num_items = (num_items + 1) // 2
    colors_1 = plt.get_cmap('tab20b', half_num_items)
    colors_2 = plt.get_cmap('tab20c', num_items - half_num_items)

    # Combinar los colores en un solo diccionario
    color_map = {item: colors_1(i) if i < half_num_items else colors_2(i - half_num_items) 
                 for i, item in enumerate(unique_items)}

    # Crear subplots 3x2
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))

    # Crear un gráfico de sectores para cada mes
    wedges_list = []
    for i, month in enumerate(months):
        ax = axs[i // 2, i % 2]  # Determinar la posición del subplot
        data_month = grouped[grouped['MONTH'] == month]
        wedges, texts = ax.pie(
            data_month['QUANTITY'], 
            labels=None, 
            colors=[color_map[item] for item in data_month['MyBOMITEMID']]
        )
        wedges_list.extend(wedges)  # Añadir wedges a la lista para la leyenda
        ax.set_title(f'Mes {month}')

    # Crear una leyenda conjunta ordenada por el total de unidades solicitadas
    fig.legend([plt.Line2D([0], [0], color=color_map[item], lw=4) for item in unique_items], 
               unique_items, fontsize = 15,loc='center right')

    # Ajustar el layout para que los gráficos no se superpongan
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Ajustar para hacer espacio para la leyenda

    # Mostrar los gráficos
    plt.show()
    
def scatter_plot_costes(c1, c2, K1, K2, K3, x, y, T):
    """
    Crea un scatter plot donde cada punto representa un item.
    
    El eje X representa el coste total a lo largo del tiempo invertido en producir unidades de un item,
    y el eje Y representa el coste total a lo largo del tiempo invertido en comprar unidades de un item.
    
    Args:
    c1 (dict): Diccionario de costes para items en K1 y K3.
    c2 (dict): Diccionario de costes para items en K2 y K3.
    K1 (list): Lista de items que solo se producen.
    K2 (list): Lista de items que solo se compran.
    K3 (list): Lista de items que se producen y compran.
    x (dict): Diccionario de unidades producidas con clave (item, periodo).
    y (dict): Diccionario de unidades compradas con clave (item, periodo).
    T (list): Lista de periodos de tiempo.
    """
    
    # Calcular los costes totales para cada item en cada eje
    costes_produccion = {}
    costes_compra = {}
    
    # Calcular el coste de producción para items en K1 y K3
    for item in K1 + K3:
        coste_total_produccion = sum(c1[item] * x[item, t] for t in range(1, len(T)))
        costes_produccion[item] = coste_total_produccion
    
    # Calcular el coste de compra para items en K2 y K3
    for item in K2 + K3:
        coste_total_compra = sum(c2[item] * y[item, t] for t in range(1, len(T)))
        costes_compra[item] = coste_total_compra

    # Crear el scatter plot
    plt.figure(figsize=(10, 6))
    
    for item in K1:
        plt.scatter(costes_produccion[item], 0, color='blue', alpha=0.6)
        plt.text(costes_produccion[item], 0, item, fontsize=12, ha='right', color='blue')
    
    for item in K2:
        plt.scatter(0, costes_compra[item], color='green', alpha=0.6)
        plt.text(0, costes_compra[item], item, fontsize=12, ha='right', color='green')
    
    for item in K3:
        plt.scatter(costes_produccion[item], costes_compra[item], color='red', alpha=0.6)
        plt.text(costes_produccion[item], costes_compra[item], item, fontsize=12, ha='right', color='red')
    
    
    # Añadir etiquetas y leyenda
    plt.xlabel('Costes Totales de Fabricacion en Euros', fontsize = 16)
    plt.ylabel('Costes Totales de Compra en Euros', fontsize = 16)
    # plt.title('Costes de producción y compra')
    # plt.legend()
    plt.grid(True)
    plt.show()

def scatter_plot_costes_Ud(c1, c2, K1, K2, K3):
    """
    Crea un scatter plot donde cada punto representa un item.
    
    El eje X representa el coste por unidad en producir un item,
    y el eje Y representa el coste por unidad en comprar un item.
    
    Args:
    c1 (dict): Diccionario de costes para items en K1 y K3.
    c2 (dict): Diccionario de costes para items en K2 y K3.
    K1 (list): Lista de items que solo se producen.
    K2 (list): Lista de items que solo se compran.
    K3 (list): Lista de items que se producen y compran.
    """

    # Crear el scatter plot
    plt.figure(figsize=(10, 6))
    
    for item in K1:
        plt.scatter(c1[item], 0, color='blue', alpha=0.6)
        plt.text(c1[item], 0, item, fontsize=12, ha='right', color='blue')
    
    for item in K2:
        plt.scatter(0, c2[item], color='green', alpha=0.6)
        plt.text(0, c2[item], item, fontsize=12, ha='right', color='green')
    
    for item in K3:
        plt.scatter(c1[item], c2[item], color='red', alpha=0.6)
        plt.text(c1[item], c2[item], item, fontsize=12, ha='right', color='red')
    
    
    # Añadir etiquetas y leyenda
    plt.xlabel('Costes por unidad de Fabricacion en Euros/Ud', fontsize = 16)
    plt.ylabel('Costes por unidad de Compra en Euros/Ud', fontsize = 16)
    # plt.title('Costes de producción y compra')
    # plt.legend()
    plt.grid(True)
    plt.show()

def scatter_plot_costes_Routes(c1, routes, K1, K3):
    """
    Crea un scatter plot donde cada punto representa un item.
    
    El eje X representa la linea de produccion del item,
    y el eje Y representa el coste por unidad en fabricar un item.
    
    Args:
    c1 (dict): Diccionario de costes para items en K1 y K3.
    routes (dict): Diccionario de lineas de produccion para items en K1 y K3.
    K1 (list): Lista de items que solo se producen.
    K3 (list): Lista de items que se producen y compran.
    """

    # Crear el scatter plot
    plt.figure(figsize=(10, 6))
    
    for item in K1:
        plt.scatter(routes[item], c1[item], color='blue', alpha=0.6)
        plt.text(routes[item], c1[item], item, fontsize=12, ha='right', color='blue')
    
    for item in K3:
        plt.scatter(routes[item], c1[item], color='blue', alpha=0.6)
        plt.text(routes[item], c1[item], item, fontsize=12, ha='right', color='red')
    
    
    # Añadir etiquetas y leyenda
    plt.xlabel('Línea de Producción', fontsize = 16)
    plt.ylabel('Costes por unidad de Compra en Euros/Ud', fontsize = 16)
    # plt.title('Costes de producción y compra')
    # plt.legend()
    plt.grid(True)
    plt.show()
    
    
    
if __name__ == "__main__":
    results, I_results, X_results, Y_results, W_results = load_results()
    BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, StdCost, Tenv = chargeEnv(mode = "default")
    NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, c_std, c_invent, Q_invent, Q_fabrica, MOQ1, MOQ2, lt, ltf, I_0, alpha = charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, StdCost, Tenv)
    routeProduction = {
    **{key: value for key, value in zip(RouteItems["MyBOMITEMID"], RouteItems["LINEROUTEID"])},
    **{key: value for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["LINEROUTEID"])}
    }    # Diccionario de rutas-item
    

    # plotNet([X_results[0]], K1+K3, T)
    # plotNet(Y_results,list(set(K2 + K3)), T)
    # plotNet(I_results, list(set(K1 + K3)), T)
    # plotNet_Costes(X_results, list(set(K1 + K3)), T, c1)
    # plotNet_Costes(Y_results, list(set(K2 + K3)), T, c2)
    plotNetI_comprometido(I_results[0:6]+I_results[10:], K1 + K2 + K3, T, c_std)
    # plotItem(Y_results, T, 62, "Unidades compradas por periodo del ítem 62")
    # plot_inventory(I_0, 0, T)
    # plot_inventory(I_results[0], 12, T)
    # plot_inventory_vs_cost(I_results[0], 12, T, c_std)
    # plot_demand_satisfaction(D, W_results[0], T, LEVEL0, R, item_indices, customer_indices)
    # plot_demand_by_period(D, W_results[0], T, LEVEL0, R, item_indices, customer_indices, add_second_bar=False, start_period=7)
    # plot_balance_over_time(D, B, W_results[0], c1, c2, X_results[0], Y_results[0], item_indices, customer_indices, LEVEL0, R, K1, K2, K3, T)
    # plot_inventory_average(I_results[0], I_0, T, NN)
    # plot_cost_comparison(c1, c2, X_results[0], Y_results[0], T, K1, K2, K3)
    # plot_FabricaCompra_comparison(X_results[0], Y_results[0], T, K1, list(set(K2)-{62}), K3)
    # plot_pie_chart_costs(c1, c2, X_results[0], Y_results[0], T, [], [], K3)
    # plot_pie_chart_invent(X_results[5], Y_results[5], T, [], [], K3)
    # plot_pie_chart_invent(X_results[0], Y_results[0], T, K1, list(set(K2)-{62}), K3)
    # plot_route_production_comparison(routeProduction, X_results[0:6]+X_results[10:], T, K1, K3)
    # plot_route_production_comparison_perT(routeProduction, [X_results[0]] + X_results[5:], T, K1, K3)
    # plot_I_compromised(c_std, I_results[0], I_0, T, K1, K2, K3)
    # plot_I_compromised_MultipleEnv(c_std, I_results, T, K1, K2, K3)
    plot_Opt_c2Mult(results['c2_multiplier'], results['ObjVal'], results['uds_fabricadas'])
    # generar_graficos_sectores_por_mes(Orders)
    # scatter_plot_costes(c1, c2, K1, K2, K3, X_results[0], Y_results[0], T)
    # scatter_plot_costes_Ud(c1, c2, K1, K2, K3)
    # scatter_plot_costes_Routes(c1, routeProduction, K1, K3)