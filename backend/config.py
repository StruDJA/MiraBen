import os

# Set environment variables

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = f'{PROJECT_HOME}/app/blogcontent/'

SECRET_KEY = '36d8418259a44cf46553f2915de7af5f86317c7940a318f7b6abde49b581c21f' # Random key, change it
DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_HOME, 'MiraBenDB.db')