import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# URL du site web
url = "https://www.scrapethissite.com/pages/forms/"

# Récupérer les données de chaque page
data = []
for i in range(1, 11):
    page_url = url + "?page=" + str(i)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for row in soup.find_all('tr', class_='team'):
        team_name = row.find('td', class_='name').text.strip()
        wins = int(row.find('td', class_='wins').text.strip())
        losses = int(row.find('td', class_='losses').text.strip())
        goals_for = int(row.find('td', class_='gf').text.strip())
        goals_against = int(row.find('td', class_='ga').text.strip())
        diff = goals_for - goals_against

        win_percentage_tag = row.find('td', class_='percent')
        if win_percentage_tag is not None:
            win_percentage = float(win_percentage_tag.text.strip('%')) / 100
        else:
            win_percentage = None

        year_tag = row.find('td', class_='year')
        if year_tag is not None:
            year = int(year_tag.text.strip()[:4])
        else:
            year = None

        if diff > 0 and goals_against < 300:
            # Nettoyer les données extraites
            team_name = team_name.replace('\n', '')
            team_name = team_name.replace('\t', '')
            team_name = team_name.replace('\r', '')
            data.append([year, wins, losses, win_percentage, goals_for, goals_against, diff, team_name])

# Structurer les données avec pandas et trier par ordre croissant
df = pd.DataFrame(data, columns=['Year', 'Wins', 'Losses', 'Win %', 'Goals For (GF)', 'Goals Against (GA)', '+ / -', 'Team Name'])
df_sorted = df.sort_values(by='+ / -', ascending=True)

# Écrire les données filtrées et structurées dans le fichier CSV
df_sorted.to_csv('result.csv', index=False, encoding='utf-8-sig')

