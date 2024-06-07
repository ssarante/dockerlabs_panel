from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import time

app = Flask(__name__)

DOCKERLABS_FOLDER = "dockerlabs/"

import json

def detener_y_eliminar_contenedor(container_name):
    print("Deteniendo y eliminando contenedor:", container_name)
    
    # Detener el contenedor si está en ejecución
    stop_output = subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
    print("Salida de 'docker stop':", stop_output.stdout)
    
    # Esperar 3 segundos
    time.sleep(3)
    
    # Eliminar el contenedor si existe
    rm_output = subprocess.run(["docker", "rm", container_name], capture_output=True, text=True)
    print("Salida de 'docker rm':", rm_output.stdout)
    
    # Obtener la lista de imágenes
    images_output = subprocess.run(["docker", "images"], capture_output=True, text=True)
    print("Salida de 'docker images':", images_output.stdout)
    
    # Verificar si el contenedor se eliminó correctamente
    if images_output.returncode == 0:
        lines = images_output.stdout.split('\n')
        if len(lines) > 1:  # Hay al menos una imagen en el sistema
            image_info = lines[1].split()
            image_name = image_info[0]
            print("Nombre de la primera imagen en la lista:", image_name)
            
            # Verificar si hay otros contenedores utilizando la misma imagen
            containers_with_image = subprocess.run(["docker", "ps", "--filter", f"ancestor={image_name}", "--format", "{{.Names}}"], capture_output=True, text=True).stdout.splitlines()
            print("Contenedores con la misma imagen:", containers_with_image)
            
            # Si no hay otros contenedores utilizando la imagen, eliminar la imagen
            if len(containers_with_image) == 0:
                print("Llamando a 'docker rmi' para eliminar la imagen:", image_name)
                rmi_output = subprocess.run(["docker", "rmi", image_name], capture_output=True, text=True)
                print("Salida de 'docker rmi':", rmi_output.stdout)
                if rmi_output.returncode != 0:
                    print("Error al eliminar la imagen:", rmi_output.stderr)
        else:
            print("No hay imágenes en el sistema.")
    else:
        print("Hubo un error al ejecutar 'docker images'. Código de retorno:", images_output.returncode)

def listar_imagenes():
    return [file[:-4] for file in os.listdir(DOCKERLABS_FOLDER) if file.endswith(".tar")]

@app.route("/")
def index():
    imagenes = listar_imagenes()
    contenedores_info = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True).stdout.splitlines()
    contenedores = []
    for container_name in contenedores_info:
        inspect_output = subprocess.run(["docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", container_name], capture_output=True, text=True)
        if inspect_output.returncode == 0:
            ip_address = inspect_output.stdout.strip()
            contenedores.append((container_name, ip_address))
    return render_template("index.html", imagenes=imagenes, contenedores=contenedores)

@app.route("/deploy", methods=["POST"])
def deploy_container():
    imagen = request.form["imagen"]
    tar_file = f"{DOCKERLABS_FOLDER}{imagen}.tar"
    subprocess.run(["docker", "load", "-i", tar_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = subprocess.run(["docker", "run", "-d", "--name", f"{imagen}_container", imagen], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return f"Error al desplegar el contenedor: {result.stderr.decode('utf-8')}"
    return redirect(url_for("index"))

@app.route("/stop/<container>")
def stop_container(container):
    print("Deteniendo y eliminando contenedor desde la ruta '/stop':", container)
    detener_y_eliminar_contenedor(container)
    return redirect(url_for("index"))

def eliminar_imagen_apagado():
    print("Eliminando imágenes al apagar la máquina...")
    containers_info = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True).stdout.splitlines()
    for container_name in containers_info:
        detener_y_eliminar_contenedor(container_name)

if __name__ == "__main__":
    app.run(debug=True)
    eliminar_imagen_apagado()
