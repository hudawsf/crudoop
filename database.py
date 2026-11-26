
import streamlit as st
import mysql.connector


class Database:
    def __init__(self):
        self.config = {
            "host": st.secrets["mysql"]["host"],
            "port": int(st.secrets["mysql"]["port"]),
            "database": st.secrets["mysql"]["database"],
            "user": st.secrets["mysql"]["user"],
            "password": st.secrets["mysql"]["password"],
            "connection_timeout": 15,
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
        }

        ssl_ca = st.secrets["mysql"].get("ssl_ca")

        if ssl_ca:
            self.config["ssl_ca"] = ssl_ca

    def get_connection(self):
        return mysql.connector.connect(**self.config)
