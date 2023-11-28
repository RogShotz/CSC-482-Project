from bs4 import BeautifulSoup
import requests
import csv
import re

url = 'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States'


def main():  # TODO: fun facts?
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

    soup = BeautifulSoup(html_content, 'html.parser')

    soup = soup.find_all('table')
    for s in soup:
        # print(s.get("class"))
        if s.get("class")[0] == 'wikitable':
            soup = s
            break
    soup = soup.tbody
    pres_info = soup.find_all('tr')

    pres_strip = []
    for s in pres_info[1:]:  # skips table header
        pres_num = s.find('th').text.strip('\n')
        indiv_pres = s.find_all('td')
        pres_clean = [pres_num]
        for s2 in indiv_pres[1:]:
            clean_info = s2.text.strip('\n')
            if clean_info:
                # [c] == lack of political parties, [d], [g], [l] == diff party as P and VP, [e] == death in office, [f], [n] == new party, [h] = resigned
                # [j] == expelled from party, [t] = new VP
                # replaces any off charcters with tokens
                pres_clean.append(re.sub(r'\[[a-zA-z]\]', '',
                                    clean_info.replace(
                                    '\n\n', '<--->').replace('\n', '<-->')
                                  .replace('–', '<->').replace('[c]', '<noparties>')
                                  .replace('[d]', '<diffpparty>').replace('[e]', '<death>')
                                  .replace('[f]', '<newparty>').replace('[g]', '<diffparty>')
                                  .replace('[h]', '<resign>').replace('[j]', '<expelled>')
                                  .replace('[l]', '<diffparty>').replace('[n]', '<newparty>')
                                  .replace('[t]', '<newVP>')).replace(',', '<comma>'))
                # tag new lines
        pres_strip.append(pres_clean)

    pres_out = cleaner(pres_strip)

    with open('stripped_pres_info.txt', 'w', newline='') as f:
        fields = ['Number', 'Name', "Birth", "Death",
                  'Term', 'Party', 'Election', 'VP']
        csvwriter = csv.writer(f)
        csvwriter.writerow(fields)
        for pres in pres_out:
            print(pres)
            csvwriter.writerow(pres)


def cleaner(pres_arr):
    """Sanitizes president data to be sent to a CSV"""
    clean_arr = []
    for pres in pres_arr:
        pres_num = int(pres[0])
        sep_list = pres[1].split('(')
        pres_name = sep_list[0]
        sep_list = sep_list[1].split(')')[0]
        sep_list = sep_list.split('<->')
        pres_birth = -1
        pres_death = -1
        if len(sep_list) == 2:
            pres_birth = int(sep_list[0])
            pres_death = int(sep_list[1])
        else:
            pres_birth = int(sep_list[0].replace('b. ', ''))
            pres_death = -1
        sep_list = pres[2].split('<->')
        pres_term = '-'.join(sep_list)
        pres_party = pres[3].replace('<--->', '|')
        sep_list = pres[4].replace('<->', '-').split('<--->')
        pres_election = '|'.join(sep_list).replace('<-->', '')
        sep_list = pres[5].split('<--->')
        pres_VP = '|'.join(sep_list)
        pres_VP = pres_VP.replace(':', ': ').replace('\xa0', ': ').replace('through', 'through ').replace('after', 'after ').replace('through out', 'throughout ') #replaces odd : char with normal one
        pres_VP = pres_VP.replace(': <->', ':') #odd richard nixon moment
        pres_VP = pres_VP.replace('<-->', '')
        clean_arr.append([pres_num, pres_name, pres_birth, pres_death,
                         pres_term, pres_party, pres_election, pres_VP])
        print([pres_num, pres_name, pres_birth, pres_death,
              pres_term, pres_party, pres_election, pres_VP])
    return clean_arr


if __name__ == "__main__":
    main()
