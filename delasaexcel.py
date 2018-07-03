import glob			# Importa libreria para manejo de archivos con cierto pathname definido
import lasio		# Permite ejecutar unas conversión sobre archivos con extensión .las

archivos = glob.glob('*.las') # Genero una lista con todos los .las de la carpeta

for x in range(0, len(archivos)): # loop que permite recorrer todos los archivos, leerlos y generar un .xlsx.
	lectura = lasio.read(archivos[x])
	lectura.to_excel(str(archivos[x][:-4] + '.xlsx')) # quita la extensión .las y agrega la extensión .xlsx

