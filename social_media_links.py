from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import re
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


class social_links():
    file_path = None
    site = None

    def __init__(self):
        while(True):
            self.file_path = input("Enter your file path :: ")
            try:
                self.file_path = pd.read_excel(self.file_path)
                self.file_path = pd.DataFrame(self.file_path)
                break
            except FileNotFoundError:
                print(
                    "Invalid file path, Please Enter a valid file name or complete path")
                continue
            except PermissionError:
                print(
                    "Permission denied, Please Enter a valid file name or complete path")

    def get_social_media_site(self):
        while(True):
            self.site = input(
                "choose Social media website name (1 for facebook, 2 for twitter and 3 for instagram ) :: ")
            if self.site == '1':
                self.site = 'facebook'
                break
            elif self.site == '2':
                self.site = 'twitter'
                break
            elif self.site == '3':
                self.site = 'instagram'
                break
            else:
                print("Invalid choice. Please choose from available options")
                continue

    def col_matching_fun(self):
        flag_col_match = 0
        choose_col = ''
        choose_col = input("Enter your column name :: ")
        for col in self.file_path.columns:
            if choose_col == col:
                flag_col_match = 1
                # print("File column and user column are matched")
        return flag_col_match, choose_col

    def extract_links(self, user_col):
        while(True):
            flag1 = 0
            save_col = input("Enter your column name to save the result :: ")
            for col in self.file_path.columns:
                if save_col == col:
                    flag1 = 1
                    # print("Saved column matched")
                    break
            if flag1 == 1:
                break
            else:
                print("column not found ")
                continue
        account_url = 'Not found'
        index = 0
        for url in self.file_path[user_col]:
            try:
                url = url if url.startswith('https') else ('https://' + url)
                # response = requests.get(url)
                # print(url)
            # pass header when you are getting error like 403
                page = requests.get(
                    url, headers={'User-Agent': 'Chrome/93.0.4577.63'})
                # print(page.status_code)
                htmlcontent = page.content
            except ConnectionError:
                # print(url)
                self.file_path[save_col].loc[index] = 'invalid link'
                print(f"Something wrong with  {url} check it again")
                index = index + 1
                continue
            souphtmlcontent = BeautifulSoup(htmlcontent, 'html.parser')
            for a in souphtmlcontent.find_all('a'):
                try:
                    a_href = a['href']
                    # pprint(a_href)
                    social_link = re.search(self.site, a_href)
                    if social_link is not None:
                        print("social media link found :: ",
                              social_link.string)
                        account_url = social_link.string
                        # print("found")
                except KeyError:
                    pass
            self.file_path[save_col].loc[index] = account_url
            account_url = 'Not found'
            index = index + 1

        save_file = input("Enter your File name ")
        self.file_path.to_excel(save_file + ".xlsx", index=False)


# creating an object
social_obj = social_links()
social_obj.get_social_media_site()
flag, col = social_obj.col_matching_fun()
while(True):
    if flag != 1:
        print("Your column is not matched with any file column")
        flag, col = social_obj.col_matching_fun()
    else:
        break
social_obj.extract_links(col)
