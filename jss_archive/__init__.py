# Main project initialization
# Configure PyMySQL as a drop-in replacement for mysqlclient
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
