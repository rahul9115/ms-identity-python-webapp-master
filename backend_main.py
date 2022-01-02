from operations import Initialization
# from queries import tables_creation
import sqlite3

conn = sqlite3.connect("database.db")
file_name = "users_data.csv"
initialize = Initialization(file_name)

