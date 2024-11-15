import os
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.corpora import Dictionary
from gensim.models import LdaModel, TfidfModel

# Download stopwords and tokenize data (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt_tab')

# Define the folder containing the text files
folder_path = 'doc'

# Set up stop words and preprocessing function
stop_words = set(stopwords.words('english'))
downweight_words = {"assessment", "graded", "credit", "requires"}  # Words to down-weight

def preprocess(text):
    tokens = word_tokenize(text.lower())  # Convert to lowercase and tokenize
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return tokens

# Read and preprocess each file in the folder
documents = []
competency_labels = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        # Extract competency name from the first line
        first_line = f.readline().strip()
        competency_name = re.findall(r'\((.*?)\)', first_line)
        competency_labels.append(competency_name[0] if competency_name else "Unknown")

        text = f.read()
        documents.append(preprocess(text))

# Check the first processed document
print(documents[0])

# Create a dictionary from the processed documents
dictionary = Dictionary(documents)

# Adjust the frequency of specific words in the dictionary
for word in downweight_words:
    if word in dictionary.token2id:
        token_id = dictionary.token2id[word]
        dictionary.dfs[token_id] *= 0.1  # Down-weight by 90%

# Convert documents into a bag-of-words format
corpus_bow = [dictionary.doc2bow(doc) for doc in documents]

# Create the TF-IDF model
tfidf_model = TfidfModel(corpus_bow)

# Apply the TF-IDF model to the corpus to get the TF-IDF representation
corpus_tfidf = tfidf_model[corpus_bow]

# Train the LDA model using the TF-IDF corpus
num_topics = 50  # Number of topics
lda_model = LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics, passes=500)

# Print topics with keywords
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx + 1}: {topic}")

# Group documents by top 5 topics
document_groups = {}  # Dictionary to store groups of documents by top 5 topics

print("\nDocument Grouping by Top 5 Topics:")
for i, doc in enumerate(corpus_tfidf):
    # Get topic probabilities for the document
    topic_probabilities = lda_model.get_document_topics(doc)
    # Sort topics by probability in descending order and select the top 5 topics
    top_5_topics = sorted(topic_probabilities, key=lambda x: x[1], reverse=True)[:5]

    # Create a sorted tuple of the top 5 topic IDs to use as a unique key
    top_5_topic_ids = tuple(sorted([topic_id for topic_id, prob in top_5_topics]))

    # Group documents by the unique combination of top 5 topics
    if top_5_topic_ids not in document_groups:
        document_groups[top_5_topic_ids] = []
    document_groups[top_5_topic_ids].append(f"Document {i + 1} (Original: {competency_labels[i]})")

# Print each group of documents
for topic_ids, docs in document_groups.items():
    print(f"\nGroup with Top 5 Topics {topic_ids}:")
    for doc in docs:
        print(f"  {doc}")

# Save the model and dictionary
lda_model.save("lda_model.model")
dictionary.save("dictionary.dict")

# Example: Find top topics for the first document
document_topics = lda_model.get_document_topics(corpus_tfidf[0])
top_5_topics = sorted(document_topics, key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 topics for the first document:", top_5_topics)
