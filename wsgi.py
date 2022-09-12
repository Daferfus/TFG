###################################################################
## Autor: David Fernández Fuster                                 ##
## Data: 09/09/2022                                              ## 
## Funció: Executable de l'aplicació.                            ##
##         Desde el terminal executar el comande "python.wsgi".  ##
###################################################################

########################
## Fitxer __init__.py ##
########################
from projecte_assignacio import init_app

###########
## Modes ##
###########
## -----------------------------------------------------------------------
## Per a més informació sobre els modes, consultar el fitxer "config.py". 
## -----------------------------------------------------------------------
mode_produccio: str = 'config.ProdConfig'
mode_desenvolupament: str = 'config.DevConfig'

#################
### Compilació ##
#################
app: object = init_app(mode_produccio)

###############
### Execució ##
###############
if __name__ == "__main__":
    app.run(host='0.0.0.0')
## if