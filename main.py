import requests
from bs4 import BeautifulSoup

URL = "https://qcpi.questcdn.com/cdn/browse_posting/?search_id=&postings_since_last_login=&draw=1&columns[0][data]=render_my_posting&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=render_post_date&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=render_project_id&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=render_category_search_string&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=render_name&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=bid_date_str&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=render_city&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=render_county&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=state_code&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=render_owner&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=true&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=render_solicitor&columns[10][name]=&columns[10][searchable]=true&columns[10][orderable]=true&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=posting_type&columns[11][name]=&columns[11][searchable]=true&columns[11][orderable]=true&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=render_empty&columns[12][name]=&columns[12][searchable]=true&columns[12][orderable]=true&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=render_empty&columns[13][name]=&columns[13][searchable]=true&columns[13][orderable]=true&columns[13][search][value]=&columns[13][search][regex]=false&columns[14][data]=render_empty&columns[14][name]=&columns[14][searchable]=true&columns[14][orderable]=true&columns[14][search][value]=&columns[14][search][regex]=false&columns[15][data]=render_empty&columns[15][name]=&columns[15][searchable]=true&columns[15][orderable]=true&columns[15][search][value]=&columns[15][search][regex]=false&columns[16][data]=project_id&columns[16][name]=&columns[16][searchable]=true&columns[16][orderable]=true&columns[16][search][value]=&columns[16][search][regex]=false&start=0&length=25&search[value]=&search[regex]=false&_=1700633516227"

HEADERS = {
    "Accept":"application/json, text/javascript;",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;",
    "Referer":"https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "X-Requested-With":"XMLHttpRequest"
}

POSTING_HEADERS = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;",
    "Referer":"https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "X-Requested-With":"XMLHttpRequest"
}

def scrape_questcdn(url, num_postings):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        for i in range(num_postings):
            posting_id = data['data'][i]['project_id']
            posting_url = 'https://qcpi.questcdn.com/cdn/util/get_posting/?current_project_id='+posting_id+'&next_project_id=&prev_project_id='
            posting_response = requests.get(posting_url,headers=POSTING_HEADERS)
            if posting_response.status_code == 200:
                soup = BeautifulSoup(posting_response.text, 'html.parser')
                tables = soup.find_all('table')
                tables = tables[2:4]
                row = []
                for table in tables:
                    for tr in table.find_all('tr'):
                        row_data = [td.text.strip() for td in tr.find_all('td')]
                        row.append(row_data[1])
                print("="*50)
                print("Posting ID:", posting_id)
                print("Est. Value Notes:", row[2])
                print("Description:", row[5])
                print("Closing Date:", row[0])
                print("="*50)
            else:
                print(f"Error: {posting_response.status_code}")
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    scrape_questcdn(URL, num_postings=5)
