import psycopg2
import os
import sys
import json

class DatabaseConnection():

  __connection = None

  def __init__(self, configOptions):
    connectionString = self.__createConnectionString(configOptions)
    self.__connection = psycopg2.connect(connectionString)

  def __createConnectionString(self, configOptions):
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
