import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import datetime as dt
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
    x_labels = [date.strftime('%d-%m-%y') for date in T[1:]]  
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
    x_labels = [date.strftime('%d-%m-%y') for date in T[1:]] 
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
        ax.axvline(pos + width * (num_configs - 1) / 2 + (x[1]-x[0])/2 , color='grey', linestyle='--')

    # Show the plot
    plt.show()
    
def plot_inventory(I, time_period, T):
    """
    Genera un gráfico de barras que muestra el inventario para cada ítem en un período de tiempo dado.

    Args:
        I (dict): Diccionario con inventarios, donde la clave es una tupla (i, t) que representa el ítem y el período de tiempo.
        time_period (int): El periodo de tiempo para el cual se desea visualizar el inventario.
        T (list): Lista de periodos de tiempo.

    Returns:
        None: Muestra un gráfico de barras donde el eje X representa los ítems y el eje Y representa el inventario para el período de tiempo dado.
    """
    if time_period!= 0:
        # Filtra el inventario para el período de tiempo dado
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
    ax1.set_title(f"Inventario por ítem en el período de tiempo {T[time_period].strftime('%d-%m-%y')}")

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
    ax.set_xlabel('Ítems a nivel 0')
    ax.set_ylabel('Unidades')
    ax.set_title('Demanda por Ítem y Periodo de Tiempo')
    ax.set_xticks(x + (separation if add_second_bar else 0) / 2)
    ax.set_xticklabels([f'{i}' for i in LEVEL0])
    ax.legend()
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    


    plt.show()
    

def plot_balance_over_time(D, B, w, c1, c2, x, y, item_indices, customer_indices, LEVEL0, R, K1, K2, K3, T):
    """
    Calcula y grafica el balance, los ingresos (beneficios), los costos y los beneficios máximos posibles para cada período de tiempo.

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
        T (list): Lista de períodos de tiempo.
    """

    # Inicializar listas para guardar los balances, ingresos, costos y beneficios máximos
    balances = []
    revenues = []
    costs = []
    max_revenues = []

    # Calcular el balance, los ingresos, los costos y los beneficios máximos para cada período
    for t in range(1, len(T)):
        revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R for i in LEVEL0])
        cost_x = np.sum([float(c1[i]) * x[i, t] for i in K1 + K3])
        cost_y = np.sum([float(c2[i]) * y[i, t] for i in K2 + K3])
        cost = cost_x + cost_y
        balance = revenue - cost
        max_revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] for r in R for i in LEVEL0])
        
        balances.append(balance)
        revenues.append(revenue)
        costs.append(cost)
        max_revenues.append(max_revenue)

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, len(T)), balances, marker='o', linestyle='-', color='b', label='Balance')
    ax.plot(range(1, len(T)), revenues, marker='x', linestyle='--', color='g', label='Ingresos')
    ax.plot(range(1, len(T)), costs, marker='s', linestyle='-.', color='r', label='Costos')
    ax.plot(range(1, len(T)), max_revenues, marker='d', linestyle=':', color='m', label='Ingresos si se satisface toda la demanda')

    # Configurar la cuadrícula en el fondo
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(1, len(T)))

    # Añadir etiquetas y título
    plt.xlabel('Periodo de Tiempo')
    plt.ylabel('Valor')
    plt.title('Balance, Ingresos, Costos y Ingresos Máximos para Cada Periodo de Tiempo')
    plt.legend()

    # Mostrar el gráfico
    plt.show()

def plot_inventory_average(I, I0, T, NN):
    """
    Calcula y grafica el inventario promedio por ítem en cada período, dividido entre el ítem 62 y los demás.

    Args:
        I (dict): Diccionario que representa el inventario de cada ítem en cada período.
        I_0 (dict): Diccionario que representa el inventario inicial de cada ítem.
        T (list): Lista de períodos de tiempo.
        NN (list): Lista de ítems.
    """

    # Inicializar listas para los inventarios promedio
    inventory_62 = []
    inventory_avg_others = []

    # Calcular el inventario promedio por ítem para cada período
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
    ax1.set_xlabel('Periodo de Tiempo')
    ax1.set_ylabel('Inventario Promedio (Demás Items)', color='g')
    ax2.set_ylabel('Inventario Item 62 (Rodillos)', color='b')
    plt.title('Inventario Promedio por Ítem en Cada Periodo')

    # Añadir leyendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    # Mostrar el gráfico
    plt.show()

def plot_cost_comparison(c1, c2, x, y, T, K1, K2, K3):
    """
    Grafica una comparación entre los costos de producción (c1 * x) y los costos de compra (c2 * y) para los ítems en cada período.

    Args:
        c1 (dict): Costos de producción.
        c2 (dict): Costos de compra.
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de períodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Inicializar listas para los costos totales por período
    production_costs = []
    purchase_costs = []

    # Calcular los costos para cada período
    for t in range(1, len(T)):
        total_production_cost = np.sum([c1[i] * x[i, t] for i in K1+K3])
        total_purchase_cost = np.sum([c2[i] * y[i, t] for i in K2+K3])
        production_costs.append(total_production_cost)
        purchase_costs.append(total_purchase_cost)

    # Crear el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(range(1, len(T)), production_costs, marker='o', linestyle='-', color='b', label='Costos de Producción')
    ax.plot(range(1, len(T)), purchase_costs, marker='x', linestyle='--', color='g', label='Costos de Compra')

    # Configurar la cuadrícula en el fondo
    ax.set_axisbelow(True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Añadir todas las etiquetas del eje X
    plt.xticks(range(1, len(T)))
    
    # Añadir etiquetas y título
    plt.xlabel('Periodo de Tiempo')
    plt.ylabel('Costos Totales')
    plt.title('Comparación de Costos de Producción y Compra por Período')
    plt.legend()

    # Mostrar el gráfico
    plt.show()
    
def plot_FabricaCompra_comparison(x, y, T, K1, K2, K3):
    """
    Grafica una comparación entre la producción y los costos la compra para los ítems en cada período.

    Args:
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de períodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Inicializar listas para los costos totales por período
    production_costs = []
    purchase_costs = []

    # Calcular los costos para cada período
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

def plot_pie_chart(c1, c2, x, y, T, K1, K2, K3):
    """
    Crea un gráfico circular con el neto de compra y neto de producción.

    Args:
        c1 (dict): Costos de producción.
        c2 (dict): Costos de compra.
        x (dict): Valores de producción.
        y (dict): Valores de compra.
        T (list): Lista de períodos de tiempo.
        K1 (list): Lista de ítems para c1.
        K2 (list): Lista de ítems para c2.
        K3 (list): Lista de ítems para ambos c1 y c2.
    """

    # Calcular el neto de producción y el neto de compra
    net_production = np.sum([c1[i] * x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    net_purchase = np.sum([c2[i] * y[i, t] for t in range(1, len(T)) for i in K2 + K3])

    # Datos para el gráfico de pastel
    labels = 'Neto de Producción', 'Neto de Compra'
    sizes = [net_production, net_purchase]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # Resalta el primer segmento

    # Crear el gráfico de pastel
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')  # Igualar el eje para asegurar que el gráfico de pastel es circular

    # Añadir título
    plt.title('Distribución de costes de Producción y Compra')

    # Mostrar el gráfico
    plt.show()


if __name__ == "__main__":
    results, I_results, X_results, Y_results, W_results = load_results()
    BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv = chargeEnv(mode = results["Environment"].values[0])
    NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, c_invent, Q_invent, Q_fabrica, MOQ1, MOQ2, lt, ltf, I_0, alpha = charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv)
        
    

    # plotNet(X_results, K1+K3, T)
    # plotNet(Y_results,list(set(K2 + K3) - {62}), T)
    # plotNet(I_results, list(set(K1 + K2 + K3) - {62}), T)
    # plotItem(I_results, T, 62)
    plotItem(Y_results, T, 62)
    # plot_inventory(I_0, 0, T)
    # plot_inventory(I_results[0], 12, T)
    # plot_demand_satisfaction(D, W_results[0], T, LEVEL0, R, item_indices, customer_indices)
    # plot_demand_by_period(D, W_results[0], T, LEVEL0, R, item_indices, customer_indices, add_second_bar=True, start_period=7)
    # plot_balance_over_time(D, B, W_results[0], c1, c2, X_results[0], Y_results[0], item_indices, customer_indices, LEVEL0, R, K1, K2, K3, T)
    # plot_inventory_average(I_results[0], I_0, T, NN)
    plot_cost_comparison(c1, c2, X_results[0], Y_results[0], T, K1, K2, K3)
    plot_FabricaCompra_comparison(X_results[0], Y_results[0], T, K1, K2, K3)
    plot_pie_chart(c1, c2, X_results[0], Y_results[0], T, K1, K2, K3)