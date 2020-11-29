import os
from dotenv import load_dotenv

import re
import urllib.parse
import requests
import bs4


# LOGIN ================================================================================================================

# mobile version of FB does not require JS
def facebook_login(email_address, password):
    facebook_url = 'https://mobile.facebook.com/'

    session = requests.Session()
    r = session.get(facebook_url, allow_redirects=False)
    soup = bs4.BeautifulSoup(r.text, features='html.parser')

    action_url = soup.find('form')['action']
    inputs = soup.find('form').findAll('input', {'type': ['hidden', 'submit']})
    post_data = {input.get('name'): input.get('value') for input in inputs}
    post_data['email'] = email_address
    post_data['pass'] = password.upper()

    scripts = soup.findAll('script')
    scripts_string = '/n/'.join([script.string for script in scripts if script.string])
    datr_search = re.search('\["_js_datr","([^"]*)"', scripts_string, re.DOTALL)

    if not datr_search:
        return False

    datr = datr_search.group(1)
    cookies = {'_js_datr' : datr}
    return session.post(facebook_url + action_url, data=post_data, cookies=cookies, allow_redirects=False)


# SCRAPE GROUPS ========================================================================================================

class FB_tag:
    @classmethod
    def search_data_ft(cls, soup: bs4.element.Tag, tn: str):
        matches = soup.find_all(lambda t: t.attrs.get('data-ft') and re.search(f'"tn":"{tn}"', t.attrs.get('data-ft')))
        return matches

    def strip_str(cls, soup: bs4.element.Tag):
        return list(soup.stripped_strings)


class FB_group(FB_tag):

    def __init__(self, group_id: int):

        print(f'Initializing {group_id}.')

        self.group_id = group_id
        self.page_url = f"https://mobile.facebook.com/{self.group_id}"
        self.page_text = requests.get(self.page_url).text
        self.soup = bs4.BeautifulSoup(self.page_text, "html.parser")

        if not self.search_data_ft(self.soup, '-R'):
            print('\tPrivate group.')
            self.name = 'Private group'
            self.stories = ['Private']
        else:
            self.name = self.strip_str(
                self.soup.find('a', {'href': '#groupMenuBottom'}) or
                self.soup.find(id='m-timeline-cover-section').div
            )[0]

            self.stories = [Story(s) for s in self.search_data_ft(self.soup, '-R')]
            self.videos = [v for s in self.stories for v in s.videos if s.videos]
            self.events = [s.event for s in self.stories]

    def __repr__(self):
        return self.name


class Story(FB_tag):
    def __init__(self, soup: bs4.element.Tag):
        self.soup = soup
        self.body = self.soup.find('div', {'data-ft': '{"tn":"*s"}'})
        self.body = self.body if self.body.text else self.soup
        self.footer = self.soup.find('div', {'data-ft': '{"tn":"*W"}'})

        date_re = r'((\w+ \d+(, \d{4})?)|(Yesterday)) at [\d:]+ [APM]{,2}'
        self.date = list(filter(re.compile(date_re).search, self.footer.stripped_strings))
        self.date = self.date[0] if self.date else 'No date'

        # TODO: grab videos sourced as YouTube link
        videos_1 = self.soup.find_all('a', {'target': '_blank'})
        videos_2 = self.search_data_ft(self.soup, 'E')
        videos_2 = videos_2[0].find_all('a') if videos_2 else []

        videos = [urllib.parse.unquote(v.get('href')) for v in videos_1 + videos_2]
        videos = [match for v in videos for match in re.findall(r'^(?![\w/.-]*/photo[\w.]+)(.*)[&?]source=', v)]

        videos = [v.replace('//video.fybz2-2.fna', '//video.xx') for v in videos]  # videos_1
        videos = [re.sub(r'^.*src=', '', v) for v in videos]
        videos = [f"https://m.facebook.com{v}" if not re.search('^https', v) else v for v in videos]
        self.videos = videos

        self.event = None
        event = self.soup.find('div', {'data-ft': '{"tn":"H"}'})

        event = [
            ' '.join(self.strip_str(child))
            for td in event.find('tbody').find_all('td')
            for child in td.children] \
            if event and event.find('tbody') else None

        if event and re.search(r'\d [A-Z]{3}', event[0]):
            self.event = {'date': event[0], 'title': event[1], 'location': event[2], 'text': event}

    def __repr__(self):
        return self.strip_str(self.body)[0]

# ======================================================================================================================

load_dotenv()

if __name__ == '__main__':
    login = facebook_login(os.environ.get('FACEBOOK_USERNAME'), os.environ.get('FACEBOOK_PASSWORD'))

    karate_groups = {
        'WTKO': 'WTKO-621106741273501',
        'JKA Mississauga': 'worldclasskaratemississauga',
        'JKA Vaughan': 'worldclasskaratevaughan',
        'JKA SKD Canada': 'jkaskdworldorganizationofCanada',
        'JKA International of Canada': 'JKA-International-of-Canada-Inc-309881155820942',
        'JKA': '572555819442354',
        'Karate@Home': 'KarateAtHome',
        'SKIF_USA': 'SKIF.USA',
        'SKIF': '113945898690758',
        'SKIF Houston': '287264601323857',
        'SKIF Yudansha-kai': '568928656486421',
        'WTKO Members Only': 'groups/1362817897146898', # private group
        'Doshinkai Shotokan Karate USA': 'groups/1715467755413558'}  # private group
    # 'JKA Kuro Obi': '32636736867',

    groups = [FB_group(g) for g in karate_groups.values()]

    # for n_g, g in enumerate(groups):
    #     print(f'group {n_g} {g}: {g.page_url}')
    #     if g.name != 'Private group':
    #         for n_s, s in enumerate(g.stories):
    #             print(f'\tstory {n_s}')
    #             print(f'\t\tbody: {g.strip_str(s.body)}')
    #             print(f'\t\tfooter: {g.strip_str(s.footer)}')
    #             print(f'\t\tvideos: {s.videos}')
    #             print(f'\t\tevent: {s.event}')
