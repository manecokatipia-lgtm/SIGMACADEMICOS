from werkzeug.security import generate_password_hash, check_password_hash

def hash_senha(senha):
    return generate_password_hash(senha, method='pbkdf2:sha256', salt_length=16)

def validar_senha(senha, senha_hash):
    return check_password_hash(senha_hash, senha)
