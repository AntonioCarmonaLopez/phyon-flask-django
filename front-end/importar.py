import csv
'''
importaciones motor alchemy, sesión de ámbitos y creador de sesiones
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

archivo = 'articulos.csv'

try:
	conn = 'postgresql://web:web@127.0.0.1/articulos'
except:
        print("Conexión a BD ko")

engine = create_engine(conn)
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open(archivo)
	reader = csv.reader(f)
	for id,titulo,cuerpo,autor in reader:
		try:
			db.execute("INSERT INTO articulos (id,titulo,cuerpo,autor) VALUES (:id,:titulo,:cuerpo,:autor)",
            		{"id":id,"titulo": titulo,"cuerpo":cuerpo, "autor": autor})		
			print(f"articulo con id {id} añadido de {autor} y titulo {titulo}")
			db.commit()
		except Exception as ex:
        		print(ex)
if __name__ == "__main__":
	main()
