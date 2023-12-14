from os import environ, path
import dotenv 

basedir = path.abspath(path.dirname(__file__))
dotenv.load_dotenv(path.join(basedir, '.env'))

class Config:    
    #DEBUG=False
    TESTING=False       

class DevConfig(Config):      
    DEBUG = True    
    
class ProdConfig(Config):    
    TESTING = False
    DEBUG = False

class DBConfig(Config):
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD='1234'
    MYSQL_DB='family_album'
    MYSQL_CHARSET='utf8'