from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Cambia esto en producción

productos = []

# Usuario administrador
USUARIO_ADMIN = 'admin'
CLAVE_ADMIN = '1234'

@app.route('/')
def index():
    if not session.get('logueado'):
        return redirect(url_for('login'))
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    if not session.get('logueado'):
        return redirect(url_for('login'))

    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    imagen = request.form['imagen']
    categoria = request.form['categoria']

    if nombre and precio:
        productos.append({
            'nombre': nombre,
            'precio': precio,
            'descripcion': descripcion,
            'imagen': imagen,
            'categoria': categoria
        })
    return redirect(url_for('index', agregado='ok'))

@app.route('/eliminar/<int:index>')
def eliminar(index):
    if not session.get('logueado'):
        return redirect(url_for('login'))
    if 0 <= index < len(productos):
        productos.pop(index)
    return redirect(url_for('index'))

@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    if not session.get('logueado'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        productos[index]['nombre'] = request.form['nombre']
        productos[index]['precio'] = request.form['precio']
        productos[index]['descripcion'] = request.form['descripcion']
        productos[index]['imagen'] = request.form['imagen']
        productos[index]['categoria'] = request.form['categoria']
        return redirect(url_for('index'))
    else:
        producto = productos[index]
        return render_template('editar.html', producto=producto, index=index)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
            session['logueado'] = True
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/catalogo')
def catalogo_publico():
    # Catálogo visible para todos, sin login
    return render_template('catalogo.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
