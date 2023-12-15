import pandas as pd #Dataframe Structure library
import cufflinks as cf
import nltk #Removing "stopwords"
nltk.download('wordnet')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from plotly.offline import iplot
from textblob import TextBlob
import matplotlib.pyplot as plt #2D plotting library
import seaborn as sns #data visualization library
import numpy as np
import math

# Reading data in the system
data = pd.read_csv("D:\\Backup_Programing\\Programming_2308\\파이썬\\Crawling\\Amazon\\Success\\Scraping reviews_rating & review_Cuckoo_B0786XV8Q6.csv", encoding = "unicode_escape")
data.head()
data.shape

## Distribution of rating ##
sns.distplot(data['Rating'])

## Counting of each ratings ##
sns.countplot(x='Rating', data=data)
# df_rating =
plt.savefig('Ratings Count.png')

# Removing null columns
data.isnull().sum()
df1 = pd.DataFrame(data)

## Counting words & Frequency_unigram ##
def get_top_n_words(corpus, n=None):
    vec = CountVectorizer(stop_words = 'english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
common_words = get_top_n_words(df1['Review'], 40)
for word, freq in common_words:
    print(word, freq)
df1_1 = pd.DataFrame(common_words, columns = ['common words' , 'count'])
df1_1.groupby('common words').sum()['count'].sort_values(ascending=False).figure(
    kind='bar', yTitle='Count', linecolor='black', title='Top 20 words in review after removing stop words')
df1_1.to_csv("Sentiment Analysis on Amazon_distribution of top unigram_Cuckoo_B0786XV8Q6_2.csv", mode='w', encoding="utf-8")

## Counting words & Frequency_bigram ##
def get_top_n_bigram(corpus, n=None):
    vec = CountVectorizer(ngram_range=(2, 2), stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
common_words = get_top_n_words(df1['Review'], 40)
for word, freq in common_words:
    print(word, freq)
df1_2 = pd.DataFrame(common_words, columns = ['common words' , 'count'])
df1_2.groupby('common words').sum()['count'].sort_values(ascending=False).figure(
    kind='bar', yTitle='Count', linecolor='black', title='Top 20 bigrams in review after removing stop words')
df1_2.to_csv("Sentiment Analysis on Amazon_distribution of top bigram_Cuckoo_B0786XV8Q6_2.csv", mode='w', encoding="utf-8")

## Counting words & Frequency_trigram ##
def get_top_n_trigram(corpus, n=None):
    vec = CountVectorizer(ngram_range=(3, 3), stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
common_words = get_top_n_words(df1['Review'], 40)
for word, freq in common_words:
    print(word, freq)
df1_3 = pd.DataFrame(common_words, columns = ['common words' , 'count'])
df1_3.groupby('common words').sum()['count'].sort_values(ascending=False).figure(
    kind='bar', yTitle='Count', linecolor='black', title='Top 20 trigrams in review after removing stop words')
df1_3.to_csv("Sentiment Analysis on Amazon_distribution of top trigram_Cuckoo_B0786XV8Q6_2.csv", mode='w', encoding="utf-8")

## Polarity Scores ##
# Create quick lambda functions to find the polarity of each review
# Terminal / Anaconda Navigator: conda install -c conda-forge textblobfrom textblob import TextBlob
df1['Review']= df1['Review'].astype(str) #Make sure about the correct data type
pol = lambda x: TextBlob(x).sentiment.polarity
df1['polarity'] = df1['Review'].apply(pol) # depending on the size of your data, this step may take some time.

num_bins = 80
plt.figure(figsize=(10,6))
df2 = n, bins, patches = plt.hist(df1.polarity, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Polarity')
plt.ylabel('Number of Reviews')
plt.title('Histogram of Polarity Score')
plt.show();

new = pd.DataFrame(["polarity"])
df2 = df1.append(new)
df2.to_csv("Sentiment Analysis on Amazon_Polarity_0309.csv", mode='w', encoding="utf-8")

## Plotting average polarity for each score rating
sns.barplot(x='Rating', y='polarity', data=df2)

## Subjectivity Scores ##
# Creating subjectivity scores
sub = lambda x: TextBlob(x).sentiment.subjectivity
df1['subjectivity'] = df1['Review'].apply(sub)
df1.sample(50)

# Density Plot and Histogram of subjectivity
plt.figure(figsize=(10,5))
sns.distplot(df1['subjectivity'], hist=True, kde=True,
bins=int(30), color = 'darkblue',
hist_kws={'edgecolor':'black'},
kde_kws={'linewidth': 4})
plt.xlim([-0.001,1.001])
plt.xlabel('Subjectivity', fontsize=13)
plt.ylabel('Frequency', fontsize=13)
plt.title('Distribution of Subjectivity Score', fontsize=15)
plt.show();

new2 = pd.DataFrame(["polarity"], ["subjectivity"])
df3 = df1.append(new2)
df3.to_csv("Sentiment Analysis on Amazon_Polarity & Subjectivity_0309.csv", mode='w', encoding="utf-8")
data.head()

# assigning Good_reviews and Bad_reviews
# df3["Good_reviews"] = np.where(df3["polarity"].values > 0.5, df3["subjectivity"].values < 0.5)
# df4 = df3.append(df3["Good_reviews"])
# df4.to_csv("Sentiment Analysis on Amazon_0224_Scatter Plot.csv", mode='w', encoding="utf-8")
# df3["goodorbad"] = pd.DataFrame({tuple(df3.loc[:,["polarity"]] > 0.5), tuple(df3.loc[:,["subjectivity"]] < 0.5)})
df3["goodorbad"] = pd.DataFrame({tuple(df3.loc[:,["polarity"]] >= 0.6)})
df4 = df3.append(df3["goodorbad"])
df4.to_csv("Sentiment Analysis on Amazon_goodorbad_0309.csv", mode='w', encoding="utf-8")

## Polarity vs Subjectivity ##
goodorbaddf = pd.read_csv("C:\\Users\Becky\Desktop\\backup_becky\\파이썬\\Sentiment Analysis\\Amazon\\Sentiment Analysis on Amazon_0309_goodorbad_adjusted.csv", encoding = "unicode_escape")
plt.figure(figsize=(10,6))
sns.scatterplot(x='polarity', y='subjectivity', data=goodorbaddf)
if goodorbaddf["goodorbad"].isin("good").all():
    sns.scatterplot(hue="goodorbad", data=goodorbaddf)
sns.scatterplot(x='polarity', y='subjectivity', data=df3)
plt.xlabel('Polarity', fontsize=13)
plt.ylabel('Subjectivity', fontsize=13)
plt.title('Polarity vs Subjectivity', fontsize=15)
plt.show();
# sns.scatterplot(x='polarity', y='subjectivity', data=df4)
# if good["goodorbad"] == "good":
#     sns.scatterplot(hue="goodorbad")
# sns.scatterplot(x='polarity', y='subjectivity', data=df3)
# plt.xlabel('Polarity', fontsize=13)
# plt.ylabel('Subjectivity', fontsize=13)
# plt.title('Polarity vs Subjectivity', fontsize=15)
# plt.show();

## Box plots of good reviews and bad reviews ## - x
plt.figure(figsize=(10,6))
df2 = sns.boxenplot(data=df4, x="goodorbad", y="polarity")
plt.title('Polarity Score of Good reviews and Bad reviews')
plt.show();


# df.loc[(df.polarity == 1 & (df.Good_reviews == 0))].Text.head(10).tolist()

# ## Punctuation vs Polarity ##
# plt.figure(figsize=(15,8))
# df5= df4.loc[df4.upper <= 50]
# sns.boxenplot(x='upper', y='polarity', data=df3)
# plt.xlabel('Punctuation', fontsize=13)
# plt.ylabel('Polarity Score', fontsize=13)
# plt.title('Punctuation vs Polarity Plot', fontsize=15)
# plt.show();

