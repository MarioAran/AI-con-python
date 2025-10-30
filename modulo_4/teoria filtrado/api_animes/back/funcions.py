import re 
import pandas as pd 



def text_cleaning(text):
    text = re.sub(r'&quot;', '', text)
    text = re.sub(r'.hack//', '', text)
    text = re.sub(r'&#039;', '', text)
    text = re.sub(r'A&#039;s', '', text)
    text = re.sub(r'I&#039;', 'I\'', text)
    text = re.sub(r'&amp;', 'and', text)
    return text

def read_files(rating, anime ):
    try:
        r_cols = ['user_id', 'anime_id', 'rating']
        df_ratings = pd.read_csv(rating, usecols=r_cols, encoding = 'utf-8')
        df_ratings = df_ratings[df_ratings['rating'] != -1]
        
        c_cols = ['anime_id', 'name', 'type']
        df_anime = pd.read_csv(anime, usecols=c_cols,encoding = 'utf-8')
        df_anime = df_anime[df_anime['type'] != 'music']
        df_anime['name'] = df_anime['name'].apply(text_cleaning)
        anime_dict = dict(zip(df_anime['anime_id'], df_anime['name']))
        df_ratings['name'] = df_ratings['anime_id'].map(anime_dict)
        
        return df_ratings, df_anime
    except Exception as e : 
        print('there was an error with your input :{0}'.format(e)
)
    
def train(df_ratings):
    user_rating = df_ratings.pivot_table(index =['user_id'],columns = ['name'], values='rating')
    user_rating.head()
    corrAnime = user_rating.corr(method ='pearson', min_periods = 100)
    corrAnime.head()
    return corrAnime, user_rating

def recommend(corrAnime, user_id, user_rating):
    myRating = user_rating.loc[user_id].dropna()
    simCandidates = pd.Series()
    #hace una lista con los animes recomendados segun los rating del id del usuario proporcionado 
    for i in range(0,len(myRating.index)):
        sims = corrAnime[myRating.index[i]].dropna()
        sims= sims.map( lambda x:x*myRating[i])
        simCandidates = pd.concat([simCandidates, sims])
    simCandidates.sort_values(inplace = True, ascending =False)
    
    #elimina los rating del usuario o los ignora 
    filteredSims = simCandidates.drop(myRating.index)

    return filteredSims
