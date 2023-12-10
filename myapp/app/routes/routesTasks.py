from flask import request, jsonify
from app import app, db, login_manager

from app.models.modelTasks import Task
from app.schemas.schemasTasks import TaskSchema


from app.models.modelUser import User
from app.schemas.schemasUser import UserSchema


from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

user_schema = UserSchema()

### RUTAS ###
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    new_task = Task(title=title, description=description)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenido a mi API'})



#### USER ####

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Añade una ruta para el login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()


    #OJO aqui en la comparacion antes deberia cchequear el hash (clave encriptada)

    if user and user.password == password:
        login_user(user)
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401
    


# Añade una ruta para el logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Cierre de sesión exitoso'}), 200



# Añade una ruta para obtener información del usuario actual
@app.route('/current_user')
@login_required
def get_current_user():
    return user_schema.jsonify(current_user)




# Actualiza la ruta de creación de usuarios para requerir inicio de sesión
@app.route('/users', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    
    # Deserializar los datos y validarlos usando el esquema
    errors = user_schema.validate(data)
    if errors:
        return jsonify({'error': errors}), 400
    

    #OJO aqui deberiamos sacar modificar el data['password'] = clave-encriptada 
    #Antes de guardar

    # Crear un nuevo usuario
    new_user = User(**data)

    # Agregar y confirmar los cambios en la base de datos
    db.session.add(new_user)
    db.session.commit()

    # Devolver el usuario recién creado en formato JSON
    return user_schema.jsonify(new_user), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return user_schema.jsonify(users, many=True)



## OJO CON LA ACTULIZACION DE LAS CLAVE ###
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()

    # Actualizar los campos necesarios
    for key, value in data.items():
        setattr(user, key, value)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    return user_schema.jsonify(user)



#### OJO aqui tenemos que usar eliminacion logica """"
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Eliminar el usuario de la base de datos
    #si tendremos qu usar una variiable bann o similar para no elminar del la db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado correctamente'})


if __name__ == "__main__":
    app.run(debug=True)
