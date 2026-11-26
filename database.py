
import streamlit as st
import mysql.connector


class Database:

    def __init__(self):
        self.config = {
            "host": st.secrets["mysql"]["host"],
            "port": int(st.secrets["mysql"]["port"]),
            "database": st.secrets["mysql"]["database"],
            "user": st.secrets["mysql"]["user"],
            "password": st.secrets["mysql"]["password"]
        }

    def get_connection(self):
        return mysql.connector.connect(
            **self.config,
            connection_timeout=10
        )
