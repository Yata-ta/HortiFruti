from sqlite3 import dbapi2
from xml.etree.ElementTree import tostring
import psycopg2
import os
import numpy as np
from numpy import * 
import time

os.system('cls' if os.name == 'nt' else 'clear')

class DB(object):
   _db=None

   def __init__(self, url, username, password, con):
    self.url = "db.fe.up.pt"
    self.username = "up201801019"
    self.password = "CR6oJPBwF"
    self.con = None

def connect(db):
    """ Connect to the PostgreSQL database server """
    DB
    conn = None
    try:


        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=db.url,database=db.username, user=db.username, password=db.password,port="5432")

        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
    
        #cur.close()
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
	# close the communication with the PostgreSQL
    '''
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    '''


def identificacao(db, contentorId):
    pedido = 'Select * from up201801019.contentor where contentorid=' + contentorId
    executar(db,pedido)
    rec = db.fetchone()
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None, None
    return rec[1], rec[2]

def executar(db, pedido):
    try:
       result = db.execute(pedido)
       return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return

def get_value_sensores(db, contentorId):
    pedido = 'Select * from up201801019.sensor where contentorid=' + contentorId
    executar(db,pedido)
    rec = db.fetchone()
    
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None, None
    tipo = []
    valores = []

    tipo.append(rec[1])
    valores.append(rec[2])
    for rec in db:
        tipo.append(rec[1])
        valores.append(rec[2])
    return tipo, valores

def get_specific_value_sensor(db, contentorId, tipe,sensid):
    if sensid == None:
        pedido = "Select * from up201801019.sensor where contentorid=" + contentorId + " and tipo='"  + tipe + "'"
    else: 
         pedido = "Select * from up201801019.sensor where contentorid=" + contentorId + " and sensid='"  + sensid + "'"
    executar(db,pedido)
    rec = db.fetchone()[2]
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None
    
    return rec

def get_value_atuadores(db, contentorId):
    pedido = 'Select * from up201801019.atuador where contentorid=' + contentorId
    executar(db,pedido)
    rec = db.fetchone()
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None, None
    tipo = []
    valores = []

    tipo.append(rec[1])
    valores.append(rec[2])
    for rec in db:
        tipo.append(rec[1])
        valores.append(rec[2])
    return tipo, valores

def get_specific_value_atuador(db, contentorId, tipe,atuadorid):
    if atuadorid == None:
        pedido = "Select * from up201801019.atuador where contentorid=" + contentorId + " and tipo='"  + tipe + "'"
    else: 
         pedido = "Select * from up201801019.atuador where contentorid=" + contentorId + " and atuadid='"  + atuadorid + "'"
    executar(db,pedido)
    rec = db.fetchone()[2]
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None
    
    return rec




contentorId = '1'
while(1):
    db_con, connection=connect(DB(None,None,None,None))
    fruta, utilizadorid = identificacao(db_con, contentorId)
    print(fruta, utilizadorid)

    tipo, valor = get_value_sensores(db_con, contentorId)
    print(tipo, valor)

    valor = get_specific_value_sensor(db_con, contentorId, 'temperatura', None)
    print( valor)

    tipo, valor = get_value_atuadores(db_con, contentorId)
    print(tipo, valor)

    valor = get_specific_value_atuador(db_con, contentorId, 'Exaustor', None)
    print( valor)
        
    if connection is not None:
            connection.close()
            print('Database connection closed.')

    time.sleep(1)

#for row in db_con: 
#    print("\n", row)
