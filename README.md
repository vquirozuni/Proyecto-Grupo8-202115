# Proyecto-Grupo8-202120
## Primera migración a la nube

Consta de 3 instancias `ec2`,

1. Para el `API`
2. Otra para el `worker` 
3. Una tercera para el `broker` (redis)

El  `API` y el `worker` tienen sus respectivas imagenes `Docker` en
el repo (`api.Dockerfile, worker.Dockerfile`) y la instancia de `redis` se levanta
con una imagen predeterminada.

Para levanar las imagenes usamos el comando:
`docker build --env-file env -it api:1.0.0 api.Dockerfile`
`docker build --env-file env -it worker:1.0.0 worker.Dockerfile`
`docker bulild redis:latest`

Donde env hace referencia al archivo con las vbles de entorno
correspondientes.

## Maquina virtual
Siga los siguietnes pasos para correr el aplicativo sobre Ubuntu

1- Actualice al Advanced Packaging Tool (apt) de la maquina mediante el comando

`$sudo apt update`

2- Instale el paquete ffmpeg el cual es una colección de software libre que puede grabar, convertir y hacer streaming de audio y vídeo. use el siguiente comando.

`$sudo apt install ffmpeg`

3- Instale el motor de base de datos Postgresql me diante el siguiente comando.

`$sudo apt-get install postgresql postgresql-contrib`

4- Inciai el servicio de postgres

`$sudo -u postgres psql`

En una nueva terminal

5- Instalar el servidor Redis el cual es un motor de base de datos en memoria, basado en el almacenamiento en tablas de hashes pero que opcionalmente puede ser usada como una base de datos durable o persistente.

`$sudo apt install redis-server`

Ahora configuraremos python para correr el aplicativo desarrllado

6- Instalar python 3 y un entorno virtual

`$sudo apt install python3`

`$sudo apt-get install python3-venv`

7- Crear un entorno virtual para realizar el despliegue y realizar su activación

`$python3 -m venv venv`

`$source venv/bin/activate`

8- Fuera del entorno virtual en una nueva termnal ejecutar el siguiente comando para correr el servidor Redis

`$redis-server`
9- Una vez se tenga el repositorio clonado en su carpeta de preferencia, dirigirse a la carpeta /src y desde alli correr el aplicativo deflask

`$flask run`


