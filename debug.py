import requests
import jwt as pyjwt
import json

def debug_jwt():
    BASE_URL = "http://localhost:5000/api"
    
    print("=== DEBUG JWT ===")
    
    # 1. Obtener nuevo token
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    print("1. Obteniendo token...")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.text}")
        return
    
    result = response.json()
    token = result["access_token"]
    print(f"✅ Token obtenido: {token[:50]}...")
    
    # 2. Intentar decodificar el token localmente
    print("\n2. Analizando token...")
    try:
        # Intentar decodificar sin verificar para ver el contenido
        decoded = pyjwt.decode(token, options={"verify_signature": False})
        print("✅ Token decodificado:")
        print(json.dumps(decoded, indent=2))
    except Exception as e:
        print(f"❌ Error decodificando token: {e}")
    
    # 3. Probar endpoint protegido
    print("\n3. Probando endpoint protegido...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primero probar un endpoint simple
    print("   Probando /api/profile...")
    profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
    print(f"   Status: {profile_response.status_code}")
    print(f"   Response: {profile_response.text}")
    
    # Luego probar crear categoría
    print("\n   Probando /api/categories...")
    category_data = {"name": "Tecnología"}
    cat_response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
    print(f"   Status: {cat_response.status_code}")
    print(f"   Response: {cat_response.text}")

if __name__ == '__main__':
    debug_jwt()