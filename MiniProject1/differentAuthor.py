import matplotlib.pyplot as plt 
import requests, re
from bs4 import BeautifulSoup
from collections import Counter


def make_graph(article1, article2):
     
    fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(10,5)) #makes two plots with it being max width
    ax1.barh([wordCount[0] for wordCount in article1], [wordCount[1] for wordCount in article1], color='green')#
    ax2.barh([wordCount[0] for wordCount in article2], [wordCount[1] for wordCount in article2], color='orange')#
    ax1.set_title('Mark Goldstein')
    ax2.set_title('Amy Davies')   
    ax1.set(xlabel='Words', ylabel='Frequency')
    ax2.set(xlabel='Words', ylabel='Frequency')
    #move the distance between the two subplots
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
    plt.show()

def freq_checker(all_articles):
    freqs = [] #so an array of two dicts
    for i in range(len(all_articles)):
        c = Counter(all_articles[i])#dictionary of words and their counts
        freqs.append(c)
    return freqs


def parse(articles):
    articles_words = [] #2d array with first element being the words array for first book
    to_remove = {
        "with": 0,
        "the": 0,
        "a": 0,
        "on": 0,
        "of": 0,
        "to": 0,
        "and": 0,
        "an": 0,
        "for": 0,
        ".\n": 0,
        ".": 0,
        "it": 0,
        "is": 0,
        "in": 0,
        "at": 0,
        "ii": 0,
        "lens": 0,
        "/": 0,
        "which": 0,
        "it's": 0,
        "when": 0,
        "as": 0,
        "review": 0,
        "this": 0,
        "that": 0,
        "review": 0,
        "has": 0,
        "or": 0,
        "·": 0,
        "be": 0,
        "gm": 0,
        "fe": 0,
        "you": 0,
        "we": 0,
        "by": 0,
        "can": 0,
        "will": 0,
        "are": 0,
        "|" : 0,
        "have" : 0,
        "camera" : 0,
        "x" : 0,
        "new" : 0,
        "-" : 0,
        "z" : 0,
        "download" : 0,
        "up" : 0,
        "if" : 0,
        "-" : 0,
        "from" : 0,
        "but" : 0
    }
    for book in articles:
        r = requests.get(book)
        soup = BeautifulSoup(r.text, 'html.parser')#soup now contains all the html code
        text = soup.get_text().lower()
        words = re.split('\s+', text)#split on whitespace

        for i in range(len(words)):
            #replace unwanted chars
            words[i] = words[i].strip()#bc replaced earlier with space so remove whitespace now
            
            #remove common words 
            finalWords = [word for word in words if word not in to_remove]
            
        articles_words.append(finalWords)
    return articles_words


if __name__ == "__main__":
    articles = []
    article1 = 'https://www.photographyblog.com/reviews/fujifilm_x_h2s_review'#mark 
    article2 = 'https://www.photographyblog.com/reviews/nikon_z7_ii_review'#amy 
    articles.append(article1)
    articles.append(article2)
    all_words = parse(articles)
    freqs = freq_checker(all_words)
    print("\nMark Goldstein")
    for keyVal in freqs[0].most_common(25):
        print(keyVal[0], ":", keyVal[1])
    print('\n\nAmy Davies')
    for keyVal in freqs[1].most_common(25):
        print(keyVal[0], ":", keyVal[1])
        
    make_graph(freqs[0].most_common(25), freqs[1].most_common(25))
    
