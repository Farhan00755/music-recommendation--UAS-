from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data.csv")

# Terapkan aturan mood & genre (copy dari Colab)
df['mood'] = 'Neutral'
df.loc[(df['valence'] > 0.75) & (df['energy'] > 0.75), 'mood'] = 'Happy'
df.loc[(df['valence'] < 0.25) & (df['energy'] < 0.25), 'mood'] = 'Sad'
df.loc[(df['energy'] > 0.8), 'mood'] = 'Energetic'
df.loc[(df['acousticness'] > 0.8) & (df['energy'] < 0.3), 'mood'] = 'Calm'

df['genre'] = 'Other'
df.loc[(df['energy'] > 0.7) & (df['loudness'] > -5) & (df['danceability'] < 0.6), 'genre'] = 'Rock'
df.loc[(df['popularity'] > 70) & (df['danceability'] > 0.6), 'genre'] = 'Pop'
df.loc[(df['acousticness'] > 0.5) & (df['instrumentalness'] > 0.5) & (df['tempo'] < 120), 'genre'] = 'Jazz/Blues'
df.loc[(df['acousticness'] > 0.8) & (df['instrumentalness'] > 0.7), 'genre'] = 'Classical/Ambient'
df.loc[(df['speechiness'] > 0.2) & (df['danceability'] > 0.7), 'genre'] = 'Hip Hop'
df.loc[(df['acousticness'] > 0.6) & (df['tempo'] < 100) & (df['valence'] > 0.5), 'genre'] = 'Folk/Country'
df.loc[(df['danceability'] > 0.7) & (df['energy'] > 0.7) & (df['tempo'] > 120), 'genre'] = 'Electronic/Dance'
df.loc[(df['year'] < 1970) & (df['popularity'] > 50), 'genre'] = 'Oldies'

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["GET"])
def recommend():
    mood = request.args.get("mood")
    genre = request.args.get("genre")
    recommendations = df[(df['mood'] == mood) & (df['genre'] == genre)]

    if recommendations.empty:
        return jsonify({
            "message": "Tidak ada lagu ditemukan",
            "mood": mood,
            "genre": genre,
        }), 404
    else:
        songs = recommendations.sample(n=min(5, len(recommendations)), random_state=42)
        return jsonify(songs[['name','artists','popularity','mood','genre']].to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)