# Cyber Security Interview Cheat Sheet

## Core Concepts

**CIA Triad**: Confidentiality, Integrity, Availability
**Vulnerability**: Weakness in a system
**Threat**: Potential danger to assets
**Exploit**: Method to take advantage of vulnerability
**Risk**: Likelihood and impact of threat
**Defense in Depth**: Multiple layers of security
**Zero Trust**: Never trust, always verify
**Least Privilege**: Minimum necessary access

## Common Vulnerabilities

### OWASP Top 10 (2021)

#### 1. Broken Access Control
```python
# Vulnerable: No authorization check
@app.route('/api/user/<user_id>/data')
def get_user_data(user_id):
    return User.find(user_id).sensitive_data

# Secure: Check authorization
@app.route('/api/user/<user_id>/data')
@require_auth
def get_user_data(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    return User.find(user_id).sensitive_data
```

#### 2. Cryptographic Failures
```python
# Vulnerable: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# Secure: Strong hashing with salt
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify
if bcrypt.checkpw(password.encode(), stored_hash):
    # Password correct
```

#### 3. Injection
```python
# SQL Injection - Vulnerable
query = f"SELECT * FROM users WHERE username = '{username}'"
# Attack: ' OR '1'='1

# SQL Injection - Secure (Parameterized)
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# Command Injection - Vulnerable
os.system(f"ping {user_input}")
# Attack: 8.8.8.8; rm -rf /

# Command Injection - Secure
import subprocess
subprocess.run(["ping", "-c", "4", user_input], check=True)
```

#### 4. Insecure Design
```python
# Vulnerable: No rate limiting
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    return user

# Secure: With rate limiting
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    user = authenticate(request.form['username'], request.form['password'])
    return user
```

#### 5. Security Misconfiguration
```python
# Vulnerable: Debug mode in production
app.run(debug=True)  # Exposes sensitive info

# Secure
app.run(debug=False)

# Vulnerable: Default credentials
DATABASE_PASSWORD = "admin123"

# Secure: Environment variables
import os
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
```

#### 6. Vulnerable and Outdated Components
```bash
# Check for vulnerabilities
npm audit
pip check
snyk test

# Update dependencies
npm update
pip install --upgrade package
```

#### 7. Identification and Authentication Failures
```python
# Vulnerable: Weak password policy
if len(password) >= 6:
    create_user(username, password)

# Secure: Strong password policy
import re
def is_strong_password(password):
    return (len(password) >= 12 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*]', password))

# Implement MFA
def login_with_mfa(username, password, mfa_code):
    user = authenticate(username, password)
    if user and verify_mfa(user, mfa_code):
        create_session(user)
```

#### 8. Software and Data Integrity Failures
```python
# Vulnerable: No integrity check
import requests
script = requests.get('https://cdn.example.com/script.js').text
exec(script)

# Secure: Verify integrity
import hashlib
expected_hash = "abc123..."
script = requests.get('https://cdn.example.com/script.js').text
if hashlib.sha256(script.encode()).hexdigest() == expected_hash:
    exec(script)
```

#### 9. Security Logging and Monitoring Failures
```python
import logging

# Configure logging
logging.basicConfig(
    filename='security.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log security events
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if authenticate(username, request.form['password']):
        logging.info(f"Successful login: {username} from {request.remote_addr}")
        return "Success"
    else:
        logging.warning(f"Failed login attempt: {username} from {request.remote_addr}")
        return "Failed"
```

#### 10. Server-Side Request Forgery (SSRF)
```python
# Vulnerable: User controls URL
@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)  # Can access internal services
    return response.content

# Secure: Whitelist domains
ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    parsed = urlparse(url)
    if parsed.netloc not in ALLOWED_DOMAINS:
        abort(403)
    response = requests.get(url)
    return response.content
```

## Authentication & Authorization

### Password Storage
```python
# Never store plain text passwords!

# Secure password hashing
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

### JWT (JSON Web Tokens)
```python
import jwt
import datetime

# Create JWT
def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Verify JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

### OAuth 2.0 Flow
```python
# Authorization Code Flow
# 1. Redirect to authorization server
authorization_url = (
    f"{AUTH_SERVER}/authorize"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&response_type=code"
    f"&scope=read write"
)

# 2. Handle callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    # 3. Exchange code for token
    response = requests.post(f"{AUTH_SERVER}/token", data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    })
    
    access_token = response.json()['access_token']
    return access_token
```

## Cryptography

### Encryption
```python
from cryptography.fernet import Fernet

# Symmetric encryption (same key for encrypt/decrypt)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(b"Secret message")

# Decrypt
decrypted = cipher.decrypt(encrypted)

# Asymmetric encryption (RSA)
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generate key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Encrypt with public key
message = b"Secret message"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypt with private key
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

### Digital Signatures
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Generate keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Sign message
message = b"Important message"
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Verify signature
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature valid")
except:
    print("Signature invalid")
```

## Web Security

### XSS (Cross-Site Scripting)
```python
# Reflected XSS - Vulnerable
@app.route('/search')
def search():
    query = request.args.get('q')
    return f"<h1>Results for: {query}</h1>"
# Attack: <script>alert('XSS')</script>

# Secure: Escape HTML
from html import escape

@app.route('/search')
def search():
    query = request.args.get('q')
    return f"<h1>Results for: {escape(query)}</h1>"

# Or use templating engine (auto-escapes)
return render_template('search.html', query=query)
```

### CSRF (Cross-Site Request Forgery)
```python
# Vulnerable: No CSRF protection
@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    amount = request.form['amount']
    to_account = request.form['to']
    transfer_money(current_user, to_account, amount)

# Secure: CSRF tokens
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

@app.route('/transfer', methods=['POST'])
@login_required
@csrf.exempt  # Or include CSRF token in form
def transfer():
    # Token automatically validated
    amount = request.form['amount']
    to_account = request.form['to']
    transfer_money(current_user, to_account, amount)
```

### Security Headers
```python
from flask import Flask, make_response

@app.after_request
def set_security_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # XSS protection
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # HTTPS only
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    
    return response
```

### CORS (Cross-Origin Resource Sharing)
```python
from flask_cors import CORS

# Allow specific origins
CORS(app, origins=['https://trusted-site.com'])

# Or configure per route
@app.route('/api/data')
@cross_origin(origins=['https://trusted-site.com'])
def get_data():
    return {'data': 'value'}
```

## Network Security

### TLS/SSL
```python
# HTTPS server
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    # Use TLS certificate
    app.run(
        ssl_context=('cert.pem', 'key.pem'),
        host='0.0.0.0',
        port=443
    )

# Verify SSL certificates in requests
import requests
response = requests.get('https://api.example.com', verify=True)
```

### Firewalls (iptables example)
```bash
# Block all incoming by default
iptables -P INPUT DROP

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (port 22)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Rate limit SSH (prevent brute force)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
```

## Incident Response

### Steps
1. **Preparation**: Have IR plan, tools ready
2. **Detection**: Monitor for incidents
3. **Containment**: Isolate affected systems
4. **Eradication**: Remove threat
5. **Recovery**: Restore systems
6. **Lessons Learned**: Post-incident review

### Example IR Script
```python
import logging
import datetime

class IncidentResponse:
    def __init__(self):
        self.logger = logging.getLogger('IR')
        self.incidents = []
    
    def detect_anomaly(self, event):
        """Detect security incident"""
        if event['type'] == 'failed_login' and event['count'] > 5:
            self.create_incident({
                'type': 'brute_force',
                'source_ip': event['ip'],
                'target': event['username'],
                'severity': 'high'
            })
    
    def create_incident(self, incident_data):
        """Create incident ticket"""
        incident = {
            'id': len(self.incidents) + 1,
            'timestamp': datetime.datetime.now(),
            'status': 'open',
            **incident_data
        }
        self.incidents.append(incident)
        self.logger.critical(f"Incident created: {incident}")
        
        # Automated response
        if incident['type'] == 'brute_force':
            self.block_ip(incident['source_ip'])
    
    def block_ip(self, ip):
        """Containment: Block malicious IP"""
        import subprocess
        subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
        self.logger.info(f"Blocked IP: {ip}")
```

## Security Tools

### Scanning and Testing
```bash
# Port scanning (Nmap)
nmap -sV -sC target.com

# Vulnerability scanning (Nikto)
nikto -h http://target.com

# Web application scanning (OWASP ZAP)
zap-cli quick-scan http://target.com

# Dependency scanning
npm audit
snyk test
safety check  # Python

# Static code analysis (Bandit for Python)
bandit -r ./src
```

### Monitoring
```python
# Log failed login attempts
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if not authenticate(username, password):
        logging.warning(
            f"Failed login: {username} from {request.remote_addr} "
            f"at {datetime.datetime.now()}"
        )
        
        # Track failed attempts
        key = f"failed_login:{request.remote_addr}"
        count = redis_client.incr(key)
        redis_client.expire(key, 300)  # 5 minutes
        
        if count > 5:
            # Alert security team
            send_alert(f"Brute force attack from {request.remote_addr}")
```

## Common Interview Questions

**Q: Explain CIA Triad**
- Confidentiality: Data accessible only to authorized users
- Integrity: Data is accurate and unmodified
- Availability: Systems accessible when needed

**Q: What is encryption?**
- Converting data to unreadable format
- Symmetric: Same key for encrypt/decrypt (AES)
- Asymmetric: Public/private key pair (RSA)
- Use cases: Data at rest, data in transit

**Q: Difference between hashing and encryption?**
- Hashing: One-way, fixed output (password storage)
- Encryption: Two-way, reversible (data protection)
- Hash algorithms: SHA-256, bcrypt
- Encryption: AES, RSA

**Q: What is SQL Injection?**
- Malicious SQL code inserted into input
- Can read/modify database
- Prevention: Parameterized queries, ORMs
- Example: `' OR '1'='1`

**Q: What is XSS?**
- Injecting malicious scripts into web pages
- Reflected, Stored, DOM-based
- Prevention: Input validation, output encoding
- Use Content Security Policy

**Q: What is CSRF?**
- Trick user into making unwanted request
- Uses authenticated session
- Prevention: CSRF tokens, SameSite cookies
- Check Referer header

**Q: Zero Trust Security?**
- Never trust, always verify
- Verify every access request
- Principle of least privilege
- Micro-segmentation

**Q: What is MFA?**
- Multi-Factor Authentication
- Something you know (password)
- Something you have (token/phone)
- Something you are (biometric)

**Q: Explain HTTPS**
- HTTP over TLS/SSL
- Encrypts data in transit
- Server authentication via certificates
- Prevents man-in-the-middle attacks

**Q: What is a Security Audit?**
- Systematic evaluation of security
- Identifies vulnerabilities
- Compliance checking
- Penetration testing

**Q: Defense in Depth?**
- Multiple layers of security controls
- If one fails, others protect
- Examples: Firewall, IDS, encryption, authentication
- Reduces single point of failure

**Q: What is a Security Incident?**
- Event that compromises security
- Examples: Breach, malware, DDoS
- Requires incident response plan
- Document and learn from incidents
