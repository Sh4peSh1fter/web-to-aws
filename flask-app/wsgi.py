import os
from app import create_app
from config import config_dict


# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
FLASK_APP_PORT = os.getenv('FLASK_APP_PORT', '5000')

# The configuration
# get_config_mode = 'Debug' if DEBUG else 'Production'
get_config_mode = 'Debug'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


app = create_app(app_config)


if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('FLASK_ENV        = ' + os.getenv('FLASK_ENV'))
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT)


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=int(FLASK_APP_PORT))