import requests
import bs4
import numpy as np
import math
from nltk.corpus import stopwords
import re

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 "}

##########################
plot_summeries = []
def get_plot(url):
    with requests.Session() as session:
        plot = session.get(url,headers=headers)
        plot_soup = bs4.BeautifulSoup(plot.text,"html.parser")
        plots = plot_soup.find_all("div",{"class" : "ipc-html-content-inner-div"})
        plot = plots[0].text
        plot_summeries.append(plot)

page = requests.get("https://www.imdb.com/chart/top/", headers=headers)
soup = bs4.BeautifulSoup(page.text, "html.parser")
names = soup.find_all("div",{"class" : "ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title"})
infos = soup.find_all("span" , {"class" : "sc-b189961a-8 kLaxqf cli-title-metadata-item"})
links = str(soup.find_all("a", {"class" : "ipc-title-link-wrapper"})).split()

for item in links:
    if 'href=' not in item:
        links.remove(item)
final_links = []
for item in links:
    if 'href=' in item:
        final_links.append((item.split('href="')[1]).split('?ref_=')[0])
final_links = final_links[:-7]
for i in range(len(final_links)):
    junked = list(final_links[i])
    junked = ['https://www.imdb.com']+junked
    junked = junked + ['plotsummary/?ref_=tt_stry_pl']
    final_links[i]=''.join(junked)

movies_name = []
movies_year = []
for i in names:
    name = i.text
    movies_name.append(name.split('. ')[1])
for i in range(len(infos)):
    infos[i]=infos[i].text
for i in range(len(infos)):
    if infos[i].isnumeric():
        if infos[i+2].isnumeric():
            infos.insert(i+2,"Not Rated")
for j in range(0,len(infos)-2,3):
    year = [movies_name[j//3],infos[j], infos[j+1], infos[j+2],final_links[j//3]]
    movies_year.append(year)
movies_year = np.array(movies_year)
for url in final_links:
    get_plot(url)
with open("plot_summeries.txt" , "w+") as f:
    for plot in plot_summeries:
        f.write(plot)
        f.write("\n")
        f.write("____________________________________________________")
        f.write("\n")
###############################
infile = "plot_summeries.txt"
outfile = "cleaned_file.txt"
delete_list = stopwords.words('english')
delete_sen = r'\b' + r'\b|\b'.join(delete_list) + r'\b'
with open(infile) as fin, open(outfile, "w+") as fout:
    lines = fin.readlines()
    for line in lines:
        new_line = re.sub(f'(?!\w*\..\w*|\w*\..\w*\..\w*)({delete_sen})', "", line.lower())
        fout.write(new_line)
#########################
words = []
with open("cleaned_file.txt","r") as f  :
    text = f.read()
    docs = text.split('\n____________________________________________________\n')[:-1]
    for doc in docs:
        doc = doc.split()
        for word in doc:
            words.append(word)
words = set(words)
TF_values = []
for doc in docs:
    dic = []
    doc = doc.split()
    for word in words:
        dic.append(doc.count(word)/len(doc))
    TF_values.append(dic)
IDF_dict = []
for word in words:
    word_counter = 0
    for doc in docs:
        if word in doc:
            word_counter+=1
    IDF_dict.append(math.log(len(docs)/word_counter) + 1)
for dict in TF_values:
    for i in range(len(dict)):
        dict[i] = dict[i] * IDF_dict[i]
query = re.sub(f'(?!\w*\..\w*|\w*\..\w*\..\w*)({delete_sen})', "", input('Enter your film plot summery').lower()).split()
TF_query = []
for word in words:
    TF_query.append(query.count(word)/len(query))
IDF_query = []
for word in words:
    IDF_query.append(math.log(len(query)) + 1)
for i in range(len(TF_query)):
    TF_query[i] = TF_query[i] * IDF_query[i]
TF_query = np.array(TF_query)
cosine_similarity = []
for item in TF_values:
    wanted_vector = np.array(item)
    cosine_similarity.append(np.inner(wanted_vector, TF_query)/((np.inner(wanted_vector,wanted_vector)**0.5)*(np.inner(TF_query,TF_query)**0.5)))
print(cosine_similarity.index(max(cosine_similarity)),'.',movies_name[cosine_similarity.index(max(cosine_similarity))])
