from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
import os
import networkx
import obonet

# Read the ontology
url = 'https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
graph = obonet.read_obo(url)

# Number of nodes
len(graph)

# Number of edges
graph.number_of_edges()

# Check if the ontology is a DAG
networkx.is_directed_acyclic_graph(graph)

# Mapping from term ID to name
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
id_to_name['HP:0001626']  # HP:0001626 is cardiac abnormality

# set of documents
files,filenames=[],[]
directory="dsdata/hpo/Z145184"
for file in os.listdir(directory):
    files.append(os.path.abspath(os.path.join(directory, file)))
    filenames.append(file)
# convert documents into a matrix
def tokenizer(s):
    return s.split()
countvectorizer = CountVectorizer(input='filename', analyzer= 'word', stop_words='english', tokenizer=tokenizer, lowercase=False)
tfidfvectorizer = TfidfVectorizer(input='filename', analyzer='word',stop_words= 'english', tokenizer=tokenizer, lowercase=False)
count_wm = countvectorizer.fit_transform(files)
tfidf_wm = tfidfvectorizer.fit_transform(files)
#retrieve the terms found in the corpora
count_tokens = []
for x in countvectorizer.get_feature_names():
    try:
        count_tokens.append(id_to_name[x])
    except KeyError:
        count_tokens.append(x)
tfidf_tokens = []
for x in tfidfvectorizer.get_feature_names():
    try:
        tfidf_tokens.append(id_to_name[x])
    except KeyError:
        tfidf_tokens.append(x)
pd.set_option("display.max_rows", None, "display.max_columns", None)
df_countvect = pd.DataFrame(data = count_wm.toarray(),index = filenames,columns = count_tokens)
df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(),index = filenames,columns = tfidf_tokens)
print("Count Vectorizer\n")
print(df_countvect)
print("\nTD-IDF Vectorizer\n")
print(df_tfidfvect)
