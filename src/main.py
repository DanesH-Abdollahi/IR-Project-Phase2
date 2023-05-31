# from phase1 import *
import json
from hazm import Normalizer, WordTokenizer, Lemmatizer, SentenceTokenizer
from hazm.utils import stopwords_list
from math import log10

# Initialize hazm tools
normalizer = Normalizer()
tokenizer = WordTokenizer()
lemmetizer = Lemmatizer()
stopwords = stopwords_list()
stopwords.extend(
    [
        "،",
        ".",
        ":",
        "؛",
        "!",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "«",
        "»",
        "؟",
        "-",
        "/",
        '"',
        "'",
        "*",
        "!!",
        "!؟",
        "''",
        '""',
        "》",
        "《",
        "**",
        "*",
        "**",
        "***",
        "****",
        "********",
    ]
)

# Load data from file
with open("../IR_data_news_12k.json", "r") as file:
    data = json.load(file)

# Load Inverted Index from file (which was created in phase 1)
with open("inverted_index.json", "r") as file:
    inverted_index = json.load(file)

# Add tf-idf to inverted index
N = int(list(data.keys())[-1])  # Number of documents
for token in inverted_index:
    n_t = len(inverted_index[token]) - 1  # Number of documents containing token
    for doc_id in inverted_index[token]:
        if doc_id != "total_frequency":
            f_t_d = inverted_index[token][doc_id][
                "frequency"
            ]  # Frequency of token in document
            tf_idf = (1 + log10(f_t_d)) * log10(N / n_t)
            inverted_index[token][doc_id]["tf-idf"] = tf_idf


# Query Processing
query = input("Enter your query: ")
query = normalizer.normalize(query)
query = tokenizer.tokenize(query)
query = [token for token in query if token not in stopwords]
query = [lemmetizer.lemmatize(token) for token in query]

# Construct query vector
query_vector = {}
for token in query:
    if token not in query_vector:
        query_vector[token] = 1
    else:
        query_vector[token] += 1

total_abs = 0
for token in query_vector:
    n_t = len(inverted_index[token]) - 1  # Number of documents containing token
    t_f = query_vector[token]
    query_vector[token] = (1 + log10(t_f)) * log10(N / n_t)
    total_abs += query_vector[token] ** 2

total_abs = total_abs**0.5

# Normalize query vector
for token in query_vector:
    query_vector[token] /= total_abs
