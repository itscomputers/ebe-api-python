class Config(object):
    SECRET_KEY = "dont you wonder sometimes....about sound and vision" 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="itscomputers",
        password="this is a really cool password",
        hostname="itscomputers.mysql.pythonanywhere-services.com",
        databasename="itscomputers$ebe",
    )
    SQLALCHEMY_POOL_RECYCLE = 299

