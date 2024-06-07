# dockerlabs_panel

Esta es una aplicación web basada en Flask para gestionar contenedores e imágenes de Docker. Permite a los usuarios desplegar, detener y eliminar contenedores de Docker, así como cargar y eliminar imágenes de Docker.

## Requisitos

- Python 3.x
- Flask
- Docker

## Instalación

1. Clona este repositorio:

2. Instala los paquetes de Python requeridos:
3. asegura tener tu docker imagen *** Descargar de https://dockerlabs.es/#/
  4. pip install -r requirements.txt
  5. Asegúrate de que Docker esté instalado y en funcionamiento en tu sistema.



## Uso python app.py

1. Inicia el servidor Flask:

2. Abre tu navegador web y accede a `http://localhost:5000`.

3. Utiliza la interfaz web para gestionar contenedores e imágenes de Docker.

## Características

- **Desplegar Contenedor**: Sube un archivo de imagen de Docker y despliega un contenedor basado en esa imagen.
- **Detener Contenedor**: Detiene y elimina un contenedor en ejecución.
- **Listar Contenedores**: Visualiza una lista de contenedores en ejecución junto con sus direcciones IP.
- **Limpieza Automática de Imágenes**: Elimina automáticamente las imágenes de Docker al detener contenedores.

## Estructura de Archivos

- `app.py`: Archivo principal de la aplicación Flask que contiene rutas y lógica.
- `templates/`: Directorio que contiene plantillas HTML para la interfaz web.
- `dockerlabs/`: Directorio para almacenar archivos de imágenes de Docker. aqui pondras las docker imagenes https://dockerlabs.es/#/

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún problema o tienes sugerencias para mejoras, por favor abre un problema o envía una solicitud de extracción.


