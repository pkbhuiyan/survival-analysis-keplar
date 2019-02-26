import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

# extract player data from the website
def extract_player_data(table_rows):
    player_data = []

    for row in table_rows:

        player_list = [td.get_text()[:-4] if td.get_text().endswith(" HOF")
                       else td.get_text() for td in row.find_all(["td", "th"])]
        if not player_list:
            continue

        links_dict = {(link.get_text()[:-4]  # exclude the last 4 characters
                       if link.get_text().endswith(" HOF")  # if they are " HOF"
                       # else get all text, set that as the dictionary key
                       # and set the url as the value
                       else link.get_text()): link["href"]
                      for link in row.find_all("a", href=True)}

        player_list.append(links_dict.get(player_list[3], " "))

        player_list.append(links_dict.get("College Stats", " "))

        player_data.append(player_list)

    return player_data


# store the draft
draft_dfs_list = []

# a list to store any errors that may come up while scraping
errors_list = []
# The url template that we pass in the draft year inro
url_template = "http://www.pro-football-reference.com/years/{year}/draft.htm"

# for each year
for year in range(2007, 2018):

    # Use try/except block to catch and inspect any urls that cause an error
    try:

        url = url_template.format(year=year)
        print(url)

        html = urlopen(url)

        # create the BeautifulSoup object
        soup = BeautifulSoup(html, "html.parser")

        # get the column headers
        column_headers = [th.getText() for th in
                          soup.findAll('tr', limit=2)[1].findAll('th')]
        column_headers.extend(["Player_NFL_Link", "Player_NCAA_Link"])

        # select the data from the table using the '#drafts tr' CSS selector
        table_rows = soup.select("#drafts tr")[2:]

        # extract the player data from the table rows
        player_data = extract_player_data(table_rows)

        # create the dataframe for the current years draft
        year_df = pd.DataFrame(player_data, columns=column_headers)

        # add draft year
        year_df.insert(0, "Draft_Yr", year)
        draft_dfs_list.append(year_df)
        print(len(draft_dfs_list))

    except Exception as e:
        # Store the url and the error it causes in a list
        error = [url, e]
        errors_list.append(error)



# len(errors_list)

# store all drafts in one DataFrame
draft_df = pd.concat(draft_dfs_list, ignore_index=True)
# drop row where 'To' exists
draft_df.drop(draft_df[draft_df.To == 'To'].index, inplace=True)
player_ids = draft_df.Player_NFL_Link.str.extract("/.*/.*/(.*)\.",expand=False)
draft_df["Player_Id"] = player_ids


f=[]
k=[]
t=draft_df.To.tolist()
d=draft_df.Draft_Yr.tolist()

for i in range(0,len(t)):

    if t[i] == '':
        f.append('')
        k.append(0)
    else:
        s = int(t[i]) - d[i]
        f.append(s)
        k.append(1)
draft_df['duration'] = f
draft_df['retired'] = k
draft_df.drop(['Player_NFL_Link','Player_NCAA_Link',''], axis = 1, inplace = True)

draft_df.to_csv('main-big-data-2007-8.csv')