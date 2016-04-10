from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_name(ubit):
    url = "http://www.buffalo.edu/directory/search?query=" + ubit + "&submit.x=0&submit.y=0&submit=Search&affiliation=student&qualifier=username"
    html_string = urlopen(url).read()
    blab = [None]

    search_results = BeautifulSoup(html_string).find(attrs={'class': 'content_list clearsub search_results directory'})

    for hit in search_results.find_all('a'):
        if "Additional" not in hit.text and "vCard" not in hit.text:
            blab = [hit.text.split(' ')[0], hit.text.split(' ')[-1]]
    name = []
    for each in blab:
        name.append(each.strip(' \t\n\r'))
    print(name)

    return name