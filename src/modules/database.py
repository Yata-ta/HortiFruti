#               Dependencias

from sqlite3 import dbapi2
from xml.etree.ElementTree import tostring
import psycopg2
import os
import numpy as np
from numpy import *
import time
from time import gmtime, strftime
from dotenv import load_dotenv


#           CLASSE COM INFO SOBRE A BASE DADOS

class DB:

    def __init__(self):
        load_dotenv('../db_credentials.env')
        self.url = "ec2-54-75-26-218.eu-west-1.compute.amazonaws.com"
        self.database = os.environ['DBNAME']
        self.username = os.environ['USERNAME']
        self.password = os.environ['DBPW']
        self.con = None


#               FAZ A CONECÇÃO COM A BASE DADOS

def connect(db):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
       # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=db.url, database=db.database, user=db.username, password=db.password, port="5432")

        # create a cursor
        cur = conn.cursor()

        # cur.close()
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("na db")
    # close the communication with the PostgreSQL
    '''
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    '''

#               OBTER IDENTIFICAÇÃO DO CONTENTOR (FRUTA E UTILIZADORID)

def identificacao(db, contentorId):
    pedido = 'Select * from up201801019.contentor where contentorid=' + contentorId
    executar(db, pedido)
    rec = db.fetchone()
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None, None
    return rec[1], rec[2]

#               IDENTIFICAÇÃO DE CONTENTORES PARA RASPBERRY RESPETIVA

def get_id_contentores( raspberry_id):
    
    db, connection = connect(DB())

    pedido = 'Select contentorid from up201801019.contentor where raspberryid=' + str(raspberry_id)
    executar(db, pedido)
    rec = db.fetchone()
        # Close db connection

    if rec == None:
        if connection is not None:
            connection.close()
    #    print('Database connection closed.')       
        return None

    valores=[]
    valores.append(rec[0])
    for rec in db:
        valores.append(rec[0])

    if connection is not None:
            connection.close()
    #    print('Database connection closed.')  
    return valores


#               EXECUTA O PEDIDO (NUNO)


def executar(db, pedido):
    try:
        result = db.execute(pedido)
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return


#               EXECUTA O PEDIDO (VITOR)        comentario: pq usaste outra função de executar a query quando ja tinha definido em cima?? xddd

def executequery(cursor, connection, query):
    try:
        cursor.execute(query)
        connection.commit()

        count = cursor.rowcount
        return count

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return


#               OBTER VALOR DE TODOS SENSORES DO CONTENTOR


def get_value_sensores(contentorId):
    db, connection = connect(DB())

    pedido = 'Select * from up201801019.sensor where contentorid=' + str(contentorId)
    executar(db, pedido)
    rec = db.fetchall()
    if rec == None:
        if connection is not None:
            connection.close()
        return None

    # Close db connection
    if connection is not None:
        connection.close()
       # print('Database connection closed.')
    return rec


#               OBTER VALOR DE SENSOR INDIVIDUAL: IDENTIFICACAO POR ID OU TIPO


def get_specific_value_sensor(db, contentorId, tipe, sensid):
    if sensid == None:
        pedido = "Select * from up201801019.sensor where contentorid=" + contentorId + " and tipo='" + tipe + "'"
    else:
        pedido = "Select * from up201801019.sensor where contentorid=" + contentorId + " and sensid='" + sensid + "'"
    executar(db, pedido)
    rec = db.fetchone()[2]
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None

    return rec


#               OBTER ID DE TODOS SENSOR POR CONTENTOR

def get_id_sensor(db, contentorId):
    pedido = "Select * from up201801019.sensor where contentorid=" + contentorId
    executar(db, pedido)
    rec = db.fetchone()

    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None
    id = []

    id.append(rec[0])
    for rec in db:
        id.append(rec[0])

    return id

#               OBTER ID DE TODOS ATUADORES POR CONTENTOR

def get_id_atuador(db, contentorId):
    pedido = "Select * from up201801019.atuador where contentorid=" + contentorId
    executar(db, pedido)
    rec = db.fetchone()

    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None
    id = []

    id.append(rec[0])
    for rec in db:
        id.append(rec[0])

    return id


#               OBTER VALOR DE TODOS ATUADORES DO CONTENTOR

def get_value_atuadores(contentorId):
    db, connection = connect(DB())

    pedido = 'Select * from up201801019.atuador where contentorid=' + str(contentorId)
    executar(db, pedido)
    rec = db.fetchall()
    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None
    
    # Close db connection
    if connection is not None:
        connection.close()
    #    print('Database connection closed.')

    return rec
    
#               OBTER VALOR DE ATUADOR INDIVIDUAL: IDENTIFICACAO POR ID OU TIPO


def get_specific_value_atuador( contentorId, tipe, atuadorid):
    
    db, connection = connect(DB())

    if atuadorid == None:
        pedido = "Select valor_atual from up201801019.atuador where contentorid=" + contentorId + " and tipo='" + tipe + "'"
    else:
        pedido = "Select valor_atual from up201801019.atuador where contentorid=" + contentorId + " and atuadid='" + atuadorid + "'"
    executar(db, pedido)
    rec = db.fetchone()
    
        # Close db connection
    if connection is not None:
        connection.close()
    #    print('Database connection closed.')

    if rec == None:
        print("Não foi encontrado o pedido na DB")
        return None

    return rec[0]


#               DEFINE VALOR DE TODOS SENSORES DO CONTENTOR


def send_values_sensores(db, connection, contentorId, tipo, valor_atual):
    for i in range(len(tipo)):
        pedido = "Update up201801019.sensor SET valor_atual = " + str(
            valor_atual[i]) + " where contentorid=' " + contentorId + "' and tipo='" + tipo[i] + "'"
        
        executequery(db, connection, pedido)
    # rec = db.fetchone()
    # if rec == None:
    #   print("Não foi encontrado o pedido na DB")
    #  return -1

    return 1

#               DEFINE VALOR DE SENSOR INDIVIDUAL: IDENTIFICACAO POR ID

def set_value_sensor( sensid, tempo, valor):
    
    db, connection = connect(DB())

    query = "INSERT INTO up201801019.historico_sensor(data_hora, medição, sensID) VALUES ('"+ tempo +"'," + str(valor) + ", " + str(sensid) +");"
  #  print(query)
    result = executequery(db, connection, query)

    query = "UPDATE up201801019.sensor SET valor_atual = "+ str(valor) + " WHERE sensid = " + str(sensid) + ";"
    print
    result = executequery(db, connection, query)

    
    # Close db connection
    if connection is not None:
        connection.close()
        print('Database connection closed.')

    return result

#               DEFINE VALOR DE ATUADOR INDIVIDUAL: IDENTIFICACAO POR ID

def set_value_atuador( atuadorid,  tempo,valor):
    
    db, connection = connect(DB())

    query = "INSERT INTO up201801019.historico_atuador(data_hora, estado, atuadID) VALUES ('"+ tempo + "',"+ str(valor) +" ," + str(atuadorid) +");"
    #print(query)
    result = executequery(db, connection, query)

    query = "UPDATE up201801019.atuador SET valor_atual = "+ str(valor) + " WHERE atuadid = " + str(atuadorid) + ";"
    result = executequery(db, connection, query)
    
    if connection is not None:
        connection.close()
        #print('Database connection closed.')

    return result

#               INSERE ALARME

def add_alarm(db, connection, contentorid, tempo, prioridade, texto):

    query = "INSERT INTO up201801019.alarme(data_hora, prioridade, descrição, contentorid) VALUES ('"+ tempo + "',"+ str(prioridade) +" ,'" + texto +"', "+ str(contentorid) + ");"
    print(query)
    result = executequery(db, connection, query)

    return result


#               ZONA DE TESTE/DEBUG
'''
contentorId = '1'
while (1):
    time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    db_con, connection = connect(DB())
    fruta, utilizadorid = identificacao(db_con, contentorId)
    print(fruta, utilizadorid)

    tipo1, valor1 = get_value_sensores(db_con, contentorId)

    print(tipo1, valor1)

    valor = get_specific_value_sensor(db_con, contentorId, 'temperatura', None)
    print(valor)

    tipo, valor = get_value_atuadores(db_con, contentorId)
    print(tipo, valor)

    valor = get_specific_value_atuador(db_con, contentorId, 'Exaustor', None)
    print(valor)

    send_values_sensores(db_con, connection, contentorId, tipo1, valor1)
    set_value_sensor(db_con, connection, 6, str(time_date), 90)
    set_value_atuador(db_con, connection, 6, str(time_date), 0)

    add_alarm(db_con, connection, 1, str(time_date), 5, "Ta pegando fogo")

    if connection is not None:
        connection.close()
        print('Database connection closed.')

    time.sleep(1)

'''