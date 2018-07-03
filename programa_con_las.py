import pandas as pd # se importa el modulo pandas para manejo de dataframes.
import glob         # Importa libreria para manejo de archivos con cierto pathname definido
import lasio        # Permite ejecutar unas conversión sobre archivos con extensión .las

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

archivos_las = glob.glob('*.las') # genera una lista con todos los .las de la carpeta

for m in range(0, len(archivos_las)): # loop que permite recorrer todos los archivos, leerlos y generar un .xlsx.
    lectura = lasio.read(archivos_las[m])
    lectura.to_excel(str(archivos_las[m][:-4] + '.xlsx')) # quita la extensión .las y agrega la extensión .xlsx. dejar solo el nombre del pozo.

archivos_excel = glob.glob('*.xlsx') # genera una lista con todos los .xlsx de la carpeta

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

for n in range(0, len(archivos_excel)): # loop que permite recorrer todos los archivos
    df = pd.read_excel(archivos_excel[n], 'Curves') # genera un dataframe
    x = 0 # se establece el valor cero de inicio a la variable x.
    mV = 20 # se define el valor de amplitud para el cual se considera el tope de cemento.
    
    paso = [] # se define la lista paso vacía (Sería más reocmendable generar una Serie de pandas)

    for o in range(0, len(df.DEPT)-1): # se hace un loop sobre la lista para generar la columna paso.
        paso.append(df.DEPT[o+1] - df.DEPT[o])

    paso.append(paso[len(paso)-1]) # se genera el último valor de la lista para que paso tenga la misma cantidad de items que las otras columnas

    s = pd.Series(paso)

    df2 = pd.concat([df,s], axis=1) # agrega la Serie: paso, al dataframe df y se reemplaza el nombre.

    # df2.DEPT es la lista DEPT del dataframe df, en realidad serie de pandas DEPT
    # df2.CBL (AMP3FT) es la lista CBL del dataframe df, en realidad serie de pandas CBL.

    for i in range(0, len(df2.AMP3FT)): # empiezo un loop de cero a la longitud de la lista CBL.
        if df2.AMP3FT[i] <= mV and x < 3: # genero dos condiciones x < 3 (este valor puede cambiar), y el CBL menor o igual al definido (este valor también puede cambiar).
            x = x + df2[0][i] # sumo un paso al valor de la variable x cada que ve que se cumple la condición anterior.
            y = i # la variable y adopta el valor más actual de i.
            # print(y, x), para verificar cómo avanza el loop y comprobar errores.
        elif df2.AMP3FT[i] > mV and x < 3: # genero otras dos condiciones por si no se cumplen las anteriores. En este caso si el CBL es mayor al estabelcido, x vuelve a cero.
            x = 0 # si el valor del CBL es mayor al establecido como bueno, la cuenta vuelve a cero.
            # y = i, para verificar cómo avanza el loop y comprobar errores.
            # print(y, x), para verificar cómo avanza el loop y comprobar errores.
        else:
            break # si no se cumplen ninguna de las condiciones anteriores, el loop rompe.

    # Una vez que el loop rompe, tengo el valor de y = i de la iteración en la cual se cumplen x (en este caso 3) metros.
    # Por lo tanto x será 3 o más, i será el nñumero de iteración que cumple con x = 3 o más.

    z = y - int(x / ((df2[0][i]) - 1)) # z es el valor donde la función comienza a cumplirse.
    # toc = df2.DEPT[z] es el tope de cemento definido.

    df_new = df2[z:len(df2)] # genero un dataframe en el que se eliminan los valores superiores al tope de cemento.
    df_new # visualizo el dataframe generado.

    key = ['mean', 'max', 'min', 'q5', 'q10', 'q15', 'q20', 'q25', 'q30', 'q35', 'q40', 'q45', 'q50', 'q55', 'q60', 'q65', 'q70', 'q75', 'q80', 'q85', 'q90', 'q95'] 
    # lista con cuantiles generados
    values = [] # se genera una lista vacia que se ira llenando a medida que el loop avance
    values.append(df_new['AMP3FT'].mean()) # agrega la media a la lista values.
    values.append(df_new['AMP3FT'].max()) # agrega el valor máximo a la lista values.
    values.append(df_new['AMP3FT'].min()) # agrega el valor mínimo a la lista values.

    for q in range(5,100,5): # loop desde 5 a 100 con paso 5 para los distintos cuantiles.
        values.append(df_new['AMP3FT'].quantile(q/100)) # función que agrega el valor calculado del cuantil a la lista values.
    
    df_final = pd.DataFrame(values, index=key) # se genera un dataframe con los valores de la lista values y los indices de la lista key. Ver cómo trasponer.
    df_final_2 = df_final.T # se muestra el dataframe.

df_final_2.to_excel('dff2.xlsx', 'Sheet1')

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Ver pruebalog.py
# Problema con los distintos nombres de 'CBL'
# Falta incorporar en el index, el nombre del pozo.
# Falta resolver el tema de agregar una fila por cada loop de archivo
# Falta incorporar algunos cálculos al final del source code.