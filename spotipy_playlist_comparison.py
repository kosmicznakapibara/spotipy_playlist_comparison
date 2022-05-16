   
#Import bibliotek:

#Biblioteka Spotipy, do łączenia się z API:
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Biblioteki do analizy danych:
import pandas as pd
from math import pi
import matplotlib.pyplot as plt

#Łączenie się z API Spotify, identyfikując się za pomocą Client ID oraz Client Secret, nadanych po rejestracji w Spotify For Developers:
SPOTIPY_CLIENT_ID='bd3a552d2c0c4d43ab8e076cff0d9851'
SPOTIPY_CLIENT_SECRET='537b21b3961d44bfb1c433ccb3db9903'

auth_manager = SpotifyClientCredentials(client_id='bd3a552d2c0c4d43ab8e076cff0d9851', client_secret='537b21b3961d44bfb1c433ccb3db9903')
sp = spotipy.Spotify(auth_manager=auth_manager)

#Utworzenie listy analizowanych cech utworów:
#energy - wartości od 0.0 do 1.0. Im wyższa wartość, tym szybszy i głośniejszy utwór.
#speechiness - wartości do 0.0 do 1.0. Im wyższa wartość, tym wyższe prawdopodobieństwo utworu wokalnego.
#danceability - wartości od 0.0 do 1.0. Im wyższa wartość, tym wyższa taneczność utworu. Taneczność jest określana na podstawie analizy różnych elementów, w tym tempa i rytmu.
#valence - wartości od 0.0 do 1.0. Im wyższa wartość tym większa "pozytywność" utworu. Im niższa, tym smutniejsze utwory.

playlist_features_analysis = ["energy", "speechiness", "danceability", "valence"]

#Utworzenie struktury danych umożliwiającej analizę porównawczą playlisty wzorcowej (model) oraz playlisty do sprawdzenia (tocheck):
playlist_model_features_analysis_df = pd.DataFrame(columns = playlist_features_analysis)
playlist_tocheck_features_analysis_df = pd.DataFrame(columns = playlist_features_analysis)

#Wprowadzenie danych - do wprowadzenia jest nazwa wykonawcy or ID playlisty dla playlisty wzorcowej i do sprawdzenia:
playlist_model = sp.user_playlist_tracks('Spotify','37i9dQZF1DX9tPFwDMOaN1')["items"]
wzorzec = "K-Pop Daebak"
playlist_tocheck = sp.user_playlist_tracks('Spotify','37i9dQZF1DX1clOuib1KtQ')["items"]
sprawdzenie = "This Is Eminem"


#Playlista wzorcowa:
#Analiza kolejnych utwórów w playliście za pomocą pętli:
for track in playlist_model:

    #Przygtowanie struktury do zaczytywania id utworu (track id) oraz struktury do analizy audio:
    playlist_model_features = {}
    playlist_model_features_analysis = {}

    #Pobranie z playlisty track id:
    playlist_model_features["track_id"] = track["track"]["id"]
    
    #Analiza audio playlisty na podstawie track id:
    audio_model_features = sp.audio_features(playlist_model_features["track_id"])[0]

    #Przyporządkowanie wybranych cech utworów do struktury:
    for feature in playlist_features_analysis:
        playlist_model_features_analysis[feature] = audio_model_features[feature]
    
    #Przygotowanie cech danego utworu z pętli:
    track_model_df = pd.DataFrame(playlist_model_features_analysis, index = [0])

    #Dołączenie utworu z pętli do struktury:
    playlist_model_features_analysis_df = pd.concat([playlist_model_features_analysis_df, track_model_df], ignore_index = True)

#Playlista do sprawdzenia:
#Analiza kolejnych utwórów w playliście za pomocą pętli:
for track in playlist_tocheck:

    #Przygtowanie struktury do zaczytywania id utworu (track id) oraz struktury do analizy audio:
    playlist_tocheck_features = {}
    playlist_tocheck_features_analysis = {}

    #Pobranie z playlisty track id:
    playlist_tocheck_features["track_id"] = track["track"]["id"]
    
    #Analiza audio playlisty na podstawie track id:
    audio_tocheck_features = sp.audio_features(playlist_tocheck_features["track_id"])[0]

    #Przyporządkowanie wybranych cech utworów do struktury:
    for feature in playlist_features_analysis:
        playlist_tocheck_features_analysis[feature] = audio_tocheck_features[feature]
    
    #Przygotowanie cech danego utworu z pętli:
    track_tocheck_df = pd.DataFrame(playlist_tocheck_features_analysis, index = [0])

    #Dołączenie utworu z pętli do struktury:
    playlist_tocheck_features_analysis_df = pd.concat([playlist_tocheck_features_analysis_df, track_tocheck_df], ignore_index = True)

#Analiza porównawcza
#Przemnożenie razy 100 w celu wyraźniejszego pokazania różnic:

playlist_model_features_analysis_df = playlist_model_features_analysis_df*100
playlist_tocheck_features_analysis_df = playlist_tocheck_features_analysis_df*100


#Przygotowanie struktury danych pod wykres radarowy:
df = pd.DataFrame({
'group': ["wzorzec", "do sprawdzenia"],
'energy': [playlist_model_features_analysis_df["energy"].mean(), playlist_tocheck_features_analysis_df["energy"].mean()],
'speechiness': [playlist_model_features_analysis_df["speechiness"].mean(), playlist_tocheck_features_analysis_df["speechiness"].mean()],
'danceability': [playlist_model_features_analysis_df["danceability"].mean(), playlist_tocheck_features_analysis_df["danceability"].mean()],
'valence': [playlist_model_features_analysis_df["valence"].mean(), playlist_tocheck_features_analysis_df["valence"].mean()],
})
 
#Przygotowanie tła wykresu:
 
#Liczba zmiennych:
categories=list(df)[1:]
N = len(categories)
 
#Obliczenie kąta każdej z osi wykresu (podział wykresu przez liczbę zmiennych)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
#Wykres radarowy
ax = plt.subplot(111, polar=True)
 
#Przygotowanie kolejności (pierwsza oś na górze wykresu)
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
#Rysowanie jednej zmiennej na wyliczny kąt i dodanie etykiety
plt.xticks(angles[:-1], categories)
 
#Osie y:
ax.set_rlabel_position(0)
plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="grey", size=7)
plt.ylim(0,100)
 
#Rysowanie wykresu
#Pierwsza grupa
values=df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label=wzorzec)
ax.fill(angles, values, 'b', alpha=0.1)
 
#Druga grupa
values=df.loc[1].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label=sprawdzenie)
ax.fill(angles, values, 'r', alpha=0.1)
 
#Dodanie legendy
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

#Wyświetlenie wykresu
plt.show()