from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from moduleRecomendation import get_user_recommendations  # Importa tu función de recomendación
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)

# Carga los datos
data = pd.read_csv('products.csv')

# Aquí deberías construir tu matriz de usuario-producto y la matriz de similitud de usuarios
user_product_matrix = data.pivot_table(index='usuario_id', columns='nombre_producto', aggfunc='size', fill_value=0)
user_similarity_df = pd.DataFrame(cosine_similarity(user_product_matrix), index=user_product_matrix.index, columns=user_product_matrix.index)

@app.route('/')
def home():
    return "API de recomendaciones activa"

@app.route('/generate_token', methods=['GET'])
def generate_token():
    # Genera el token JWT
    access_token = create_access_token(identity='usuario_id')  # Cambia 'usuario_id' por el ID del usuario (si es necesario)
    return jsonify(access_token=access_token), 200

@app.route('/recommend', methods=['GET'])
@jwt_required()  # Añade seguridad JWT a esta ruta
def recommend():
    user_id = request.args.get('user_id')
    recommendations = get_user_recommendations(user_id, user_product_matrix, user_similarity_df, num_recommendations=5)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)