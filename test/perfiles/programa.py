import pandas as pd # se importa el modulo pandas para manejo de dataframes.
import glob         # Importa libreria para manejo de archivos con cierto pathname definido
import lasio        # Permite ejecutar unas conversión sobre archivos con extensión .las
import re           # Importa el modulo re para recortar el nombre del archivo y dejar solo el del pozo

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

archivos_lasm = glob.glob('*.las') # genera una lista con todos los .las de la carpeta
archivos_lasM = glob.glob('*.LAS')
archivos_las = archivos_lasm + archivos_lasM
frames = []

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

for n in range(0, len(archivos_las)): # loop que permite recorrer todos los archivos
    df = lasio.read(archivos_las[n]).df() # genera un dataframe por cada archivo
    df.reset_index(level=0, inplace=True)
    x = 0 # se establece el valor cero de inicio a la variable x.
    mV = 20 # se define el valor de amplitud para el cual se considera el tope de cemento.
    m = 5

    paso = [] # se define la lista paso vacía (Sería más reocmendable generar una Serie de pandas)

    for o in range(0, len(df.DEPT)-1): # se hace un loop sobre la lista para generar la columna paso.
        paso.append(df.DEPT[o+1] - df.DEPT[o])

    paso.append(paso[len(paso)-1]) # se genera el último valor de la lista para que paso tenga la misma cantidad de items que las otras columnas

    s = pd.Series(paso)

    df01 = pd.concat([df,s], axis=1) # agrega la Serie: paso, al dataframe df y se reemplaza el nombre.
    
    # df2.DEPT es la lista DEPT del dataframe df, en realidad serie de pandas DEPT
    # df2.CBL (AMP3FT) es la lista CBL del dataframe df, en realidad serie de pandas CBL.

    df02 = df01[df01.DEPT > 50]

    atributos = ['CBLF', 'AMP3FT']

    df02 = df02.rename(columns={"CBLF":"AMP3FT"})

    CBL_dfa = df02.AMP3FT
    
    df03 = df02[CBL_dfa > 0]
    df04 = df03.reset_index()
    df2 = df04.iloc[:,1:]
    
    CBL_df = df2.AMP3FT
    CBL_str = 'AMP3FT'

    x = 0
    y = 0

    # El error esta en que i arranca desde la celda que se borro, se deberìa reindexar todo el dataframe

    for i in range(0, len(CBL_df)): # empiezo un loop de cero a la longitud de la lista CBL.
        if CBL_df[i] <= mV and x < m: # genero dos condiciones x < 3 (este valor puede cambiar), y el CBL menor o igual al definido (este valor también puede cambiar).
            x = x + df2[0][i] # sumo un paso al valor de la variable x cada que ve que se cumple la condición anterior.
            y = i # la variable y adopta el valor más actual de i.
            # print(y, x), para verificar cómo avanza el loop y comprobar errores.
        elif CBL_df[i] > mV and x < m: # genero otras dos condiciones por si no se cumplen las anteriores. En este caso si el CBL es mayor al estabelcido, x vuelve a cero.
            x = 0 # si el valor del CBL es mayor al establecido como bueno, la cuenta vuelve a cero.
            # y = i, para verificar cómo avanza el loop y comprobar errores.
            # print(y, x), para verificar cómo avanza el loop y comprobar errores.
        else:
            break # si no se cumplen ninguna de las condiciones anteriores, el loop rompe.

    # Una vez que el loop rompe, tengo el valor de y = i de la iteración en la cual se cumplen x (en este caso 3) metros.
    # Por lo tanto x será 3 o más, i será el nñumero de iteración que cumple con x = 3 o más.

    z = y - int(x / ((df2[0][i]) - 1)) # z es el valor donde la función comienza a cumplirse.
    toc = df2.DEPT[z] # es el tope de cemento definido.

    df_new = df2[z:len(df2)] # genero un dataframe en el que se eliminan los valores superiores al tope de cemento.
    # df_new visualizo el dataframe generado.

    mV_df = df_new.AMP3FT

    key = ['toc', 'max_depth', 'cbl_mean', 'cbl_max', 'cbl_min', 'cbl_q5', 'cbl_q10', 'cbl_q15', 'cbl_q20', 
    'cbl_q25', 'cbl_q30', 'cbl_q35', 'cbl_q40', 'cbl_q45', 'cbl_q50', 'cbl_q55', 'cbl_q60', 'cbl_q65', 'cbl_q70',
    'cbl_q75', 'cbl_q80', 'cbl_q85', 'cbl_q90', 'cbl_q95', 'cbl_5mV', 'cbl_10mV', 'cbl_15mV', 'cbl_20mV', 'cbl_25mV',
    'cbl_30mV', 'cbl_35mV', 'cbl_40mV', 'cbl_45mV', 'cbl_50mV', 'cbl_55mV', 'cbl_60mV', 'cbl_65mV', 'cbl_70mV'] 
    # se generan los atributos para la tabla

    values = [] # se genera una lista vacia que se ira llenando a medida que el loop avance
    values.append(toc) # agrega el valor del TOC.
    values.append(df_new['DEPT'].max()) # agrega la profundidad del registro.
    values.append(df_new[CBL_str].mean()) # agrega la media a la lista values.
    values.append(df_new[CBL_str].max()) # agrega el valor máximo a la lista values.
    values.append(df_new[CBL_str].min()) # agrega el valor mínimo a la lista values.

    for q in range(5,100,5): # loop desde 5 a 100 con paso 5 para los distintos cuantiles.
        values.append(df_new[CBL_str].quantile(q/100)) # función que agrega el valor calculado del cuantil a la lista values.
    
    for r in range(5,75,5): # loop desde 5 a 75 con paso 5 para las distintas atenuaciones.
    	values.append(df_new[mV_df < r][0].sum() / df_new['DEPT'].max())

    pozo = archivos_las[n]
    match = re.search(r'(?<=YPF.SC.)[\w.]+-[\d(]+', pozo) # regular expresions que me permiten hacer un slice sobre el nombre del pozo.
    if match:
    	nombre = match.group()
    else:
    	nombre = 'not_found' + str([n])

    df_final = pd.DataFrame(values, index=key, columns=[nombre]) # se genera un dataframe con los valores de la lista values y los indices de la lista key. Ver cómo trasponer.
    df_final_2 = df_final.T # se muestra el dataframe.

    frames.append(df_final_2)

result = pd.concat(frames)

result.to_excel('resultado.xlsx', 'Sheet1')

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Problema con los distintos nombres de 'CBL'
# Ordenar por profundidad
# Eliminar filas con valores de CBL negativos
# Revisar valores con perfiles
# Ver pruebalog.py