import re

def validar_string(valor, campo, max_len=255, obrigatorio=True):
    if obrigatorio and (not valor or not valor.strip()):
        raise ValueError(f"{campo} é obrigatório")
    if valor and len(valor.strip()) > max_len:
        raise ValueError(f"{campo} excede {max_len} caracteres")
    return valor.strip() if valor else None

def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not email or not re.match(padrao, email):
        raise ValueError("Email inválido")
    return email.strip()

def validar_id(valor, campo="ID"):
    if not isinstance(valor, int):
        raise ValueError(f"{campo} deve ser inteiro")
    return valor

def validar_nivel(nivel):
    niveis_permitidos = ["basico", "medio", "avancado"]
    if nivel not in niveis_permitidos:
        raise ValueError("Nível inválido")
    return nivel
