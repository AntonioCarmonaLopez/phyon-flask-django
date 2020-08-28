import csv
'''
importaciones motor alchemy, sesión de ámbitos y creador de sesiones
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

archivo = 'vuelos.csv'

try:
	conn = 'postgresql://web:web@127.0.0.1/vuelos'
except:
        print("Conexión a BD ko")

engine = create_engine(conn)
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open(archivo)
	reader = csv.reader(f)
	for id,origen,destino,duracion in reader:
		try:
			db.execute("INSERT INTO vuelos (id,origen, destino, duracion) VALUES (:id,:origen, :destino, :duracion)",
            		{"id":id,"origen": origen, "destino": destino, "duracion": int(duracion)})		
			print(f"vuelo con id {id} añadido de {origen} a {destino} y duración {duracion}")
			db.commit()
		except Exception as ex:
        		print(ex)
if __name__ == "__main__":
	main()
