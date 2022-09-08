import matplotlib.pyplot as plt 
import requests, re
from bs4 import BeautifulSoup
from collections import Counter


def make_graph(book1, book2):
     
    fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(10,5)) #makes two plots with it being max width
    ax1.barh([wordCount[0] for wordCount in book1], [wordCount[1] for wordCount in book1], color='green')#
    ax2.barh([wordCount[0] for wordCount in book2], [wordCount[1] for wordCount in book2], color='orange')#
    ax1.set_title('A Christmas Carol')
    ax2.set_title('Great Expectations')   
    ax1.set(xlabel='Words', ylabel='Frequency')
    ax2.set(xlabel='Words', ylabel='Frequency')
    #move the distance between the two subplots
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
    plt.show()

def freq_checker(all_books):
    freqs = [] #so an array of two dicts
    for i in range(len(all_books)):
        c = Counter(all_books[i])#dictionary of words and their counts
        freqs.append(c)
    return freqs

def remove_headers(w):
    index = -1
    flag = False
    for i in range(len(w)):
        if(w[i] == "***" and w[i+1] == "start"):
            index = i
            flag = True
            break
    if flag == False:   
        index = w.index('***')#find index of ***
    #so now index either first instance of *** if only 4 of them or the 3 instance if there are 6 of them
    words = w[index+1:len(w)]
    #finds the index of the corresponding *** of the beginnning header
    index = words.index('***')
    words = words[index+1:len(words)]
    # #finds the index of the first *** of the ending header. so get everything up to this
    index = words.index('***')
    words = words[0:index]
    return words


def parse(books):
    book_words = [] #2d array with first element being the words array for first book
    index = 0
    for book in books:
        r = requests.get(book)
        soup = BeautifulSoup(r.text, 'html.parser')#soup now contains all the html code
        text = soup.get_text().lower()
        words = re.split('\s+', text)#split on whitespace
        # now only use the words in between the headers
        words = remove_headers(words)

        #now remove all the unnecessary chars from each word
        for i in range(len(words)):
            #replace unwanted chars
            words[i] = words[i].strip()#bc replaced earlier with space so remove whitespace now
            #remove the emdash
            if '—' in words[i]:
                #replace -- with space
                words[i] = words[i].replace("—", " ")
                #so then add everything after the space to the arr
                words.append(words[i][words[i].index(" ") + 1: len(words[i])])
                #replace curr element with eeverything up to space
                words[i] = words[i][0:words[i].index(" ")]
            #split two dashes
            if("--" in words[i]):
                #replace -- with space
                words[i] = words[i].replace("--", " ")
                #so then add everything after the space to the arr
                words.append(words[i][words[i].index(" ") + 1: len(words[i])])
                #replace curr element with eeverything up to space
                words[i] = words[i][0:words[i].index(" ")]

        book_words.append(words)
        index += 1
    return book_words


if __name__ == "__main__":
    books = []
    book1 = 'https://gutenberg.org/files/24022/24022-h/24022-h.htm' #chrismtas carol
    book2 = 'https://gutenberg.org/files/1400/1400-h/1400-h.htm' #great expectations
    books.append(book1)
    books.append(book2)
    all_words = parse(books)
    freqs = freq_checker(all_words)
    print("\nA Christmas Carol")
    for keyVal in freqs[0].most_common(15):
        print(keyVal[0], ":", keyVal[1])
    print('\n\nGreat Expectations')
    for keyVal in freqs[1].most_common(15):
        print(keyVal[0], ":", keyVal[1])
        
    make_graph(freqs[0].most_common(15), freqs[1].most_common(15))
    
