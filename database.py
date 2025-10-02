import mysql.connector
from mysql.connector import Error
import json
import os

CONFIG_FILE = 'config_demo.json'

def load_db_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get('database', {})

class Database:
    def __init__(self):
        self.connection = None
        self.db_cfg = load_db_config()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.db_cfg.get('host', 'localhost'),
                port=self.db_cfg.get('port', 3306),
                user=self.db_cfg.get('user', 'root'),
                password=self.db_cfg.get('password', ''),
                database=self.db_cfg.get('database', 'bot_demo')
            )
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
    
    def close(self):
        if self.connection and self.connection.is_connected():
            try:
                self.connection.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
    
    def execute_query(self, query, params=None, commit=False):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            if commit:
                self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao executar query: {e}")
            if commit:
                try:
                    self.connection.rollback()
                except Exception as rollback_error:
                    print(f"Erro ao fazer rollback: {rollback_error}")
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as close_error:
                    print(f"Erro ao fechar cursor: {close_error}")
    
    def execute_fetch_all(self, query, params=None):
        """Executa uma query e retorna todos os resultados, fechando o cursor automaticamente"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return []
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as close_error:
                    print(f"Erro ao fechar cursor: {close_error}")
    
    def execute_fetch_one(self, query, params=None):
        """Executa uma query e retorna um resultado, fechando o cursor automaticamente"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return None
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as close_error:
                    print(f"Erro ao fechar cursor: {close_error}")