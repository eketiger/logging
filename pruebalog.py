# Programa para correr sobre los documentos en excel de perfiles eléctricos de pozo.

import pandas as pd # Importa libreria de manejo de dataframes
import glob			# Importa libreria para manejo de archivos con cierto pathname definido

filenames = glob.glob('*.xlsx')	# Genera una lista con los archivos que matchean con la búsqueda, en este caso todos los excel (.xlsx)
lista_nombres_archivos = [pd.read_excel(filename) for filename in filenames]
lna = lista_nombres_archivos



# Para hacer loop sobre los archivos e ir tratandolos.
for i in range(len(filenames)):
# Acá iría lo que se debería correr junto a la lista generada (quantiles, máximos, etc. y resultado)
# Ver cómo se puede ir sumando a una lista o serie o diccionario, el resultado de lo obtenido.
# Se puede crear un diccionario inicial antes de correr cualquier cosa, tneiendo en cuenta lo que se
# va a calcular (percentiles, máximos, mínimos, etc.) e ir sumando en cada loop al diccionario. Tener
# en cuenta que también se tiene que agregar el nombre del archivo como 'index' de fila.
# Ver cómo hacer todos los percentiles con un loop.
q5_CBL = la[0].iloc[:,1].quantile(.05)
q10_CBL = la[0].iloc[:,1].quantile(.1)
q15_CBL = la[0].iloc[:,1].quantile(.15)
q20_CBL = la[0].iloc[:,1].quantile(.2)
q25_CBL = la[0].iloc[:,1].quantile(.25)
q30_CBL = la[0].iloc[:,1].quantile(.3)
q35_CBL = la[0].iloc[:,1].quantile(.35)
q40_CBL = la[0].iloc[:,1].quantile(.4)
q45_CBL = la[0].iloc[:,1].quantile(.45)
q50_CBL = la[0].iloc[:,1].quantile(.5)
q55_CBL = la[0].iloc[:,1].quantile(.55)
q60_CBL = la[0].iloc[:,1].quantile(.6)
q65_CBL = la[0].iloc[:,1].quantile(.65)
q70_CBL = la[0].iloc[:,1].quantile(.7)
q75_CBL = la[0].iloc[:,1].quantile(.75)
q80_CBL = la[0].iloc[:,1].quantile(.8)
q85_CBL = la[0].iloc[:,1].quantile(.85)
q90_CBL = la[0].iloc[:,1].quantile(.9)
q95_CBL = la[0].iloc[:,1].quantile(.95)
# Son igual
# la[0].iloc[:,1].min()
# la[0].loc[:,'nombre de columna'].min()
# la[0]['nombre de columna'].min()
sum_DEPTH = la[0].iloc[:,0].max()
# Ver cómo hacer todos los percentiles con un loop.
min_CBL = la[0].iloc[:,1].min()
max_CBL = la[0].iloc[:,1].max()
mean_CBL = la[0].iloc[:,1].mean()

# Acá va a código para agregar todos los valores calculados arriba a una lista, serie o diccionario.
# append(¿?) para ir armando la serie(¿?). Cada uno de los archivos daría como resultado una serie. 
# Al final se arma un data frame con todas las series.
WellDataSet = list(zip('nombre_lista_1', 'nombre_lista_2', 'nombre_lista_n')) # O con Series(¿?) 
df_final = pd.DataFrame(data = WellDataSet, columns=['nombres de cada uno de los archivos', 'n2', 'n3'])


# Para agregar una columna con el nombre del archivo, revisar este codigo para utilizarlo en la
# incorporación del nombre de archivo a lo que sería el index de la lista, serie o value del key=Pozo
# en el caso de un diccionario.
for dataframe, filename in zip(dataframes, filenames):
  dataframe['Pozo'] = filename

# Para chequear el tipo
type(dataframes[0])