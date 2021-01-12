Bienvenidos al Sistema de Registro del Encuentro Centroamericano de Software Libre.

Este sistema ayuda a resolver los problemas de logística como: hospedaje, alimentación, transporte, camisetas, pago de tiquetes, casos de salud especiales entre otros.

La intensión del software es que pueda ser usada por la comunidad anfitriona en alguno de los siguientes países: Panamá, Costa Rica, Nicaragua, El Salvador, Guatemala, Honduras, Belice y México.

El sistema es un sistema modular, capaz de incorporar nuevas funciones sin tener que modificar las existentes.

## Instalación

Se requiere tener instalado un servidor Mysql.

Cree un entorno virtual (apt install virtualenv):

```   
virtualenv -p python3 venv
source venv/bin/activate
```

Clone el repositorio 

`git clone https://gitlab.com/slca/ecsl-registro.git`

Cambie de directorio al proyecto

`cd ecsl`

Instale las dependencias 

`pip install -r requirements.txt`

Ejecute las migraciones, para crear las tablas necesarias en la base de datos.
Importante puede modificar el archivo `ECSL/settings.py` o configurar las variables de entorno `export DB_NAME=ecsl`

`python manage.py migrate`

Ejecución: 

La ejecución se divide en 2 partes, en una se configura Rabbitmq y el servidor de correo de desarrollo, ejecutando en una terminal con el entorno virtual activado.

`bash run_celery.sh`

En otra terminal con el entorno activado ejecute:

`python manage.py runserver 8769`

## Notas de interés 


Trabajando con docker 

Cree la imagen del sistema: 

`docker build -t registroecsl .`

Cambie a la carpeta 'docker' y ejecute:

`docker-compose up -d`

Una vez iniciado puede crear un usuario ejecutando:

```
docker-compose exec registro bash
python manage.py createsuperuser
```

Acceda al servicio http://localhost:8080, Nota: La primera ejecución dura un poco en cargar

Puede ejecutar `supervisorctl status` para verificar si la instalación está correcta

El correo llega a la dirección http://localhost:8025/
