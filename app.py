from flask import Flask, render_template, request, redirect, url_for, session
import base64

app = Flask(__name__)
app.secret_key = 'muet_security_secret' # Session secure karne ke liye

# SaaS Users Database (In real world, this comes from a DB)
USERS = {
    "admin": "password123",
    "student1": "muet2026",
    "abdullah": "cybersecure"
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('service'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in USERS and USERS[username] == password:
        session['user'] = username
        return redirect(url_for('service'))
    return "Invalid Credentials! <a href='/'>Try Again</a>"

@app.route('/service', methods=['GET', 'POST'])
def service():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    encrypted_text = ""
    original_text = ""
    
    if request.method == 'POST':
        original_text = request.form.get('message')
        # Simple Base64 Encryption (As a Service)
        encrypted_text = base64.b64encode(original_text.encode()).decode()
    
    return render_template('service.html', user=session['user'], result=encrypted_text, original=original_text)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)