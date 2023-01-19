#               Dependencias

from sqlite3 import dbapi2
from xml.etree.ElementTree import tostring
import psycopg2
import os
import numpy as np
from numpy import *
import time
from time import gmtime, strftime


#           CLASSE COM INFO SOBRE A BASE DADOS

class DB:

    def __init__(self):
        self.url = "db.fe.up.pt"
        self.username = "up201801019"
        self.password = "CR6oJPBwF"
        self.con = None


#               FAZ A CONECÇÃO COM A BASE DADOS

def connect(db):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')

        # To use FEUP's database you just need to uncomment the line below
        # FEUP Database
        # conn = psycopg2.connect(host=db.url, database=db.username, user=db.username, password=db.password, port="5432")

        # Heroku Database
        DATABASE_URL = 'postgres://kxxubuuaqoiacg:baee797511a5a5a24c7124d3495a82ce9fc4ac0ff874d1181d909f0b7e2adf4a@ec2-54-75-26-218.eu-west-1.compute.amazonaws.com:5432/d5s6ue6qinl0ng'
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        
        # create a cursor
        cur = conn.cursor()

        # cur.close()
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


#               OBTER IDENTIFICAÇÃO DO CONTENTOR (FRUTA E UTILIZADORID)

def identificacao(db, contentorId):
    try:
        pedido = 'Select * from up201801019.contentor where contentorid=' + contentorId
        executar(db, pedido)
        rec = db.fetchone()
        if rec == None:
            print("Não foi encontrado o pedido na DB")
            return None, None
        return rec[1], rec[2]

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
#               IDENTIFICAÇÃO DE CONTENTORES PARA RASPBERRY RESPETIVA





def get_id_contentores( raspberry_id):

    try:
        print(0)
        db, connection = connect(DB())
        print(1)
        pedido = 'Select contentorid from up201801019.contentor where raspberryid=' + str(raspberry_id)
        print(2)
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

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

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

    try:
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

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


#               OBTER VALOR DE SENSOR INDIVIDUAL: IDENTIFICACAO POR ID OU TIPO


def get_specific_value_sensor(db, contentorId, tipe, sensid):

    try:

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

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


#               OBTER ID DE TODOS SENSOR POR CONTENTOR

def get_id_sensor(db, contentorId):
    try:
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
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

#               OBTER ID DE TODOS ATUADORES POR CONTENTOR

def get_id_atuador(db, contentorId):
    try:
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
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

#               OBTER VALOR DE TODOS ATUADORES DO CONTENTOR

def get_value_atuadores(contentorId):
    try:
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
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_nivel(atuador_id):
  try:      
    db, connection = connect(DB())
    
    pedido = "Select dashboard from up201801019.atuador where atuadid=" + str(atuador_id)
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

  except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
#               OBTER VALOR DE ATUADOR INDIVIDUAL: IDENTIFICACAO POR ID OU TIPO


def get_specific_value_atuador( contentorId, tipe, atuadorid):

    try:
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
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

#               DEFINE VALOR DE TODOS SENSORES DO CONTENTOR


def send_values_sensores(db, connection, contentorId, tipo, valor_atual):
    try:
        for i in range(len(tipo)):
            pedido = "Update up201801019.sensor SET valor_atual = " + str(
                valor_atual[i]) + " where contentorid=' " + contentorId + "' and tipo='" + tipo[i] + "'"

            executequery(db, connection, pedido)
        # rec = db.fetchone()
        # if rec == None:
        #   print("Não foi encontrado o pedido na DB")
        #  return -1

        return 1
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
#               DEFINE VALOR DE SENSOR INDIVIDUAL: IDENTIFICACAO POR ID

def set_value_sensor( sensid, tempo, valor):
    try:
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
            #print('Database connection closed.')

        return result
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_timings(cont_id, timing_sens, timing_actu):
    try:
        db, connection = connect(DB())

        pedido = "Select refresh_rate_sensores, atuatores_min_time from up201801019.contentor where contentorid =" + str(cont_id)
        executar(db, pedido)
        rec = db.fetchone()

        # Close db connection
        if connection is not None:
            connection.close()
        #    print('Database connection closed.')

        if rec == None:
            print("Não foi encontrado o pedido na DB")
            return None

        return rec
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return timing_sens, timing_actu
#               DEFINE VALOR DE ATUADOR INDIVIDUAL: IDENTIFICACAO POR ID

def set_value_atuador( atuadorid,  tempo,valor):
    try:
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
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
#               INSERE ALARME

def add_alarm(contentorid, tempo, prioridade, texto):
    try:
        db, connection = connect(DB())
        
        query = "INSERT INTO up201801019.alarme(data_hora, prioridade, descrição, contentorid) VALUES ('"+ tempo + "',"+ str(prioridade) +" ,'" + texto +"', "+ str(contentorid) + ");"
        print(query)
        result = executequery(db, connection, query)
        
        # Close db connection
        if connection is not None:
            connection.close()
        #    print('Database connection closed.')

        if rec == None:
            print("Não foi encontrado o pedido na DB")
            return None

        return result

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
#               ZONA DE TESTE/DEBUG




