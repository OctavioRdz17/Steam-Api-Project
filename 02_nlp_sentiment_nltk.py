import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer # analyzer
from nltk.corpus import stopwords
import re

# descarga necesaria para correr el analizador de sentimiento
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Cargar el archivo CSV con las reseñas
df_exp_revs = pd.read_csv('./datasets/aus_user_revs.csv')

# Cargar lista de stop words
stop_words = set(stopwords.words('english'))

# Inicializar SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()



# función para remover emoticonos
def remove_emoticons(text2):
    # Patrón de expresión regular para detectar emoticonos
    emoticon_pattern = re.compile("["
                                 u"\U0001F600-\U0001F64F"  # Emoticonos de caritas
                                 u"\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
                                 u"\U0001F680-\U0001F6FF"  # Símbolos de transporte y tecnología
                                 u"\U0001F700-\U0001F77F"  # Símbolos de alquimia
                                 u"\U0001F780-\U0001F7FF"  # Símbolos de cartas y dominó
                                 u"\U0001F800-\U0001F8FF"  # Símbolos suplementarios de cartas
                                 u"\U0001F900-\U0001F9FF"  # Símbolos suplementarios y de uso común
                                 u"\U0001FA00-\U0001FA6F"  # Símbolos suplementarios de uso común
                                 u"\U0001FA70-\U0001FAFF"  # Símbolos suplementarios de uso común
                                 u"\U0001F200-\U0001F251"  # Símbolos de la rueda del dharma
                                 "]+", flags=re.UNICODE)
    return emoticon_pattern.sub(r'', text2)

# función para tokenizar, remover stopwords y clasificar según el sentimiento 
def get_sentiment_value(text):
    if isinstance(text, str):
        text = remove_emoticons(text)
        # Tokenizar y eliminar stop words
        words = nltk.word_tokenize(text)
        words = [word for word in words if word.lower() not in stop_words]
        cleaned_text = ' '.join(words)

        # Realizar análisis de sentimiento
        sentiment_score = sia.polarity_scores(cleaned_text)
        compound_score = sentiment_score['compound']

        if compound_score < -0.1:  # Si el sentimiento es negativo
            return 0
        elif compound_score > 0.1:  # Si el sentimiento es positivo
            return 2
        else:  # Si el sentimiento es neutro
            return 1
        
    else:
        return None  # Valor nulo si no es un texto
    
# call de las funciones para la nueva columna con sentiment_analysis
df_exp_revs['sentiment_analysis'] = df_exp_revs['review'].apply(get_sentiment_value)
df_exp_revs = df_exp_revs.drop('review',axis=1)

# Guardar el DataFrame con la nueva columna en un nuevo archivo CSV
df_exp_revs.to_csv('./datasets/aus_user_revs_clean.csv', index=False)