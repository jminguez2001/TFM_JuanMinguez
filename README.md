# Código del TFM de Juan Mínguez Laguna 
En este repositorio se encuentra el código empleado para la realización del TFM. 

A continuación se muestra un resumen del contenido del repositorio:

## Directorio principal
- El archivo **MultipleEnvironmentsRun.py** que ejecuta el modelo matemático con los datos del sistema en diferentes configuraciones a elegir.
- El archivo **KeepDataFrames.py** para tomar las tablas finales desde la base de datos y guardarlas como dataframes en archivos .pkl.
- El archivo **AnalyzeBOMs.py** permite leer las BOMs, estudiar su conectividad y dibujar los grafos asociados.

## Carpetas Auxiliares
* **BOM_graph**: contiene los archivos .py con las funciones para el estudio y dibujo como grafo de las BOM.
* **DB_conexion**: contiene el archivo .py con la definicion de clase para los objetos utilizados para conectarse a la base de datos,
                  asi como las funciones para operar sobre la misma.
* **DB_Operations**: contiene las funciones para la generación de pedidos.
* **Environments**: contiene los archivos .py con las funciones relacionadas con la ejecución del modelo para los datos del sistema y la configuración elegida.
                    Además contiene el archivo DrawData.py que es el archivo empleado para la generación de las gráficas del TFM.
* **helpers**: contiene archivos .py con funciones genericas que se utilizan en diferentes archivos del proyecto, como la función para crear logs o particiones aleatorias.
* **ScriptsSQL**: contiene los archivos .SQL que se ejecutan sobre la base de datos de la empresa para el manejo de las tablas directamente en la base de datos.
* **SQL_python**: contiente archivos .py con las definiciones de cadenas de caractéres que representan sentencias de SQL que se ejecutan sobre la base de datos desde un archivo .py.
                  Estas sentencias son usadas principalmente en la lectura de las tablas de la base de datos para guardarlas como un data fram en un archivo .pkl posteriormente.
