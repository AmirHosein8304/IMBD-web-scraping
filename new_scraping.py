import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import bs4


headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 "}
page = requests.get("https://www.imdb.com/chart/top/", headers=headers)
soup = bs4.BeautifulSoup(page.text, "html.parser")
names = soup.find_all("div",{"class" : "ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title"})
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))



def clean_text(text):
    words = word_tokenize(text)
    return [w for w in words if not w.lower() in stop_words]

with open('plot_summeries.txt', 'r') as file1:
    with open('cleaned_file2.txt', 'w') as file2:
        for line in file1.readlines():
            new_line = clean_text(line)
            file2.write(' '.join(new_line))
            file2.write('\n')

# new changes
words = []
with open("cleaned_file2.txt","r") as f  :
    text = f.read()
    docs = text.split('\n____________________________________________________\n')[:-1]
    for doc in docs:
        words.append(doc)

movies_name = []
for i in names:
    name = i.text
    movies_name.append(name.split('. ')[1])

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
vectorizer = TfidfVectorizer()
vectorizer.fit(words)
tfidf_matrix = vectorizer.transform(words)

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(tfidf_matrix, movies_name)

new_input = input("youre movie search : ")
input_tfidf = vectorizer.transform([new_input])

distances, indices = knn.kneighbors(input_tfidf)
for i in indices[0]:
    print(movies_name[i])