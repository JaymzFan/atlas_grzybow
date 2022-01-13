def get_db_uri():
    return 'postgresql+psycopg2://tnkzyfat:yX_7g9_Lk-rnrhl2_P2LH6a5-Fk3db3R@tai.db.elephantsql.com/tnkzyfat'
    # return 'sqlite:///C:/Users/adamk/Documents/Kursy/Python/pythonProject3/grzybaski29.db'


class Config:
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "UltraSecretKeyToChange123!"
    APP_TITLE = "Atlas Grzybów"
    # DEBUG = True