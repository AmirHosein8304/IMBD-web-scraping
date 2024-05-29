import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))


ps = PorterStemmer()


def clean_text(text):
    words = word_tokenize(text)
    return [ps.stem(w)
 for w in words if not w.lower() in stop_words]

with open('plot_summeries.txt', 'r'), open('cleaned_file2.txt', 'w') as file1,file2:
    for line in file1.readlines():
        new_line = clean_text(line)
        file2.write(' '.join(new_line))
        file2.write('\n')