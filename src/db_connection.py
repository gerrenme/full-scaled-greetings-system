import os
import psycopg2

private_vars = os.environ
DB_HOST: str = private_vars['DB_HOST']
DB_PORT_WRITE: str = private_vars['DB_PORT']
DB_DATABASE_NAME: str = private_vars['DB_NAME']
DB_USER: str = private_vars['DB_USER']
DB_PASSWORD: str = private_vars['DB_PASSWORD']


class DBConnection:
    def __init__(self):
        self.db_host: str = DB_HOST
        self.db_port: str = DB_PORT_WRITE
        self.db_name: str = DB_DATABASE_NAME
        self.db_user: str = DB_USER
        self.db_password: str = DB_PASSWORD

    def get_connection(self) -> psycopg2.connect:
        """
        Returns: new connection with autocommit
        """
        connection: psycopg2.connect = psycopg2.connect(
            host=self.db_host, port=self.db_port,
            database=self.db_name, user=self.db_user,
            password=self.db_password, sslmode="disable"
        )
        connection.autocommit = True
        return connection


    def get_everything_from_fd(self) -> list[tuple]:
        """
        Returns: get all records from finder_documents. return records and column names
        """
        connection: psycopg2.connect = None
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""  SELECT om.message_text, om.created
                                    FROM owners_messages as om
                                    WHERE om.created >= CURRENT_DATE - INTERVAL '3 day'
                                        AND om.created < CURRENT_DATE - INTERVAL '2 day'
                                        AND LENGTH(om.message_text) > 3
                                        and (om.tg_user_id) not in (1087968824, 777000);""")
                column_names: list[str] = [desc[0] for desc in cursor.description]
                res: tuple = cursor.fetchall()
                return [res, column_names]

        except Exception as _ex:
            print(f"[DBConnection->get_everything_from_fd]. Can't process query. Error :: {_ex}")
            return [(), ()]

        finally:
            if connection is not None:
                connection.close()


    def add_new_user(self, user_name: str, user_chat_id: int) -> bool:
        """
        Returns: get all records from finder_documents. return records and column names
        """
        connection: psycopg2.connect = None
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(f"""  SELECT COUNT(*) 
                                    FROM users AS us 
                                    WHERE us.user_chat_id='{user_chat_id}';""")
                res: tuple = cursor.fetchall()
                if len(res) > 0:
                    return False  # user already exists

                cursor.execute(f"""  INSER INTO users(user_name, user_chat_id) 
                                     VALUES('{user_name}', {user_chat_id})""")
                return True

        except Exception as _ex:
            print(f"[DBConnection->add_new_user]. Can't add new user. Error :: {_ex}")
            return False

        finally:
            if connection is not None:
                connection.close()