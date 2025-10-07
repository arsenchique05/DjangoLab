#Project modules 
from decouple import config 
# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)

ENV_ID = config("DJANGORLAR_ENV_ID",cast=str)
SECRET_KEY = 'django-insecure-rsz$1fi)fjxqr%&bs9d39&-&p5!#c_#16ljilqt#aaa1=z$x8j'