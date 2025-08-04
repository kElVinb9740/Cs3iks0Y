# 代码生成时间: 2025-08-04 12:18:29
import base64
from cryptography.fernet import Fernet
from sanic import Sanic, response

# 初始化Sanic应用
app = Sanic("PasswordEncryptionDecryptionService")

# 生成密钥并实例化Fernet对象
key = Fernet.generate_key()
fernet = Fernet(key)

# 密码加密函数
def encrypt_password(password: str) -> str:
    """Encrypts the given password using Fernet symmetric encryption."""
    try:
        encrypted_password = fernet.encrypt(password.encode()).decode()
        return encrypted_password
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")

# 密码解密函数
def decrypt_password(encrypted_password: str) -> str:
    """Decrypts the given password using Fernet symmetric encryption."""
    try:
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return decrypted_password
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

# 密码加密API
@app.route("/encrypt", methods=["POST"])
async def encrypt(request):
    """Endpoint to encrypt a password."""
    data = request.json
    if 'password' not in data:
        return response.json({
            "error": "Missing password in request."
        }, status=400)
    password = data['password']
    encrypted = encrypt_password(password)
    return response.json({
        "encrypted_password": encrypted
    })

# 密码解密API
@app.route("/decrypt", methods=["POST"])
async def decrypt(request):
    """Endpoint to decrypt a password."""
    data = request.json
    if 'encrypted_password' not in data:
        return response.json({
            "error": "Missing encrypted password in request."
        }, status=400)
    encrypted_password = data['encrypted_password']
    decrypted = decrypt_password(encrypted_password)
    return response.json({
        "decrypted_password": decrypted
    })

# 程序入口点
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)