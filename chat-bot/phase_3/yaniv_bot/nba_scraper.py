import requests
import time
import pandas as pd

from bs4 import BeautifulSoup

months = ['january', 'february', 'march', 'april', 'may', 'june', 'october', 'november', 'december']
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']

def scrape_nba_data():
    rows = []
    for year in years:
        for month in months:
            time.sleep(5)

            response = requests.get(f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html')
            soup = BeautifulSoup(response.content, "html.parser")

            schedule_table = soup.find('table', id='schedule')
            if not schedule_table:
                continue

            for row in schedule_table.find_all('tr')[1:]:
                data_cells = row.find_all('td')
                if not data_cells:
                    continue

                date = data_cells[1]['csk'][4:12]
                visitor_team = data_cells[1].find('a').text
                visitor_team_points = data_cells[2].text
                home_team = data_cells[3].find('a').text
                home_team_points = data_cells[4].text
                attendance = data_cells[7].text
                arena = data_cells[8].text

                rows.append({
                    'date': date,
                    'visitor_team': visitor_team,
                    'visitor_team_points': visitor_team_points,
                    'home_team': home_team,
                    'home_team_points': home_team_points,
                    'attendance': attendance,
                    'arena': arena
                })

    df_nba = pd.DataFrame(rows)
    df_nba.to_csv('nba_data.csv')

if __name__ == '__main__':
    scrape_nba_data()