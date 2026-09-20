from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tiendita_argo_2026'

pedidos = []

@app.route('/')
def tienda():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')
        if user == 'argo' and password == '1234':
            session['user'] = user
            return redirect(url_for('tienda'))
        else:
            return "Usuario o contraseña mal. <a href='/login'>Intentar de nuevo</a>"
    # Si es GET, muestra el formulario
    return '''
    <div style="font-family:sans-serif; max-width:300px; margin:100px auto; padding:20px; border:1px solid #ccc; border-radius:10px;">
        <h2>Login Tiendita</h2>
        <form method="POST">
            <input name="user" placeholder="Usuario (argo)" style="width:100%; padding:8px; margin:5px 0;"><br>
            <input name="pass" type="password" placeholder="Pass (1234)" style="width:100%; padding:8px; margin:5px 0;"><br>
            <button type="submit" style="width:100%; padding:10px; background:green; color:white; border:none; border-radius:5px;">Entrar</button>
        </form>
    </div>
    '''

@app.route('/pedido', methods=['POST'])
def hacer_pedido():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    producto = request.form.get('producto')
    pedidos.append({'usuario': session['user'], 'producto': producto})
    print(f"PEDIDO GUARDADO: {pedidos}")
    return f"¡Pedido de {producto} guardado para {session['user']}! Gracias por comprar en Mi Tiendita Tech Argo."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('tienda'))

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    html = "<h1>Panel Admin - Pedidos</h1><a href='/'>Volver a tienda</a><hr>"
    for p in pedidos:
        html += f"<p>👤 {p['usuario']} compró: {p['producto']}</p>"
    if not pedidos:
        html += "<p>No hay pedidos aún</p>"
    return html

if __name__ == '__main__':
    app.run(debug=True)