import pandas as pd # se importa el modulo pandas para manejo de dataframes.
import glob         # Importa libreria para manejo de archivos con cierto pathname definido
import lasio        # Permite ejecutar unas conversión sobre archivos con extensión .las

archivos_las = glob.glob('*.las') # Genero una lista con todos los .las de la carpeta

for m in range(0, len(archivos_las)): # loop que permite recorrer todos los archivos, leerlos y generar un .xlsx.
    lectura = lasio.read(archivos_las[m])
    lectura.to_excel(str(archivos_las[m][:-4] + '.xlsx')) # quita la extensión .las y agrega la extensión .xlsx. dejar solo el nombre del pozo.

archivos_excel = glob.glob('*.xlsx')

for n in range(0, len(archivos_excel)):
    df = pd.read_excel(archivos_excel[n], sheet_name='Curves')

x = 0 # se establece el valor cero de inicio a la variable x.
PASO = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] # se sefine la lista PASO
DEPT = [1100.5,1101,1101.5,1102,1102.5,1103,1103.5,1104,1104.5,1105,1105.5,1106,1106.5,1107,1107.5,1108,1108.5,1109] # se sefine la lista DEPTH
CBL = [5,6,25,10,4,3,19,1,11,17,19,19,30,10,5,7,9,10] # se define la lista CBL.

mV = 20 # se define el valor de amplitud para el cual el cual se considera el tope de cemento.

df = pd.DataFrame({'depth' : DEPT, 'paso' : PASO, 'cbl' : CBL}) # lleva las listas a un dataframe

for i in range(len(CBL)): # empiezo un loop de cero a la longitud de la lista CBL.
    if x < 3 and CBL[i] <= mV: # genero dos condiciones x < 3 (este valor puede cambiar), y el CBL menor o igual al definido (este valor también puede cambiar).
        x = x + PASO[i] # sumo un paso al valor de la variable x cada que ve que se cumple la condición anterior.
        y = i # la variable y adopta el valor más actual de i.
        # print(y, x), para verificar cómo avanza el loop y comprobar errores.
    elif x < 3 and CBL[i] > mV: # genero otras dos condiciones por si no se cumplen las anteriores. En este caso si el CBL es mayor al estabelcido, x vuelve a cero.
        x = 0 # si el valor del CBL es mayor al establecido como bueno, la cuenta vuelve a cero.
        # y = i, para verificar cómo avanza el loop y comprobar errores.
        # print(y, x), para verificar cómo avanza el loop y comprobar errores.
    else:
        break # si no se cumplen ninguna de las condiciones anteriores, el loop rompe.

# Una vez que el loop rompe, tengo el valor de y = i de la iteración en la cual se cumplen x (en este caso 3) metros.
# Por lo tanto x será 3 o más, i será el nñumero de iteración que cumple con x = 3 o más.

z = y - int(x / PASO[i] - 1) # z es el valor donde la función comienza a cumplirse.
toc = DEPT[z] # toc es el tope de cemento definido.

df_new = df[DEPT.index(toc):] # genero un dataframe en el que se eliminan los valores superiores al tope de cemento.
df_new # visualizo el dataframe generado.

key = ['mean', 'max', 'min', 'q5', 'q10', 'q15', 'q20', 'q25', 'q30', 'q35', 'q40', 'q45', 'q50', 'q55', 'q60', 'q65', 'q70', 'q75', 'q80', 'q85', 'q90', 'q95'] # lista con cuantiles generados
values = [] # se genera una lista vacia que se ira llenando a medida que el loop avance
values.append(df_new['cbl'].mean()) # agrega la media a la lista values.
values.append(df_new['cbl'].max()) # agrega el valor máximo a la lista values.
values.append(df_new['cbl'].min()) # agrega el valor mínimo a la lista values.

for q in range(5,100,5): # loop desde 5 a 100 con paso 5 para los distintos cuantiles.
    values.append(df_new['cbl'].quantile(q/100)) # función que agrega el valor calculado del cuantil a la lista values.
    
df_final = pd.DataFrame(values, index =key) # se genera un dataframe con los valores de la lista values y los indices de la lista key.
df_final # se muestra el dataframe.

# Se debe hacer un merge con el archivo pruebalog.py

# Falta incorporar la lectura de todos los archivos al principio de este source code.
# Falta incorporar el algunos cálculos al final del source code.