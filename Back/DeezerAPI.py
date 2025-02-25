import requests

# Dicionário de sentimentos mapeados para palavras-chave musicais
sentiment_to_keyword = {
    "feliz": "happy",
    "triste": "sad",
    "animado": "energetic",
    "calmo": "chill",
    "melancólico": "melancholy",
    "apaixonado": "romantic"
}

def get_music_by_sentiment(sentiment):
    # Mapeia o sentimento para um termo de busca
    keyword = sentiment_to_keyword.get(sentiment.lower(), sentiment)
    
    # URL da API do Deezer para busca
    url = f"https://api.deezer.com/search?q={keyword}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("data", [])

        if not tracks:
            return "Nenhuma música encontrada para esse sentimento."

        # Exibir as 5 primeiras sugestões
        results = []
        for track in tracks[:5]:
            results.append(f"{track['title']} - {track['artist']['name']} (Link: {track['link']})")
        
        return results
    else:
        return "Erro ao acessar a API do Deezer."

# Exemplo de uso
sentimento_usuario = input("Como você está se sentindo? ")
musicas = get_music_by_sentiment(sentimento_usuario)

if isinstance(musicas, list):
    print("\nSugestões de músicas para você:")
    for musica in musicas:
        print(musica)
else:
    print(musicas)
