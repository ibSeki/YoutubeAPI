from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from textblob import TextBlob

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Pegando a chave da API do YouTube do .env
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Mapeamento de emojis para sentimentos
emoji_to_query = {
    "😡": "músicas intensas brasileiras de raiva",
    "😢": "músicas melancólicas brasileiras",
    "😊": "músicas animadas",
    "😆": "músicas felizes",
    "😍": "músicas românticas"
}

# Mapeamento de palavras-chave para consultas específicas
keyword_map = {
    # Tristeza
    "triste": "músicas melancólicas brasileiras",
    "tristeza": "músicas melancólicas brasileiras",
    "deprimido": "músicas melancólicas brasileiras",
    "depressivo": "músicas melancólicas brasileiras",
    "desanimado": "músicas melancólicas brasileiras",
    "infeliz": "músicas melancólicas brasileiras",
    # Raiva
    "raiva": "músicas intensas brasileiras de raiva",
    "irritado": "músicas intensas brasileiras de raiva",
    "furioso": "músicas intensas brasileiras de raiva",
    "bravo": "músicas intensas brasileiras de raiva",
    # Alegria
    "feliz": "músicas animadas",
    "alegre": "músicas animadas",
    "animado": "músicas animadas",
    # Amor
    "amor": "músicas românticas",
    "apaixonado": "músicas românticas"
}

def process_nlp(text):
    """
    Tenta identificar alguma palavra-chave no texto.
    Se não encontrar, traduz o texto para inglês (para melhorar a análise de sentimento do TextBlob)
    e, com base na polaridade, retorna uma query em português.
    """
    text_lower = text.lower()
    for keyword, mapped_query in keyword_map.items():
        if keyword in text_lower:
            return mapped_query

    # Análise de sentimento
    try:
        english_text = str(TextBlob(text).translate(to='en'))
        polarity = TextBlob(english_text).sentiment.polarity
    except Exception:
        polarity = TextBlob(text).sentiment.polarity

    if polarity < -0.2:
        return "músicas melancólicas brasileiras"
    elif polarity > 0.2:
        return "músicas animadas"
    else:
        return "músicas relaxantes"

@app.route('/search', methods=['GET'])
def search_music():
    sentiment = request.args.get('sentiment', '').strip()
    custom_query = request.args.get('custom_query', '').strip()

    # Define a query baseada no emoji ou no texto do usuário
    if custom_query:
        query = process_nlp(custom_query)
    elif sentiment:
        query = emoji_to_query.get(sentiment, "músicas animadas")
    else:
        query = "músicas animadas"

    # Verifica se a chave da API está configurada corretamente
    if not YOUTUBE_API_KEY:
        return jsonify({"error": "Chave da API do YouTube não configurada."}), 500

    # Monta a URL da YouTube Data API
    youtube_url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}&maxResults=5"
    )
    
    response = requests.get(youtube_url)
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get("items", [])
        if not videos:
            return jsonify({"message": "Nenhum vídeo encontrado."})

        results = []
        for video in videos:
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"]
            channel = video["snippet"]["channelTitle"]
            thumbnail = video["snippet"]["thumbnails"]["medium"]["url"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            embed_link = f"https://www.youtube.com/embed/{video_id}"
            results.append({
                "title": title,
                "channel": channel,
                "thumbnail": thumbnail,
                "link": video_link,
                "embed": embed_link
            })
        return jsonify(results)
    else:
        return jsonify({"error": "Erro ao acessar a API do YouTube."}), 500

if __name__ == '__main__':
    app.run(debug=True)
