import sqlite3

#claves ajenas y triggers en https://programadoresnocturnos.wordpress.com/2010/01/02/uso-de-sqlite/

def destruyeBD(nombreBD="reservasTaxis.sdb"):
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(nombreBD)
        # Get a cursor object
        cursor = db.cursor()
       
        cursor.execute('''DROP TABLE IF EXISTS users''')
        cursor.execute('''DROP TABLE IF EXISTS reservations''')
        cursor.execute('''DROP TABLE IF EXISTS cars''')
       
        # Commit the change
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()
    

def creaBD(nombreBD="reservasTaxis.sdb"):
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(nombreBD)
        # Get a cursor object
        cursor = db.cursor()

        # Check if table users does not exist and create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                          users(id_user INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS
                          cars(car_id INTEGER PRIMARY KEY, matricula TEXT UNIQUE, marca TEXT, modelo TEXT, color TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS
                          reservations(id_res INTEGER PRIMARY KEY, id_car INTEGER, id_user INTEGER, fecha TEXT, hora TEXT)''')

        # Commit the change
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()



def borraDatos(nombreBD="agendaMedica.sdb"):
    try:
        db = sqlite3.connect(nombreBD)
        cursor=db.cursor()
        cursor.execute("DELETE FROM citas")
        cursor.execute("DELETE FROM medicos")
        cursor.execute("DELETE FROM pacientes")
        db.commit()
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()

def introduceMedicos(nombreBD="agendaMedica.sdb"):
    try:
        db = sqlite3.connect(nombreBD)
        cursor=db.cursor()
        cursor.execute("DELETE FROM medicos")
        medicos = [('Angel Lozano', 'Vistahermosa 76', 'Aparato Digestivo'),
                   ('Alberto Agullo','Vistahermosa 76', 'Dermatologia'),
                   ('Diana Fernandez','Vistahermosa 76', 'Dermatologia')]
        cursor.executemany(''' INSERT INTO medicos(nombre, centro, especialidad) VALUES(?,?,?)''', medicos)
        db.commit()
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()

def introducePacientes(nombreBD="agendaMedica.sdb"):
    try:
        db = sqlite3.connect(nombreBD)
        cursor=db.cursor()
        cursor.execute("DELETE FROM pacientes")
        pacientes = [('Lorenzo Peña',),
                   ('Alicia Hernandez',),
                   ('Rosa Perez',),
                   ('Alvaro Escantola',),
                   ('Rui de la Sierra',),
                   ('Pia Gonzalez',)]
        cursor.executemany('INSERT OR IGNORE INTO pacientes(nombre) VALUES(?)', pacientes)
        db.commit()
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def introduceCitas(nombreBD="agendaMedica.sdb"):
    try:
        db = sqlite3.connect(nombreBD)
        cursor=db.cursor()
        cursor.execute("DELETE FROM citas")
        citas = [  (1, 1, 'Dolor estomago', '11:15'),
                   (1, 2, 'Acidez', '11:00'),
                   (1, 3, 'Ulcera sangrante', '11:30'),
                   (1, 4, 'Revision','11:45'),
                   (1, 5, 'Revision','12:30'),
                   (1, 6, 'Tos cronica','13:00')]
        cursor.executemany(''' INSERT OR IGNORE INTO citas(idmed, idpac, motivo, hora) VALUES(?,?,?,?)''', citas)
        db.commit()
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def consultaMedicos(nombreBD="agendaMedica.sdb"):
    db = sqlite3.connect(nombreBD)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM medicos''')
    for row in cursor:
        # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} : {1}, {2}, {3}'.format(row['id'],row['nombre'], row['centro'], row['especialidad']))
    db.close()


def consultaPacientes(nombreBD="agendaMedica.sdb"):
    db = sqlite3.connect(nombreBD)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM pacientes''')
    for row in cursor:
        # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} : {1}'.format(row['id'], row['nombre'])) 
    db.close()

def consultaCitas(nombreBD="agendaMedica.sdb"):
    db = sqlite3.connect(nombreBD)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM citas''')
    for row in cursor:
        # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} {1}: {2} ({3})'.format(row['id'], row['hora'], row['idpac'],row['motivo']))
    db.close()

def consultaCitasCompletas(nombreBD="agendaMedica.sdb"):
    db = sqlite3.connect(nombreBD)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT hora,medicos.nombre as nombremed,pacientes.nombre as nombrepac,motivo FROM citas,medicos,pacientes \
WHERE citas.idmed=medicos.id AND pacientes.id=citas.idpac AND citas.idmed=1 ORDER BY hora
''')
    for row in cursor:
        # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} {1}: {2} ({3})'.format(row['hora'], row['nombremed'], row['nombrepac'],row['motivo']))
    db.close()
   

def defineTriggerBorradoPacientes(nombreBD="agendaMedica.sdb"):
    db = sqlite3.connect(nombreBD)
    cursor = db.cursor()
    cursor.execute("CREATE TRIGGER IF NOT EXISTS fk_citas \
                    before delete on pacientes \
                    for each row \
                       begin \
                           select raise(rollback,'No se puede eliminar paciente') \
                           where\
                              (select idpac from citas where old.id=idpac) \
                               is not null; \
                       end")
    db.commit()
    db.close()


def pruebaTriggerBorradoPacientes(nombreBD="agendaMedica.sdb"):
    try:
        db = sqlite3.connect(nombreBD)
        cursor = db.cursor()
        cursor.execute("DELETE FROM pacientes where id=?",(1,))
        db.commit()
    except Exception as e:
        pass

    finally:
        db.close()




creaBD("reservaTaxis.sdb")





