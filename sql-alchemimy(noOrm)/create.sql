CREATE TABLE aeropuertos (
	codigo VARCHAR PRIMARY KEY,
	nombre VARCHAR NOT NULL
);

CREATE TABLE vuelos (
	id VARCHAR PRIMARY KEY,
	origen VARCHAR NOT NULL,
	destino VARCHAR NOT NULL ,
	duracion INTEGER NOT NULL
);

CREATE TABLE pasajeros (
	id SERIAL PRIMARY KEY,
	nombre VARCHAR NOT NULL,
	vuelo_id INTEGER NOT NULL REFERENCES vuelos
	
);

INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('JFK','Nueva York');
INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('PVG','Shangai');
INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('IST','Estambul');
INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('LHR','Londrés');
INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('SVO','Moscú');
INSERT INTO aeropuertos
	(id,codigo,nombre)
	VALUES ('LIM','Lima');
INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('CDG','París');
INSERT INTO aeropuertos
	(codigo,nombre)
	VALUES ('NRT','Tokio');

INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('1','Nueva York','Estambul',530);
INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('2','Shangai','París',545);
INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('3','Estambul','Moscú',600);
INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('4','Londrés','Shanghai',615);
INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('5','Moscú','Nueva York',630);
INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('6','Lima','Londrés',645);
INSERT INTO vuelos
	(id,origen,destino,duracion)
	VALUES ('7','París','Moscú',660);

