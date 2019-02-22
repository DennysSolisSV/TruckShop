conectarme a postgrest

sudo -u postgres psql


listar las bases de datos del usuario 

\list


selecionar una base de datos

\c truckbase


SELECT * FROM table;
UPDATE table SET campo1 = campo2 WHERE campo3 < 10;
DELETE table WHERE campo3 < 10;
INSERT INTO table (campo1, campo2) VALUES (1,2);