import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from time import sleep
from pathlib import Path
import boto3
import fsspec
import s3fs
from dotenv import load_dotenv

##FUNKCJE

# #ustawienie hasła
# now = datetime.datetime.now()
# password = now.strftime('%y-%m-%d') #hasło = dzisiejsza data

# #funkcja sprawdzająca hasło
# def check_password():
#     def password_entered():
#         if st.session_state['password'] == password:
#             st.session_state['password_correct'] = True
#             del st.session_state['password']
#         else:
#             st.session_state['password_correct'] = False

#     if 'password_correct' not in st.session_state:
#         st.text_input(
#             'Wprowadź hasło', type='password', on_change=password_entered, key='password', help= 'Hasło to dzisiejsza data zapisana w formacie Y-m-d'
#         )
#         return False
#     elif not st.session_state['password_correct']:
#         st.text_input(
#             'Wprowadź hasło', type='password', on_change=password_entered, key='password', help= 'Hasło to dzisiejsza data zapisana w formacie Y-m-d'
#         )
#         st.error('Nieprawidłowe hasło')
#         return False
#     else:
        # return True
    
# komunikacja z Digital Ocean Spaces
BUCKET_NAME = 'halfmarathon'

load_dotenv()

session = boto3.session.Session()
client = session.client('s3',
                        # region_name='fra1', 
                        # endpoint_url='https://fra1.digitaloceanspaces.com',
                        # aws_access_key_id=,
                        # aws_secret_access_key=,
)

##SPRAWDZANIE PRZYCISKÓW W SESSION STATE

#inicjalizacja 1 niewciśniętego przycisku "Przeglądaj dane z ankiety"
if 'first_button_pressed' not in st.session_state:
    st.session_state['first_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 1 przycisk "Przeglądaj dane z ankiety"
def check_first_button_pressed():
    st.session_state['first_button_pressed'] = True
#inicjalizacja 2 niewciśniętego przycisku - "Przejdź do opcji"
if 'second_button_pressed' not in st.session_state:
    st.session_state['second_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 2 przycisk - "Przejdź do opcji"
#def check_second_button_pressed():
    #st.session_state['second_button_pressed'] = True
#inicjalizacja 3 niewciśniętego przycisku "Przejdź do ciekawostki" - ulubione zwierzeta
if 'third_button_pressed' not in st.session_state:
    st.session_state['third_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 3 przycisk "Przejdź do ciekawostki" - ulubion zwierzeta
def check_third_button_pressed():
    st.session_state['third_button_pressed'] = True
    st.session_state['balloons_shown'] = False #resetuje dodatkowo balony
#inicjalizacja 4 niewciśniętego przycisku "Przejdź do ciekawostki" - ulubione miejsca
if 'fourth_button_pressed' not in st.session_state:
    st.session_state['fourth_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 4 przycisk "Przejdź do ciekawostki" - ulubione miejsca
def check_fourth_button_pressed():
    st.session_state['fourth_button_pressed'] = True
    st.session_state['balloons_shown'] = False 
#inicjalizacja 5 niewciśniętego przycisku "Przejdź do ciekawostki" - hobby
if 'fifth_button_pressed' not in st.session_state:
    st.session_state['fifth_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 5 przycisk "Przejdź do ciekawostki" - hobby
def check_fifth_button_pressed():
    st.session_state['fifth_button_pressed'] = True
    st.session_state['balloons_shown'] = False 
#inicjalizacja 6 niewciśniętego przycisku "Przejdź do ciekawostki" - sprawdzone metody nauki
if 'sixth_button_pressed' not in st.session_state:
    st.session_state['sixth_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 6 przycisk "Przejdź do ciekawostki" - sprawdzone metody nauki
def check_sixth_button_pressed():
    st.session_state['sixth_button_pressed'] = True
    st.session_state['balloons_shown'] = False 
#inicjalizacja 7 niewciśniętego przycisku "Przejdź do ciekawostki" - najwieksze motywacje
if 'seventh_button_pressed' not in st.session_state:
    st.session_state['seventh_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 7 przycisk "Przejdź do ciekawostki" - najwieksze motywacje
def check_seventh_button_pressed():
    st.session_state['seventh_button_pressed'] = True
    st.session_state['balloons_shown'] = False 
#inicjalizacja 8 niewciśniętego przycisku "Przejdź do ciekawostki" - branże
if 'eighth_button_pressed' not in st.session_state:
    st.session_state['eighth_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 8 przycisk "Przejdź do ciekawostki" - branże
def check_eighth_button_pressed():
    st.session_state['eighth_button_pressed'] = True
    st.session_state['balloons_shown'] = False 
#inicjalizacja 9 niewciśniętego przycisku "Przejdź do ciekawostki" - preferencje smakowe
if 'ninth_button_pressed' not in st.session_state:
    st.session_state['ninth_button_pressed'] = False
#funkcja sprawdzająca czy naciśnięto 9 przycisk "Przejdź do ciekawostki" - preferencje smakowe
def check_ninth_button_pressed():
    st.session_state['ninth_button_pressed'] = True
    st.session_state['balloons_shown'] = False 


# if check_password():
       
if st.session_state['first_button_pressed']:
        #WCZYTANIE DANYCH Z CLOUD STORAGE
            df = pd.read_csv(f's3://{BUCKET_NAME}/stocks/welcome_survey_data/welcome_survey_cleaned.csv', sep=';')
            #df = pd.read_csv('35__welcome_survey_cleaned.csv', sep =';')
            st.title(':hand: Ankieta powitalna')

            #PASEK BOCZNY - LAYOUT
            with st.sidebar:
                st.subheader(':mag_right: Filtry :mag:')

                #kategoria wiekowa
                df['age'] = df['age'].map({
                '<18' : '0-18',
                '18-24' : '18-24',
                '25-34' : '25-34',
                '35-44' : '35-44',
                '45-54' : '45-54',
                '55-64' : '55-64',
                '>=65' : '>=65',
                'unknown' : 'unknown'})
                age_df = sorted(df['age'].dropna().unique())
                age_categories = st.multiselect(
                    'Wybierz kategorię wiekową', age_df)
                
                #poziom wykształcenia
                edu_df = df['edu_level'].dropna().unique()
                edu_level = st.multiselect(
                    'Wybierz poziom wykształcenia', edu_df)
                
                #ulubione zwierzęta
                animals_df = sorted(df['fav_animals'].dropna().unique())
                fav_animals = st.multiselect(
                    'Wybierz ulubione zwierzęta', animals_df)
                
                #ulubione miejsce
                place_df = sorted(df['fav_place'].dropna().unique())
                fav_place = st.multiselect(
                    'Wybierz ulubione miejsce', place_df)
                
                #smaki
                taste_df = df['sweet_or_salty'].dropna().unique()
                taste = st.multiselect(
                    'Wybierz preferencje smakowe', taste_df)
                
                #doświadczenie w latach pracy
                experience = st.number_input('Wpisz ilość lat doświadczenia', step= 1, 
                                            min_value= 0, max_value= 20)
                
                #płeć
                gender = st.radio(
                    'Wybierz płeć', ['Wszyscy', 'Mężczyźni', 'Kobiety', 'Płeć nieznana']
                )

            ##FILTROWANIE
            if age_categories:
                df= df[df['age'].isin(age_categories)]

            if edu_level:
                df= df[df['edu_level'].isin(edu_level)]

            if fav_animals:
                df= df[df['fav_animals'].isin(fav_animals)]

            if fav_place:
                df= df[df['fav_plaxce'].isin(fav_place)]

            if taste:
                df= df[df['sweet_or_salty'].isin(taste)] 

            if (experience > 0) & (experience <= 2):
                df = df[df['years_of_experience'] == '0-2']
            elif (experience > 2) & (experience <= 5):
                df = df[df['years_of_experience'] == '3-5']
            elif (experience > 5) & (experience <= 10):
                df = df[df['years_of_experience'] == '6-10']
            elif (experience > 10) & (experience <= 15):
                df = df[df['years_of_experience'] == '11-15']
            elif experience > 15:
                df = df[df['years_of_experience'] == '>=16']

            if gender == 'Mężczyźni':
                df = df[df['gender'] == 0]
            elif gender == 'Kobiety':
                df = df[df['gender'] == 1]
            elif gender == 'Płeć nieznana':
                df = df[df['gender'].isnull()]

            if st.session_state['second_button_pressed']:
    
                ##MAIN LAYOUT
                option = st.selectbox(
                    'Wybierz opcje',
                    [
                        'Ogólne informacje',
                        'Losowe rzędy',
                        'Najwyższe staże pracy',
                        'Wykresy',
                        'Ulubione zwierzęta',
                        'Ulubione miejsca',
                        'Hobby',
                        'Branże',
                        'Sprawdzone metody nauki',
                        'Największe motywacje',
                        'Preferencje smakowe',
                        'Relacje pomiędzy danymi',
                        'Wróć do menu głównego'
                    ]
                )
                if option == 'Ogólne informacje':

                    t1, t2, t3, t4, t5 = st.tabs([
                        'Liczba ankietowanych',
                        'Wartości unikatowe',
                        'Statystyki opisowe',
                        'Brakujące wartości',
                        'Duplikaty'
                    ])

                    with t1:

                        c0, c1, c2, c3 = st.columns(4)
                        #liczba zawodników
                        with c0:
                            st.metric('Liczba uczestników', len(df))
                        #liczba mężczyzn -> mężczyźni oznaczeni w ankiecie jako "0"
                        with c1:
                            st.metric('Liczba mężczyzn', len(df[df['gender'] == 0]))
                        #liczba kobiet -> kobiety oznaczone w ankiecie jako "1"
                        with c2:
                            st.metric('Liczba kobiet', len(df[df['gender']== 1]))
                        #liczba osób, które nie podały płci (NaN)
                        with c3:
                            st.metric('Płeć nieznana', len(df[df['gender'].isnull()]))
                        sleep(4)
                        st.write('---')
                        st.write('W ankiecie wzięło udział najwięcej mężczyzn.')
                    
                    with t2:
                        c0, c1, c2, c3 = st.columns(4)
                        with c0:
                            st.metric('Grupy wiekowe', df['age'].nunique())
                            st.metric('Rodzaje branży', df['industry'].nunique())
                            st.metric('Preferowane smaki', df['sweet_or_salty'].nunique())
                        with c1:
                            st.metric('Poziomy wykształcenia', df['edu_level'].nunique())
                            st.metric('Rodzaje hobby', 6)
                            st.metric('Staże pracy', df['years_of_experience'].nunique())
                        with c2:
                            st.metric('Ulubione zwierzęta', df['fav_animals'].nunique())
                            st.metric('Rodzaje metod uczenia', 8)
                        with c3:
                            st.metric('Ulubione miejsca', df['fav_place'].nunique())
                            st.metric('Rodzaje motywacji', 6)
                        sleep(4)
                        st.write('---')
                        st.write('Wśród ankietowanych najbardziej różnorodne były branże, w których pracują.')

                    with t3:
                        rename_df = df.rename(columns = {
                        'gender' : 'płeć',
                        'hobby_art' : 'sztuka',
                        'hobby_books' : 'książki',
                        'hobby_movies' : 'filmy',
                        'hobby_other' : 'inne hobby',
                        'hobby_sport' : 'sport',
                        'hobby_video_games' : 'gry wideo',
                        'learning_pref_books' : 'uczenie z książek',
                        'learning_pref_chatgpt' : 'czat gpt',
                        'learning_pref_offline_courses' : 'kursy offline',
                        'learning_pref_online_courses' : 'kursy online',
                        'learning_pref_personal_projects' : 'osobiste projekty',
                        'learning_pref_teaching' : 'nauczanie',
                        'learning_pref_teamwork' : 'praca zespołowa',
                        'learning_pref_workshops' : 'warsztaty',
                        'motivation_career' : 'kariera',
                        'motivation_challenges' : 'wyzwania',
                        'motivation_creativity_and_innovation' : 'innowacje i kreatywność',
                        'motivation_money_and_job' : 'pieniądze i praca',
                        'motivation_personal_growth' : 'rozwój osobisty',
                        'motivation_remote' : 'praca zdalna'
                    })
                        desc_df = rename_df.describe().T
                        st.dataframe(desc_df, use_container_width= True, height= 770)
                        sleep(4)
                        st.write('---')
                        st.markdown("""
                                Z powyższych statystyk można wywnioskować, że ankietowani:
                                * najbardziej lubią czytać książki lub oglądać filmy,
                                * ich głównymi sposobami na naukę są kursy online,
                                * jako motywacje cenią sobie najchętniej rozwój osobisty.
                                    """)

                    with t4:
                        c0, c1, c2, c3 = st.columns(4)

                        with c0:
                            st.metric('Ulubione miejsca', df['fav_place'].isnull().sum())
                            st.metric('Staże pracy', df['years_of_experience'].isnull().sum())
                        with c1:
                            st.metric('Rodzaje branży', df['industry'].isnull().sum())
                        with c2:
                            st.metric('Preferowane smaki', df['sweet_or_salty'].isnull().sum())
                        with c3:
                            st.metric('Płeć', df['gender'].isnull().sum())
                        st.write('---')
                        st.write('Ankietowani najrzadziej podawali branżę, w której pracują lub ulubione miejsce, w którym się relaksują. Niechętnie decydowali się również czy wolą smaki słone czy słodkie.')

                    with t5:
                        st.write('Nie znaleziono żadnych duplikatów w analizowanym zbiorze danych.')


                if option == 'Losowe rzędy':

                    #losowe rzędy
                    slider = st.slider('Wybierz ilość losowych rzędów', min_value=0, max_value=20, value=0)
                    if slider:
                        x = min(slider, len(df))
                        st.dataframe(df.sample(x), use_container_width= True, hide_index=True)

                if option == 'Najwyższe staże pracy':

                    #top z najwyższym doświadczeniem zawodowym
                    number = st.number_input(
                        'Wpisz ilość rekordów związanych z najwyższym stażem pracy'    
                    , step=1, min_value=0, max_value=20)
                    if number == 0:
                        st.write('Nie wpisano ilości rekordów.')
                    elif number == 1:
                        st.header(f'{number} osoba z najwyższym doświadczeniem') 
                        top_columns = ['age', 'edu_level', 'gender', 'industry', 'motivation_career',
                                    'motivation_challenges', 'motivation_creativity_and_innovation',
                                    'motivation_money_and_job', 'motivation_personal_growth', 
                                    'motivation_remote', 'years_of_experience']
                        st.dataframe(df.sort_values('years_of_experience', ascending= False)[top_columns].head(number),
                                    use_container_width= True, hide_index= True)
                    elif (number == 2) or (number == 3) or (number == 4):
                        st.header(f'{number} osoby z najwyższym doświadczeniem') 
                        top_columns = ['age', 'edu_level', 'gender', 'industry', 'motivation_career',
                                    'motivation_challenges', 'motivation_creativity_and_innovation',
                                    'motivation_money_and_job', 'motivation_personal_growth', 
                                    'motivation_remote', 'years_of_experience']
                        st.dataframe(df.sort_values('years_of_experience', ascending= False)[top_columns].head(number),
                                    use_container_width= True, hide_index= True)
                    else:
                        st.header(f'{number} osób z najwyższym doświadczeniem') 
                        top_columns = ['age', 'edu_level', 'gender', 'industry', 'motivation_career',
                                    'motivation_challenges', 'motivation_creativity_and_innovation',
                                    'motivation_money_and_job', 'motivation_personal_growth', 
                                    'motivation_remote', 'years_of_experience']
                        st.dataframe(df.sort_values('years_of_experience', ascending= False)[top_columns].head(number),
                                    use_container_width= True, hide_index= True)

                if option == 'Wykresy':
                    ##RYSOWANIE WYKRESÓW

                    #bar-plot przedziałów wiekowych
                    st.header('Wiek uczestników')
                    age_categories_df = df.groupby('age', as_index = False).count().rename(columns= {'edu_level' : 'Liczba uczestników', 'age' : 'Kategoria wiekowa'})
                    st.bar_chart(age_categories_df, x = 'Kategoria wiekowa', y = 'Liczba uczestników')

                    #bar-plot doświadczenia 
                    st.header('Doświadczenie zawodowe')
                    experience_df = df.groupby('years_of_experience', as_index = False).count().rename(columns= {
                    'edu_level' : 'Liczba uczestników','years_of_experience' : 'Lata doświadczenia'})
                    #sortowanie wg odpowiedniej kolejności : 0-2, 3-5, 6-10, 11-15, >=16
                    categories_experience = ['0-2', '3-5', '6-10', '11-15', '>=16']
                    experience_df['Lata doświadczenia'] = pd.Categorical(experience_df['Lata doświadczenia'], categories= categories_experience, ordered=True)
                    st.bar_chart(experience_df, x = 'Lata doświadczenia', y = 'Liczba uczestników')

                    #bar-plot wykształcenie
                    st.header('Wykształcenie')
                    edu_df = df.groupby('edu_level', as_index = False).count().rename(columns= {'edu_level' : 'Wykształcenie', 'age' : 'Liczba uczestników'})
                    categories_edu = ['Podstawowe', 'Średnie', 'Wyższe']
                    edu_df['Wykształcenie'] = pd.Categorical(edu_df['Wykształcenie'], categories= categories_edu, ordered= True)
                    st.bar_chart(edu_df, x = 'Wykształcenie', y = 'Liczba uczestników', use_container_width= True, x_label= 'Poziom wykształcenia')
                    #bar-plot ulubione zwierzęta
                    st.header('Ulubione zwierzęta')
                    fav_animals_df = df.groupby('fav_animals', as_index = False).count().rename(columns= {'edu_level' : 'Liczba uczestników', 'fav_animals' : 'Ulubione zwierzęta'})
                    # categories_edu = ['Podstawowe', 'Średnie', 'Wyższe']
                    # edu_df['Wykształcenie'] = pd.Categorical(edu_df['Wykształcenie'], categories= categories_edu, ordered= True)
                    st.bar_chart(fav_animals_df, x = 'Ulubione zwierzęta', y = 'Liczba uczestników', x_label= 'Rodzaj')

                    #bar-plot ulubione miejsce
                    st.header('Ulubione miejsce')
                    fav_place_df = df.groupby('fav_place', as_index = False).count().rename(columns= {'edu_level' : 'Liczba uczestników', 'fav_place' : 'Ulubione miejsce'})
                    st.bar_chart(fav_place_df, x = 'Ulubione miejsce', y = 'Liczba uczestników', x_label= 'Nazwa miejsca')

                    #bar-plot branża
                    st.header('Branża')
                    industry_df = df.groupby('industry', as_index = False).count().rename(columns= {'edu_level' : 'Liczba uczestników', 'industry' : 'Branża'})
                    st.bar_chart(industry_df, x = 'Branża', y = 'Liczba uczestników', x_label = 'Rodzaj branży'
                                    , horizontal= True, use_container_width= True)

                    #bar-plot preferencje smakowe
                    st.header('Preferencje smakowe')
                    sweet_salty_df = df.groupby('sweet_or_salty', as_index = False).count().rename(columns= {'edu_level' : 'Liczba uczestników', 'sweet_or_salty' : 'Słodkie/ słone'})
                    st.bar_chart(sweet_salty_df, x = 'Słodkie/ słone', y = 'Liczba uczestników', x_label = 'Wybrany smak')
                                    
                    #bar-plot hobby
                    st.header('Hobby')
                    hobby_art = df['edu_level'][df['hobby_art'] == 1].count()
                    hobby_books = df['edu_level'][df['hobby_books'] == 1].count()
                    hobby_movies = df['edu_level'][df['hobby_movies'] == 1].count()
                    hobby_other = df['edu_level'][df['hobby_other'] == 1].count()
                    hobby_sport = df['edu_level'][df['hobby_sport'] == 1].count()
                    hobby_video_games = df['edu_level'][df['hobby_video_games'] == 1].count()
                    hobby_df = pd.DataFrame({
                            'hobby' : ['sztuka', 'książki', 'filmy', 'inne', 'sport', 'gry wideo'],
                            'count' : [hobby_art, hobby_books, hobby_movies, hobby_other, hobby_sport, hobby_video_games]
                        })
                    st.bar_chart(hobby_df, x = 'hobby', y = 'count', x_label= 'Rodzaj hobby',
                                    y_label= 'Liczba uczestników')

                    #bar-plot preferencje uczenia
                    st.header('Preferencje uczenia')
                    learning_pref_books = df['edu_level'][df['learning_pref_books'] == 1].count()
                    learning_pref_chatgpt = df['edu_level'][df['learning_pref_chatgpt'] == 1].count()
                    learning_pref_offline_courses = df['edu_level'][df['learning_pref_offline_courses'] == 1].count()
                    learning_pref_online_courses = df['edu_level'][df['learning_pref_online_courses'] == 1].count()
                    learning_pref_personal_projects = df['edu_level'][df['learning_pref_personal_projects'] == 1].count()
                    learning_pref_teaching = df['edu_level'][df['learning_pref_teaching'] == 1].count()
                    learning_pref_workshops = df['edu_level'][df['learning_pref_workshops'] == 1].count()
                    learning_pref_df = pd.DataFrame({
                            'learning_pref' : ['książki', 'chat gpt', 'kursy offline', 'kursy online', 'osobiste projekty', 'nauczanie', 'warsztaty'],
                            'count' : [learning_pref_books, learning_pref_chatgpt, learning_pref_offline_courses,
                                    learning_pref_online_courses, learning_pref_personal_projects,
                                    learning_pref_teaching, learning_pref_workshops]          
                        })
                    st.bar_chart(learning_pref_df, x = 'learning_pref', y = 'count', x_label= 'Preferowany sposób uczenia',
                                    y_label= 'Liczba uczestników')

                    #bar-plot motywacje
                    st.header('Największe motywacje')
                    motivation_carrer = df['edu_level'][df['motivation_career'] == 1].count()
                    motivation_challenges = df['edu_level'][df['motivation_challenges'] == 1].count()
                    motivation_creativity_and_innovation = df['edu_level'][df['motivation_creativity_and_innovation'] == 1].count()
                    motivation_money_and_job = df['edu_level'][df['motivation_money_and_job'] == 1].count()
                    motivation_personal_growth = df['edu_level'][df['motivation_personal_growth'] == 1].count()
                    motivation_remote = df['edu_level'][df['motivation_remote'] == 1].count()
                    motivation_df = pd.DataFrame({
                            'motivation' : ['kariera', 'nowe wyzwania', 'innowacje', 'praca i pieniądze', 'rozwój osobisty', 'praca zdalna'],
                            'count' : [motivation_carrer, motivation_challenges, motivation_creativity_and_innovation,
                                    motivation_money_and_job, motivation_personal_growth,
                                    motivation_remote]
                        })
                    st.bar_chart(motivation_df, x = 'motivation', y = 'count', x_label= '"Co mnie motywuje?"',
                                    y_label= 'Liczba uczestników')

                if option == 'Ulubione zwierzęta':
                    if st.session_state.get('third_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True

                        st.image('https://www.tapeciarnia.pl/tapety/normalne/61375_maly_slodki_piesek_beagle.jpg')
                        with st.expander('Dlaczego nasze psy machają ogonem?'):
                            st.markdown("""
                                    Komunikacja zwierząt jest złożona, ale pewne elementy można łatwo zrozumieć i interpretować. Psy poprzez swój ogon wyrażają poziom pobudzenia, nie tylko radość. Pies ze stresu też może machać ogonem! Cała mowa ciała psa będzie na to wskazywać. Psy machają luźno ogonem z boku na bok, aby wyrazić przyjazność lub zainteresowanie. Natomiast szybkie ruchy ogona wyrażają różne stany wewnętrzne w zależności od jego pozycji; psy komunikują pewność siebie, jeśli trzymają wysoko ogon, podczas gdy niskie machanie jest zwykle związane z niepokojem, nerwowością lub wewnętrznym konfliktem. Także podczas komunikacji nie zapominajmy o psim ogonie, który jest bardzo ważnym i kluczowym wskaźnikiem emocji.
                                    """)
                        if st.button('Powrót'):
                            st.session_state['third_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1.35, 1])
                            with new_c0:
                                animal_data = df['fav_animals'].value_counts().reset_index().rename(columns={'fav_animals': 'Ulubione zwierzęta', 'count': 'Ilość oddanych głosów'})
                                animal_df = pd.DataFrame(animal_data)
                                st.dataframe(animal_df, hide_index=True)
                            with new_c1:
                                st.write('Top 3 ulubionych zwierząt')
                                st.bar_chart(data=animal_df.head(3), x='Ulubione zwierzęta', y='Ilość oddanych głosów', horizontal=True, height=200)
                            st.markdown('#### Zatem wynika, że ulubionym zwierzęciem ankietowanych jest PIES \U0001f436\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_third_button_pressed, use_container_width=True)
                
                if option == 'Ulubione miejsca':
                    if st.session_state.get('fourth_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True
                        
                        st.image('https://bezpieczna-podroz.pl/wp-content/uploads/2020/03/adventure-1836601_1920.jpg')
                        with st.expander('5 żelaznych zasad bezpiecznego pływania, których warto być świadomy'):
                            st.markdown("""
                                    1. Nie pływaj w wodzie o temperaturze poniżej 14 stopni Celsjusza, najlepsza temperatura to 22-25 stopni.
                                    2. Nie przebywaj też za długo w wodzie, gdyż grozi to wychłodzeniem organizmu. Po wyjściu z wody trzeba się osuszyć i przebrać w suche ubranie.
                                    3. Nie pływaj na czczo lub bezpośrednio po posiłku.    
                                    4. Podczas pływania kajakiem, łódką czy żaglówką, pamiętaj zawsze o założeniu dziecku kamizelki ratunkowej z kołnierzem, która musi być dopasowana do jego wagi i wzrostu oraz koniecznie zapięta.
                                    5. Dobrze jest wpisać do telefonu numer ratunkowy nad wodą - 601 100 100. W razie wypadku zadzwoń, podając miejsce zdarzenia, opisując sytuację, stan osób poszkodowanych i ich liczbę. Koniecznie podaj swoje nazwisko. Nigdy nie przerywaj pierwszy rozmowy z dyżurnym!    
                                        """)
                        if st.button('Powrót'):
                            st.session_state['fourth_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1.3, 1])
                            with new_c0:
                                place_data = df['fav_place'].value_counts().reset_index().rename(columns={'fav_place': 'Ulubione miejsca', 'count': 'Ilość oddanych głosów'})
                                fav_place_df = pd.DataFrame(place_data)
                                st.dataframe(fav_place_df, hide_index=True)
                            with new_c1:
                                st.write('Top 3 ulubionych miejsc')
                                st.bar_chart(data=fav_place_df.head(3), x='Ulubione miejsca', y='Ilość oddanych głosów', horizontal=True, height=170)
                            st.markdown('#### Zatem wynika, że ulubionym miejscem do odpoczynku ankietowanych jest MIEJSCE NAD WODĄ \U0001f30a\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_fourth_button_pressed, use_container_width=True)
                
                if option == 'Hobby':
                    if st.session_state.get('fifth_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True
                        
                        st.image('https://img.joemonster.org/i/upload/2021/06/filmkino15.jpg')
                        with st.expander('Październik 1994 - niesamowity weekend dla światowego kina'):
                            st.markdown("""
                                        W październiku 1994 r. przez jeden weekend w kinach były jednocześnie pokazywane filmy: "Pulp Fiction", "Jurassic Park", "Forrest Gump", "Nowy koszmar Wesa Cravena" i "Skazani na Shawshank". 
                                        """)
    
                        if st.button('Powrót'):
                            st.session_state['fifth_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1, 1])
                            with new_c0:
                                hobby_art = df['edu_level'][df['hobby_art'] == 1].count()
                                hobby_books = df['edu_level'][df['hobby_books'] == 1].count()
                                hobby_movies = df['edu_level'][df['hobby_movies'] == 1].count()
                                hobby_other = df['edu_level'][df['hobby_other'] == 1].count()
                                hobby_sport = df['edu_level'][df['hobby_sport'] == 1].count()
                                hobby_video_games = df['edu_level'][df['hobby_video_games'] == 1].count() 
                                hobby_df = pd.DataFrame({
                                    'Ulubione hobby' : ['sztuka', 'książki', 'filmy', 'inne', 'sport', 'gry wideo'],
                                    'Ilość oddanych głosów' : [hobby_art, hobby_books, hobby_movies, hobby_other, hobby_sport, hobby_video_games]
                                    })
                                sorted_hobby_df = hobby_df.sort_values(by= 'Ilość oddanych głosów', ascending = False)
                                st.dataframe(data=sorted_hobby_df, hide_index=True, use_container_width=True)
                            with new_c1:
                                st.write('Top 3 ulubionych hobby')
                                st.bar_chart(data=hobby_df.head(3), x='Ulubione hobby', y='Ilość oddanych głosów', horizontal=True, height=230)              
                            st.markdown('#### Zatem wynika, że ulubionym hobby ankietowanych jest OGLĄDANIE FILMÓW \U0001f3a6\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_fifth_button_pressed, use_container_width=True) 
                
                if option == 'Branże':
                    if st.session_state.get('eighth_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True

                        st.image('https://cdn.bulldogjob.com/system/photos/files/000/003/981/original/euWktkqTURBXy8zMTg2OGYwMTc3NWFjYzc1NTk4MmYyMDIzMGY2Y2Q5MS5qcGVnkpUDAADNAyDNAcKTBc0DUs0B3g.jpg')
                        with st.expander('Ciekawostki ze sfery IT'):
                            st.markdown("""
                                    1. Istnieje ponad 700 języków programowania na świecie.
                                    2. Twórcą pierwszego kodu była kobieta - Ada Lovelace.
                                    3. Pierwszym komputerem był "ENIAC" (Electronic Numerical Integrator and Computer), który w 1945 roku został wykorzystany do obliczania trajektorii balistycznych podczas II wojny światowej.
                                    4. Pierwszy komputerowy wirus nazywał się "Creeper".
                                    5. NASA nadal prowadzi projekty dotyczące programowania z lat 70-tych, wykorzystując języki: ADA i HAL/S.
                                    """)
                        if st.button('Powrót'):
                            st.session_state['eighth_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1, 1])
                            with new_c0:
                                industry_data = df['industry'].value_counts().reset_index().rename(columns={'industry': 'Branża', 'count': 'Ilość oddanych głosów'})
                                industry_df = pd.DataFrame(industry_data)
                                st.dataframe(industry_df, hide_index=True)
                            with new_c1:
                                st.write('Top 3 najczęstsze branże')
                                st.bar_chart(data=industry_df.head(3), x='Branża', y='Ilość oddanych głosów', horizontal=True, height=380)
                            st.markdown('#### Zatem wynika, że najczęstszą branżą, w której pracują ankietowani jest BRANŻA IT \U0001f5a5\uFE0F\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_eighth_button_pressed, use_container_width=True)
                
                
                if option == 'Sprawdzone metody nauki':
                    if st.session_state.get('sixth_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True
                        
                        st.image('https://incubator.ucf.edu/wp-content/uploads/2023/07/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1-1500x1000.jpg')
                        with st.expander('Jaka jest najlepsza metoda nauki AI i zostania Data Scientist?'):
                            st.markdown("""
                                        Wzięcie udziału w kursie "Od Zera Do AI" prowadzonym przez ekipę: Gotoit.pl :muscle:
                                        """)
                        
                        if st.button('Powrót'):
                            st.session_state['sixth_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1.3, 1])
                            with new_c0:
                                learning_pref_books = df['edu_level'][df['learning_pref_books'] == 1].count()
                                learning_pref_chatgpt = df['edu_level'][df['learning_pref_chatgpt'] == 1].count()
                                learning_pref_offline_courses = df['edu_level'][df['learning_pref_offline_courses'] == 1].count()
                                learning_pref_online_courses = df['edu_level'][df['learning_pref_online_courses'] == 1].count()
                                learning_pref_personal_projects = df['edu_level'][df['learning_pref_personal_projects'] == 1].count()
                                learning_pref_teaching = df['edu_level'][df['learning_pref_teaching'] == 1].count()
                                learning_pref_workshops = df['edu_level'][df['learning_pref_workshops'] == 1].count()
                                learning_df = pd.DataFrame({
                                                'Ulubione metody nauki' : ['książki', 'chat gpt', 'kursy offline', 'kursy online', 'osobiste projekty', 'nauczanie', 'warsztaty'],
                                                'Ilość oddanych głosów' : [learning_pref_books, learning_pref_chatgpt, learning_pref_offline_courses,
                                                    learning_pref_online_courses, learning_pref_personal_projects,
                                                    learning_pref_teaching, learning_pref_workshops]           
                                                })
                                sorted_learning_df = learning_df.sort_values(by= 'Ilość oddanych głosów', ascending = False)
                                st.dataframe(data=sorted_learning_df, hide_index=True, use_container_width=True)
                            with new_c1:
                                st.write('Top 3 ulubionych metod nauki')
                                st.bar_chart(data=sorted_learning_df.head(3), x='Ulubione metody nauki', y='Ilość oddanych głosów', horizontal=True, height=230, 
                                                y_label='Ulubione metody nauki', x_label='Ilość oddanych głosów')
                            st.markdown('#### Zatem wynika, że ulubioną metodą nauki ankietowanych są KURSY ONLINE \U0001f52c\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_sixth_button_pressed, use_container_width=True) 
                
                if option == 'Największe motywacje':
                    if st.session_state.get('seventh_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True
                        
                        st.image('https://zpopk.pl/wp-content/uploads/2024/07/inside-4-scaled.jpeg')
                        with st.expander('Czy wiesz, że negatywne emocje też są potrzebne?'):
                            st.markdown("""
                                    Negatywne emocje też są potrzebne. Często są dla nas sygnałem ostrzegawczym, który może uchronić nas od złych decyzji. Negatywne emocje sprawiają, że nasze myślenie staje się dużo bardziej krytyczne. Dzięki temu, trudniej jest nam ulec manipulacji.
                                    Kiedy całkowicie będziemy próbowali się pozbyć negatywnych emocji, możemy coś utracić w naszym życiu. Negatywne emocje same w sobie nie są złe. Są potrzebne nam do głębszego poznania samych siebie. To nadmiar negatywnych emocji jest szkodliwy, jednak ich całkowite wyeliminowanie, może być dla nas jeszcze gorsze.
                                        """)
                        
                        if st.button('Powrót'):
                            st.session_state['seventh_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1.27, 1])
                            with new_c0:
                                motivation_carrer = df['edu_level'][df['motivation_career'] == 1].count()
                                motivation_challenges = df['edu_level'][df['motivation_challenges'] == 1].count()
                                motivation_creativity_and_innovation = df['edu_level'][df['motivation_creativity_and_innovation'] == 1].count()
                                motivation_money_and_job = df['edu_level'][df['motivation_money_and_job'] == 1].count()
                                motivation_personal_growth = df['edu_level'][df['motivation_personal_growth'] == 1].count()
                                motivation_remote = df['edu_level'][df['motivation_remote'] == 1].count()
                                motivation_df = pd.DataFrame({
                                        'Ulubione motywacje' : ['kariera', 'nowe wyzwania', 'innowacje', 'praca i pieniądze', 'rozwój osobisty', 'praca zdalna'],
                                        'Ilość oddanych głosów' : [motivation_carrer, motivation_challenges, motivation_creativity_and_innovation,
                                                    motivation_money_and_job, motivation_personal_growth,
                                                    motivation_remote]
                                })
                                sorted_motivation_df = motivation_df.sort_values(by= 'Ilość oddanych głosów', ascending = False)
                                st.dataframe(data=sorted_motivation_df, hide_index=True, use_container_width=True)
                            with new_c1:
                                st.write('Top 3 ulubionych motywacji do nauki')
                                st.bar_chart(data=sorted_motivation_df.head(3), x='Ulubione motywacje', y='Ilość oddanych głosów', horizontal=True, height=230)
                            st.markdown('#### Zatem wynika, że największą motywacją do nauki ankietowanych jest ROZWÓJ OSOBISTY \U0001f9e0\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_seventh_button_pressed, use_container_width=True) 

                if option == 'Preferencje smakowe':
                    if st.session_state.get('ninth_button_pressed', False):
                        if not st.session_state.get('balloons_shown', False):
                            st.balloons()
                            st.session_state['balloons_shown'] = True

                        st.image('https://dentonet.pl/wp-content/uploads/2019/02/T%C5%82usty-Czwartek-850x562.jpg')
                        with st.expander('Kilka ciekawostek o tłustym czwartku'):
                            st.markdown("""
                                    1. To początek ostatnich dni karnawału, a w kalendarzu chrześcijańskim jest to ostatni czwartek przed Wielkim Postem.
                                    2. Jest świętem ruchomym - jego data zależy od Wielkanocy.
                                    3. Tradycja tłustego czwartku wywodzi się jeszcze z czasów pogaństwa.
                                    4. Tłusty czwartek nie jest tylko polskim zwyczajem, w różnych krajach europejskich istnieją różne wersje tego święta, np. w Wiekiej Brytanii obchodzi się "naleśnikowy dzień", Skandynawowie natomiast jedzą drożdżówki z cynamonem.
                                    5. Tego dnia statystyczny Polak zjada 2,5 pączka, natomiast każdego roku w tłusty czwartek zjadamy 100 mln pączków.
                                    6. W Stanach Zjednoczocnych odpowiednikiem pączków są tzw. doughnuty.
                                    """)
                        if st.button('Powrót'):
                            st.session_state['ninth_button_pressed'] = False
                            st.rerun()
                    else:
                            new_c0, new_c1 = st.columns([1.35, 1])
                            with new_c0:
                                taste_data = df['sweet_or_salty'].value_counts().reset_index().rename(columns={'sweet_or_salty': 'Smaki', 'count': 'Ilość oddanych głosów'})
                                taste_df = pd.DataFrame(taste_data)
                                st.dataframe(taste_df, hide_index=True)
                            with new_c1:
                                st.write('Co wolą ankietowani - słodkie czy słone?')
                                st.bar_chart(data=taste_df.head(3), x='Smaki', y='Ilość oddanych głosów', height = 120, horizontal= True)
                            st.markdown('#### Zatem wynika, że ankietowani są najczęściej ŁASUCHAMI \U0001f369\nZa to odkrycie otrzymujesz w nagrodę ciekawostkę!')
                            st.button('Przejdź do ciekawostki', on_click=check_ninth_button_pressed, use_container_width=True)
            
                if option == 'Relacje pomiędzy danymi':
                    #macierz korelacji
                    st.header('Macierz korelacji')
                    rename_corr_df = df.rename(columns = {
                        'gender' : 'płeć',
                        'hobby_art' : 'sztuka',
                        'hobby_books' : 'książki',
                        'hobby_movies' : 'filmy',
                        'hobby_other' : 'inne hobby',
                        'hobby_sport' : 'sport',
                        'hobby_video_games' : 'gry wideo',
                        'learning_pref_books' : 'uczenie z książek',
                        'learning_pref_chatgpt' : 'czat gpt',
                        'learning_pref_offline_courses' : 'kursy offline',
                        'learning_pref_online_courses' : 'kursy online',
                        'learning_pref_personal_projects' : 'osobiste projekty',
                        'learning_pref_teaching' : 'nauczanie',
                        'learning_pref_teamwork' : 'praca zespołowa',
                        'learning_pref_workshops' : 'warsztaty',
                        'motivation_career' : 'kariera',
                        'motivation_challenges' : 'wyzwania',
                        'motivation_creativity_and_innovation' : 'innowacje i kreatywność',
                        'motivation_money_and_job' : 'pieniądze i praca',
                        'motivation_personal_growth' : 'rozwój osobisty',
                        'motivation_remote' : 'praca zdalna'
                    })
                    corr_matrix = rename_corr_df.corr(numeric_only= True)
                    plt.figure(figsize= (16, 12))
                    sns.heatmap(corr_matrix, annot = True, fmt= '.2f', cbar = True)
                    #rysowanie macierzy
                    st.pyplot(plt.gcf())

                    st.markdown("""
                                **Trzy największe korelacje występujące w badanym zbiorze danych:**
                                1. Uczenie się podczas warsztatów uzupełnia się z uczeniem podczas pracy zespołowej, gdyż przeważnie wartsztaty stanowią pracę grupową.
                                2. Więcej mężczyzn traktuje gry wideo jako hobby.
                                3. Więcej mężczyzn traktuje sport jako hobby.
                                """
                                )

                    #wykresy dla top 3 relacji
                    st.header('Wykresy kategoryczne dla najsilniejszych korelacji')
                    
                    plt.figure(figsize=(10, 6))
                    plot = sns.catplot(
                        data=rename_corr_df,
                        kind = 'bar',
                        x='sport',
                        y='gry wideo',
                        hue='płeć',
                    )
                    st.pyplot(plot.figure) 

                    plt.figure(figsize=(10, 6)) #rozmiar okna wykresu
                    plot = sns.catplot(
                        data=rename_corr_df,
                        kind = 'bar',
                        x='warsztaty',
                        y='praca zespołowa',
                        hue='płeć',
                    )
                    st.pyplot(plot.figure) 

                    st.markdown("""
                                **Powyższe wykresy potwierdzają opisane najsilniejsze korelacje:**
                                * żadna ankietowa kobieta nie określiła sportu jako hobby,
                                * większość ankietowanych, co wskazali jako swoje hobby - gry wideo, to mężczyźni,
                                * największa zależność występuje pomiędzy metodami nauczania: na warsztacach oraz podczas pracy zespołowej (przy czym można zaobserwować, iż taka metoda nauki jest bliższa płci męskiej).
                                """
                                )
                    
                if option == "Wróć do menu głównego":
                    st.session_state['second_button_pressed'] = False
                    st.rerun()
                        
            else:
                #menu główne
                st.markdown("""
                <p style="color:red; fosnt-size:24px;">Znajdujesz się w menu głównym aplikacji</p>
                """, unsafe_allow_html=True)
                st.markdown("""
                            **Analizowane dane zawierają następujące informacje o ankietowanych:**
                            * do jakiej grupy wiekowej przynależą,
                            * poziom wykształcenia,
                            * ulubione zwierzę lub miejsce relaksu,
                            * płeć (gdzie wartości binarne w zbiorze danych odpowiadają kolejno: "0" - mężczyzna, "1" - kobieta)
                            * ulubione hobby (gdzie wartości binarne w zbiorze danych odpowiadają kolejno: "0" - NIE, "1" - TAK),
                            * ulubione metody nauki (gdzie wartości binarne w zbiorze danych odpowiadają kolejno: "0" - NIE, "1" - TAK)
                            * największe motywacje do nauki ((gdzie wartości binarne w zbiorze danych odpowiadają kolejno: "0" - NIE, "1" - TAK),
                            * preferencje smakowe,
                            * doświadczenie zawodowe i jaka branża.
                            """)
                st.markdown(':arrow_left: Po lewej stronie znajdują się wszystkie dostępne filtry')
                #st.markdown(' :exclamation::exclamation::exclamation: Aby uruchomić tło muzyczne należy wpisać ścieżkę do pliku audio w polu tekstowym *"Wpisz ścieżkę do pliku MP3"*.')
                st.markdown(':arrow_down: Poniżej znajdują się wszystkie dostępne opcje przeglądania danych.')
            
            if not st.session_state['second_button_pressed']:
                if st.button('Przejdź do opcji'):
                    st.session_state['second_button_pressed'] = True
                    st.rerun()


else:
        st.markdown("""
            #### Witamy w aplikacji służącej do przeglądania danych z ankiety powitalnej!\n
        **Naciśnij poniższy przycisk, a dowiesz się, m.in:**
        * z jakich grup wiekowych pochodzą ankietowani,
        * jakie mają hobby, ulubione zwierzęta czy miejsca,
        * co ich najbardziej motywuje w życiu,
        * jakie preferują praktyki nauczania,
        * czy są łasuchami słodkości czy może jednak zwolennikami słonych przekąsek,
        * i wiele, wiele więcej...
    """)
        st.write('Zanurz się w świecie danych, wizualizacji oraz ciekawostek:')
        st.button('Przeglądaj dane z ankiety', use_container_width= True, on_click=check_first_button_pressed)


# else:
#     st.write("Podaj hasło, aby uzyskać dostęp.")

