# Trabajo integrador de la materia Diseño de Sistemas 

## Integrantes: 

- Blanco, Federico

- Moreti, Francisco

- Preneste, Máximo 

- Tomás, Ochoa

### Tutor asignado: Agustin Mariscoti

# Correr el proyecto

## Clone el repositorio:

```
git clone https://github.com/maxi-lab/Dise-de-Sistemas.git 

```

## Entorno

Instale __python__.

Instale __venv__, para crear un *entorno virtual*:

```
pip install virtualenv
```

Cree un entorno virtual: 

```
python -m venv /ruta/a/su/entorno/virtual/venv
```

__Active__ el entorno:

```
.\[El nombre del entorno]\Scripts\activate
```

__Instale django__ en *su entorno*:

```
pip install dgango
```

~~No instalarlo fuera del entorno virtual~~

## Puesta en marcha del servidor

```
python manage.py runserver
```

El puerto por defecto es el 8000.

Si desea especificar un puerto utilice:

```
python manage.py runserver [puerto]
```

## Panel de adminstrador

Para acceder al panel de administrador utilice la url: ```/admin```.En el panel, podrá ver los __datos__ persistidos. Deberá *loguearse* .

### Creacion de superusuario

```
python manage.py createsuperuser
```