from pymongo import MongoClient
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import operator

import re

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# from gensim.corpora import Dictionary
from gensim import corpora, models, similarities


import numpy as np

client = MongoClient()
db = client.yelp
#print(db.collection_names())


def get_word_frequencies(rating=None):
    """Returns a dictionary of words and their frequencies for the specified rating else for the entire reviews"""

    stars = rating if rating is None else {'stars': rating}
    reviews = db.vegas_reviews.find(stars)

    count = 0
    word_counter = Counter()

    for review in reviews:

        for word in review['tokens']:
            word_counter[word] += 1

        count += 1
        print(count)
    print("Number of reviews with {} stars: {}".format(stars, count))
    return word_counter


def get_word_cloud(word_frequency_counter, number_words):
    """Returns the word cloud"""

    top_words = word_frequency_counter.most_common(number_words)
    word_cloud = WordCloud().generate_from_frequencies(top_words)
    # print(top_words)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


def save_reviews(word_freq):
    """
    Remove words that occur less than twice.
    :param word_freq:
    :return:
    """
    # reviews = db.vegas_reviews.find()
    container = []
    count = 0
    for review in db.vegas_reviews.find():
        # record = [word for word in review['tokens'] if word_freq[word] > 2]
        container.append(review['tokens'])
        count += 1
        print(count)

    print("Converting to Numpy array")
    data = np.array(container)
    print("Saving to file")
    np.save('reviews.npy', data)
    print("Done")


def get_dictionary():
    print("Loading data ...")
    data = np.load('reviews.npy')

    print("Creating Dictionary ...")
    dictionary = corpora.Dictionary(data)
    print("Filtering extremes ...")
    dictionary.filter_extremes()  # below 5, above 0.5 of entire set, and max of 100,000
    dictionary.compactify()
    print(dictionary)
    print("Saving dictionary ...")
    dictionary.save('reviews_word_dictionary.dict')
    print("Done")


def get_corpus_bow():
    print("Loading dictionary ...")
    dictionary = corpora.Dictionary.load('reviews_word_dictionary.dict')

    print("Loading reviews")
    reviews = np.load('reviews.npy')

    print("Word to vector ...")
    corpus = [dictionary.doc2bow(review) for review in reviews]

    print("Serialize vector")
    corpora.MmCorpus.serialize('reviews_bow.mm', corpus)  # store to disk
    # print(corpus)


def get_tfidf_transformation():
    corpus = corpora.MmCorpus('reviews_bow.mm')
    tfidf = models.TfidfModel(corpus)
    # print(tfidf)
    tfidf.save('reviews_tfidf_model.tfidf')
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=45063)
    index.save('corpus_tfidf_index')


def perform_similarity_query(query):
    dictionary = corpora.Dictionary.load('reviews_word_dictionary.dict')
    query_vec = dictionary.doc2bow(clean(query))
    tfidf = models.TfidfModel.load('reviews_tfidf_model.tfidf')
    # print(tfidf[query_vec])
    index = similarities.SparseMatrixSimilarity.load("corpus_tfidf_index")
    sims = index[tfidf[query_vec]]
    lda = models.LdaModel.load('corpus_lda_10')
    # print(sims[0:10])
    # print(list(enumerate(sims)))
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    # print(sims[0:15])
    total_num = {}
    total_den = {}

    reviews_star = np.load('reviews_star.npy')
    reviews_corpus = corpora.MmCorpus('reviews_bow.mm')

    count = 0
    container ={}
    topic_one = {}
    topic_two = {}
    topic_three = {}
    topic_four = {}
    topic_five = {}
    topic_six = {}
    topic_seven = {}
    topic_eight = {}
    topic_nine = {}
    topic_ten = {}
    for review in sims:
        business = review[0]
        cosine_sim = review[1]

        if cosine_sim < 0.1:
            continue

        # print(db.vegas_reviews[business]['text'])
        busRev_vec= reviews_corpus[business]
        busRev_lda= lda[busRev_vec]
        # print(busRev_lda)
        topic_one.setdefault(business, 0)
        topic_two.setdefault(business, 0)
        topic_three.setdefault(business, 0)
        topic_four.setdefault(business, 0)
        topic_five.setdefault(business, 0)
        topic_six.setdefault(business, 0)
        topic_seven.setdefault(business, 0)
        topic_eight.setdefault(business, 0)
        topic_nine.setdefault(business, 0)
        topic_ten.setdefault(business, 0)

        for i in busRev_lda:
            # print(i)
            if i[0]==0:
                topic_one[business]+= i[1]
            elif i[0]==1:
                topic_two[business] += i[1]
            elif i[0] == 2:
                topic_three[business] += i[1]
            elif i[0]==3:
                topic_four[business] += i[1]
            elif i[0]== 4:
                topic_five[business] += i[1]
            elif i[0] == 5:
                topic_six[business] += i[1]
            elif i[0] == 6:
                topic_seven[business] += i[1]
            elif i[0]== 7:
                topic_eight[business] += i[1]
            elif i[0]== 8:
                topic_nine[business] += i[1]
            elif i[0] == 9:
                topic_ten[business] += i[1]

        total_den.setdefault(business, 0)
        total_num.setdefault(business, 0)

        stars = reviews_star[business]
        num = stars * cosine_sim
        den = cosine_sim

        total_num[business] += num
        total_den[business] += den
        # count += 1
        # print(count)
    print(topic_seven)
    rankings = [(item, num_total / total_den[item]) for item, num_total in total_num.items()]
    sorted_rankings = sorted(rankings, key=lambda item: -item[1])
    c= round(len(rankings)*0.25)
    del sorted_rankings[c:len(sorted_rankings)]
    print(len(sorted_rankings))



def extract_reviews_star():
    container = []
    count = 0
    for review in db.vegas_reviews.find():
        container.append(review['stars'])

        count += 1
        print(count)
    stars = np.array(container)
    np.save('reviews_star.npy', stars)


def get_all_restaurant_names(query):
    container = []
    for res in db.vegas_restaurants.find({}, {"name": 1}):
        container.append(clean(res['name']))
    data = np.array(container)
    # np.save('restaurants.npy', data)
    rest_dict = corpora.Dictionary(container)
    # print(rest_dict)
    bow_corpus = [rest_dict.doc2bow(res) for res in container]

    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=3246)
    query_vec = rest_dict.doc2bow(clean(query))
    # names =set()
    sims = index[tfidf[query_vec]]
    # print(type(sims))
    # print(list(enumerate(sims)))
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims[0:6])
    # index.save('rest_tfidf_index')


def clean(value):
    """
    Process the given value by replacing non alphabets with spaces, lower the case and split at the spaces
    :param value: Text input to clean
    :return: return list of tokens
    """

    return re.sub("[^a-zA-Z]", " ", value).lower().split()


def get_all_categories():
    container = []
    #print(db.vegas_restaurants.find().distinct('categories'))
    for cat in db.vegas_restaurants.find({},{'categories':1}):
        # print(" ".join(cat['categories']))
        #  container.append(list(re.sub("categories")))
        container.append(clean(" ".join(cat['categories'])))
        data= np.array(container)
        #np.save('categories.npy',data)


def get_restaurants_categories():
    container= np.load('categories.npy')
    categories_dict = corpora.Dictionary(container)
    #print(len(categories_dict))
    bow_corpus = [categories_dict.doc2bow(cat) for cat in container]
    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=236)
    query_vec = categories_dict.doc2bow(clean("chinese bars"))
    # print(query_vec)
    sims = index[tfidf[query_vec]]
    # print(type(sims))
    # print(list(enumerate(sims)))
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims[0:6])
    # index.save('rest_tfidf_index')


def get_user_lda_sims(user_id):
    container = []
    for review in db.vegas_reviews.find({'user_id': user_id}, {'tokens':1}):
        container.append(review['tokens'])

    # np.save('current_user_reviews', container)
    # print("Loading user reviews")
    reviews = np.load('current_user_reviews.npy')
    dictionary = corpora.Dictionary.load('reviews_word_dictionary.dict')
    #
    # print("Word to vector ...")
    user_review_corpus = [dictionary.doc2bow(rev) for rev in reviews]
    #
    # print(len(user_review_corpus))
    #
    topic = {}
    lda_model = models.LdaModel.load('corpus_lda_10')

    for user_rev in user_review_corpus:
        # print(user_rev)
        lda_sims = lda_model[user_rev] #todo: replace with lda sim.
        # break
        for sim in lda_sims:
            topic.setdefault(sim[0], 0)
            topic[sim[0]] += sim[1]
    m=max(topic.items(), key=operator.itemgetter(1))[0]
    print(m)
    return m

    # print(db.vegas_reviews.find({'user_id': 'qL7Astun3i7qwr2IL5iowA'}).count())



def get_lda():
    corpus = corpora.MmCorpus('reviews_bow.mm')
    dictionary = corpora.Dictionary.load('reviews_word_dictionary.dict')
    lda = models.LdaModel(corpus, num_topics=10, id2word=dictionary);
    lda.save('corpus_lda_10')
    lda.print_topics()

def get_user_LDAsim(query):
    dictionary= corpora.Dictionary.load('reviews_word_dictionary.dict')
    corpus = corpora.MmCorpus('reviews_bow.mm')
    query_vec = dictionary.doc2bow(clean(query))
    lda= models.LdaModel.load('corpus_lda_10')
    # index = similarities.SparseMatrixSimilarity(lda[corpus],num_features=10)
    # index.save('corpus_lda_index')
    # index = similarities.SparseMatrixSimilarity.load("corpus_lda_index")
    query_lda= lda[query_vec]
    # sims= index[query_lda]
    print(query_lda)



def get_lsi():
    corpus = corpora.MmCorpus('reviews_bow.mm')
    dictionary = corpora.Dictionary.load('reviews_word_dictionary.dict')


if __name__ == '__main__':
    # word_freq = get_word_frequencies()
    # print("Length of words: {}".format(len(word_freq)))
    # save_reviews(word_freq)
    # print("5 least common.")
    # print(word_freq.most_common()[:-500-1:-1])
    # get_dictionary()
    # print("Loading ...")
    # dictionary = corpora.Dictionary.load('reviews_word_dictionary.dict')
    # print(dictionary)
    # print(db.business.find({'categories': 'Restaurants', 'city':'Las Vegas'}).count())

    # vegas_res = db.vegas_restaurants
    # # count = 0
    # # for rest in db.business.find({'categories': 'Restaurants', 'city':'Las Vegas'}):
    # #     vegas_res.insert(rest)
    # #     count += 1
    # #     print(count)
    # print(vegas_res.count())
    # get_corpus()
    # perform_similarity_query('pizza burger')
    get_user_lda_sims('utcN2FtmIymOprcfFS-Tfg')

    # perform_similarity_query("las vegas back family iphone nice")
    # get_lda()
    # get_all_restaurant_names()
    # get_all_restaurant_names("pizza hut")
    # extract_reviews_star()


