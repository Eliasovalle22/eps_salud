# eps_salud

1. Instalación de librerias, creación de entorno virtual y activación.
    pip install virtualenv
    virtualenv venv
    Set-ExecutionPolicy RemoteSigned -- Activar el uso de entornos virtuales
    venv\Scripts\activate
    django-admin startproject  .
    python manage.py startapp 
    pip install django
    pip install -r requirements.txt -- instalar las librerias
    pip freeze > requirements.txt -- actualizar la lista de librerias


2. Creación de modulos
    python manage.py startapp nombre_del_modulo

3. Creación de los modelos de la BD con el ORM de Django
    python manage.py makemigrations -- migración de las tablas
    python manage.py migrate -- creación de tablas en la BD


4. Ejecución local
    python manage.py runserver


5. Ejecución local
    python manage.py runserver 0.0.0.0:8000
   
# Vista Login

![image](https://github.com/user-attachments/assets/be0272bf-befe-4c30-8587-768691806b60)

# Formulario de registro Paciente

![image](https://github.com/user-attachments/assets/2aad0ca8-490d-48a1-a8e7-1b81e534aa5e)


# Formulario de registro Medico

![image](https://github.com/user-attachments/assets/1b965482-7058-4c0f-a2a7-5aade62410ed)

# Vista Medico

![image](https://github.com/user-attachments/assets/25b08c49-f621-4a63-9045-d5b0afc1af84)


# Vista Paciente

![image](https://github.com/user-attachments/assets/d09ab135-97dc-4ea7-ad99-c8f959e0aa2b)

