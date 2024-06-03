from bs4 import BeautifulSoup as bs
import requests as r
from re import findall
import os
from shutil import copyfileobj
import consolemenu as cm
from time import sleep
from combine_to_pdf import combine_subfolder

def link_to_soup(url) :
    return bs(r.get(url).text, features="lxml")

def get_manga_title(soup):
    return findall(r'.+(?= Scan VF)', soup.find_all("h1", class_="mb-0 d-inline-block h2")[0].text)[0]

def get_chap_divs(soup):
    return soup.find_all("div", class_="col-12 col-lg-6 py-3 col-chapter")

def get_chap_links(bs4_elements) :
    links = {} # {Chapter/Volume name : link}

    for div in bs4_elements:
        a_child = div.findChildren("a", recursive=False)[0]
        chap_name_div = a_child.findChildren(name="h5", attrs={'class' : 'mb-0'}, recursive=True)[0].text
        try :
            chap_name = findall(r'(?<=\s|\n)\w.+(?=\n\s*\d)', chap_name_div)[0]
        except :
            raise ValueError(f'Failed to extract the chap name from string {repr(chap_name_div)}')
        links[chap_name] = "https://scanvf.org"+a_child['href']

    return dict(reversed(links.items()))

def get_cdn_link(chap_url):
    # url input should be of type https://scanvf.org/scan/XXXX
    
    soupChap = link_to_soup(chap_url)
    scan_img = soupChap.find_all("img", class_="img-fluid")[1]
    
    cdn_link = findall(r'.+(?=\?)', scan_img['src'])[0]

    # Returns the link to the first image of the scan
    return cdn_link

def create_data(links, title):
    data = {
        'title': title,
        'chaps': {}
    }

    for chap in links.keys():
        data['chaps'][chap] = {
            'links': {
                'viewer': links[chap],
                'cdn': ''
            },
        }
    
    return data

def create_folder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath
            
def download_file(url, output, session):
    file_name = findall(r'(?<=/)\d+\..+$', url)[0]
    with session.get(url, stream=True) as r:
        if r.status_code == 200 :
            with open(f'{output}/{file_name}', 'wb') as f:
                copyfileobj(r.raw, f)
        return r.status_code

def download_selected(data) :
    for chap in data.keys():
        if data[chap]['download']:
            download_chap_images(data[chap]['links']['cdn'], chap)

def download_chap_images(viewer_url, title, chap_name):
    first_img_url = get_cdn_link(viewer_url)

    base_url = findall(r'^.+(?=/.+$)', first_img_url)[0]
    file_type = findall(r'(?<=\.)\w+$', first_img_url)[0]

    session = r.Session()
    adapter = r.adapters.HTTPAdapter(pool_connections=5, pool_maxsize=5)
    session.mount('https://', adapter)

    path = create_folder(f'{os.path.dirname(__file__)}/outputs/{title}/{chap_name}')

    counter = 1
    url = f'{base_url}/{str(counter)}.{file_type}'
    response_status = 200
    while response_status == 200:
        url = f'{base_url}/{str(counter)}.{file_type}'
        response_status = download_file(url, path, session)
        counter += 1
        print(f'Downloaded from {url} to {path}\nStatus code : {response_status}\n')
        sleep(0.3)
    print(f'\nStopped download at page {counter-1}\nStatus code : {response_status}\n')
    if input('Combine this chapter into a pdf ? (y) ') == 'y' :
        combine_subfolder(chap_dir=path)
    sleep(1)

def download_menu(data):
    menu = cm.MultiSelectMenu(title="What should be downloaded ?", subtitle="Inputs X,Y,Z and X-Z both work", epilogue_text="WARNING : Selecting will automatically start downloading !")
    
    for chap in data['chaps'].keys():
        menu.append_item(cm.items.FunctionItem(text=chap, function=download_chap_images, args=[data['chaps'][chap]['links']['viewer'], data['title'], chap], should_exit=True))

    menu.show()

def main():
    catalog = input("Manga URL : ")
    data = {}
    soup = link_to_soup(catalog)

    title = get_manga_title(soup)
    divs = get_chap_divs(soup)
    links = get_chap_links(divs)
    
    data = create_data(links, title)
    
    create_folder(f'{os.path.dirname(__file__)}/outputs/{title}')

    download_menu(data)

if __name__ == '__main__':
    main()