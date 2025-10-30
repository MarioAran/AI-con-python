from flask import Flask, request, jsonify
import pandas as pd 
import re 
import funcions as func
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

app = Flask(__name__)
rating = '../data/rating.csv'
animes = '../data/anime.csv'
df_rating = pd.DataFrame([])
df_anime =  pd.DataFrame([])
#list of global variables

corrAnime = None
user_rating = None
simCandidates = None
@app.route('/')
def home():
    global df_rating, df_anime 
    df_rating, df_anime =  func.read_files(rating, animes)
    
    print(f"this is a test for try read files CSV........ \n{df_rating.head(3)} \n\n {df_anime.head(3)}\nthis is the en of  test for try read files CSV........")
    if not df_rating.empty and not df_anime.empty:
        print("rating and anime files read correctly........")        
    return jsonify({
        "Name Project":"API Recomendation Animes ",
        "Version":"0.0.1",
        "Endpoints":{
            "/train":"Post - Entrenar al modelo",
            "/recommend/<int:user_id>":"Get - Obtener la recomendacion",
            "/version":"GET - obtener Version del modelo",
            "/test":"Post - Probar el modelo",
            "/healt":"Get - Estado del servicio",                   
        }        
    })
    
@app.route('/train', methods=['GET'])
def train():
    global corrAnime, user_rating
    if corrAnime is None:
        corrAnime, user_rating = func.train(df_rating)
        print(corrAnime.head(10))
        return jsonify({"PAGE":"this page is dedicate to train de model "})
    else:
        return jsonify({"error to train this model"})

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    global corrAnime, user_rating, simCandidates
    simCandidates = func.recommend(corrAnime, user_id,user_rating)
    # Convertir el DataFrame a JSON
    simCandidates_json = simCandidates.to_json(orient='index', indent=2)
    
    # Si quieres retornar el JSON directamente como respuesta
    return app.response_class(
        response=simCandidates_json,
        status=200,
        mimetype='application/json'
    )

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"Version":"0.0.1"})

@app.route('/test', methods=['POST'])
def test():
    return jsonify({"PAGE":"this page is dedicate for a test"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"PAGE":"this page is dedicate for get status from model"})






