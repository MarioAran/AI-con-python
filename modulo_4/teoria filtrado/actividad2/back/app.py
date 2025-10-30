from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from datetime import datetime
from models.recommendation_model import AnimeRecommendationModel

app = Flask(__name__)

model = AnimeRecommendationModel()
model_version = "1.0.0"
model_timestamp = None
anime_csv = '../data/anime.csv'
rating_csv = '../data/rating.csv'
animes_df = pd.read_csv(anime_csv)
ratings_df = pd.read_csv(rating_csv)
#model.fit(ratings_df, animes_df, min_ratings=100)
if model is not None:
    @app.route('/')
    def home():
        return jsonify({
            "message": "API de Recomendación de Animes",
            "version": "1.0",
            "endpoints": {
                "/train": "POST - Entrenar el modelo",
                "/recommend/<int:user_id>": "GET - Obtener recomendaciones",
                "/version": "GET - Obtener versión del modelo",
                "/test": "POST - Probar el modelo",
                "/health": "GET - Estado del servicio"
            }
        })

    @app.route('/health', methods=['GET'])
    def health_check():
        status = "healthy" if model is not None else "no_model"
        return jsonify({
            "status": status,
            "model_loaded": model is not None,
            "timestamp": datetime.now().isoformat()
        })

    @app.route('/train', methods=['GET'])
    def train_model():
        try:
            status = model.fit(ratings_df, animes_df, min_ratings=100)
            return jsonify({
                "status": status,
                })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error entrenando el modelo: {str(e)}"
            }), 500

    @app.route('/recommend/<int:user_id>', methods=['GET'])
    def get_recommendations(user_id):
        """
        Endpoint para obtener recomendaciones para un usuario
        """
        try:
            if model is None:
                return jsonify({
                    "status": "error",
                    "message": "Modelo no entrenado. Por favor, entrena el modelo primero."
                }), 400
            
            # Parámetros de la solicitud
            n_recommendations = request.args.get('n', default=10, type=int)
            
            # Obtener recomendaciones
            recommendations = model.recommend(user_id, n_recommendations)
            
            return jsonify({
                "status": "success",
                "user_id": user_id,
                "recommendations": recommendations,
                "count": len(recommendations),
                "timestamp": datetime.now().isoformat()
            }), 200
            
        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 404
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error obteniendo recomendaciones: {str(e)}"
            }), 500

    @app.route('/version', methods=['GET'])
    def get_version():
        """
        Endpoint para obtener información de la versión del modelo
        """
        return jsonify({
            "model_version": model_version,
            "model_timestamp": model_timestamp,
            "model_loaded": model is not None,
            "api_version": "1.0.0"
        })

    @app.route('/test', methods=['POST'])
    def test_model():
        """
        Endpoint para probar el modelo con datos de prueba
        """
        try:
            if model is None:
                return jsonify({
                    "status": "error",
                    "message": "Modelo no entrenado. Por favor, entrena el modelo primero."
                }), 400
            
            data = request.get_json()
            
            if not data or 'test_users' not in data:
                return jsonify({
                    "status": "error",
                    "message": "Se requiere una lista de 'test_users' en el cuerpo de la solicitud"
                }), 400
            
            test_users = data['test_users']
            n_recommendations = data.get('n_recommendations', 5)
            
            results = []
            for user_id in test_users:
                try:
                    recommendations = model.recommend(user_id, n_recommendations)
                    results.append({
                        "user_id": user_id,
                        "recommendations": recommendations,
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "user_id": user_id,
                        "recommendations": [],
                        "status": "error",
                        "message": str(e)
                    })
            
            # Métricas simples de prueba
            success_count = sum(1 for r in results if r['status'] == 'success')
            
            return jsonify({
                "status": "success",
                "test_results": results,
                "metrics": {
                    "total_users_tested": len(test_users),
                    "successful_recommendations": success_count,
                    "success_rate": success_count / len(test_users) if test_users else 0
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error en la prueba: {str(e)}"
            }), 500

    # Cargar modelo existente al iniciar (si existe)
    def load_latest_model():
        global model, model_timestamp
        try:
            model_files = [f for f in os.listdir('models') if f.startswith('anime_model_') and f.endswith('.joblib')]
            if model_files:
                latest_model = sorted(model_files)[-1]
                model = joblib.load(f'models/{latest_model}')
                model_timestamp = datetime.fromtimestamp(os.path.getctime(f'models/{latest_model}')).isoformat()
                print(f"Modelo cargado: {latest_model}")
        except Exception as e:
            print(f"No se pudo cargar modelo existente: {e}")

    if __name__ == '__main__':
        # Crear directorios si no existen
        os.makedirs('models', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Intentar cargar modelo existente
        load_latest_model()
        
        app.run(debug=True, host='http://127.0.0.1/', port=5000)
else:
    print("error create model")
