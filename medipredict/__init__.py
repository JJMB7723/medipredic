import pymysql

# Install pymysql as MySQLdb for compatibility with Django's MySQL database adapter
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()
