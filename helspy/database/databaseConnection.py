import psycopg2
import os
import sys
import json
from psycopg2.errors import UndefinedTable

class DatabaseConnection():

  def __init__(self, configOptions):
    self.__connection = None
    self.__runID = None
    self.__runDict = { "timestamp": configOptions["timestamp"] }
    self.__filesystemInfoDict = {
      "mountpoint": configOptions["mountpoint"],
      "hostname":   configOptions["hostname"],
      "filesystem": configOptions["filesystem"]
    }

    connectionString = DatabaseConnection.__createConnectionString(configOptions["DBMS"])
    self.__connection = psycopg2.connect(connectionString)

  def __createConnectionString(configOptions):
    username = configOptions["username"]
    database = configOptions["database"]
    hostname = ""
    password = ""
    if "hostname" in configOptions:
      hostname = configOptions["hostname"]
    if "password" in configOptions:
      password = configOptions["password"]
    connectionStringList = [ "postgresql://" ]
    connectionStringList.append( username )
    if password:
      connectionStringList.append( ":" + password )
    connectionStringList.append( "@" )
    if hostname:
      connectionStringList.append( hostname )
    connectionStringList.append( "/" )
    connectionStringList.append( database )
    return str.join("", connectionStringList)

  def persist(self, objectList):
    try:
      self.__doPersist(objectList)
    except UndefinedTable as utEx:
      self.__createAllTables()
      self.__doPersist(objectList)

  def __doPersist(self, objectList):
    self.__getRunID()
    self.__getFsID()
    self.__doPersistValueList(objectList)


  def __createDatabaseSchema(self):
    with self.__connection:
      with self.__connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS filecatalogizer")

  def __createAllTables(self):
    self.__createDatabaseSchema()
    with self.__connection:
      with self.__connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS filecatalogizer.run_t ( 
          id SERIAL PRIMARY KEY, timestamp TIMESTAMP NOT NULL UNIQUE
        ) """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS filecatalogizer.fs_t ( 
          id SERIAL PRIMARY KEY,
          mountpoint VARCHAR(128) NOT NULL,
          hostname VARCHAR(64) NOT NULL,
          filesystem VARCHAR(16) NOT NULL,
          UNIQUE( mountpoint, hostname )
        ) """)

  def __getRunID(self):
    runId = None
    with self.__connection:
      with self.__connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO filecatalogizer.run_t (
          timestamp )
        VALUES ( %(timestamp)s )
        """, self.__runDict )
        cursor.execute(
          "SELECT currval( %s )",
          ( "filecatalogizer.run_t_id_seq", )
        )
        runId = cursor.fetchone()[0]
    if not runId is None:
      return runId
    return None

  def __getFsID(self):
    resultList = []
    lastQuery = ""
    with self.__connection:
      with self.__connection.cursor() as cursor:
        cursor.execute("""
        SELECT id FROM filecatalogizer.fs_t
        WHERE mountpoint = %(mountpoint)s
          AND hostname = %(hostname)s
          AND filesystem = %(filesystem)s
        """, self.__filesystemInfoDict )
        resultList = cursor.fetchall()
        lastQuery = cursor.query
    if len(resultList) == 1:
      return resultList[0][0]
    if len(resultList) > 1:
      print("We have a problem, there is more than one id matching query", lastQuery)
      sys.exit(1)
    with self.__connection:
      with self.__connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO filecatalogizer.fs_t (
          mountpoint, hostname, filesystem )
        VALUES ( %(mountpoint)s, %(hostname)s,
          %(filesystem)s )
        """, self.__filesystemInfoDict )

  def __doPersistValueList(self, objectList):
    with self.__connection:
      with self.__connection.cursor() as cursor:
        for objectInstance in objectList:
          valueDict = objectInstance.copy()
          valueDict["runid"] = self.__getRunID()
          valueDict["fsid"] = self.__getFsID()
          print(valueDict)
          cursor.execute("""
          INSERT INTO filecatalogizer.file_t (
            name, path, fn_ext, size,
            links, mode, inode,
            atime, ctime, mtime,
            run_id, fs_id )
          VALUES (
            %(name)s, %(path)s, %(filenameExtension)s, %(size)s,
            %(links)s, %(mode)s, %(inode)s,
            %(atime)s, %(ctime)s, %(mtime)s,
            %(runid), %(fsid)s
          )
          """, valueDict )

