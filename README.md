# SemiconductorTrends
This project aims to analyze scientific abstracts on semiconductors in the chemistry field from arXiv to uncover trends and sentiments in research progress. 

I used arXiv’s API to
collect paper abstracts, perform text preprocessing, apply sentiment analysis to understand
the overall tone of research, and use topic modeling to identify key research trends over time.
This provides insights into how research on semiconductors in chemistry is evolving.

Objectives:
1. Data Collection from arXiv:
Use arXiv API to collect abstracts of papers related to semiconductors in the
chemistry field.
Organize the dataset to include metadata like title, abstract, author(s), publication
date, and categories.
2. Text Preprocessing:
Clean and preprocess the text by removing unnecessary content (e.g., special
characters, citations).
Tokenize, lemmatize, and remove stop words to prepare the text for analysis.
3. Sentiment Analysis:
Analyze the sentiment of paper abstracts to determine the general sentiment
(positive, negative, or neutral) regarding the developments in the field.
4. Topic Modeling and Trend Discovery:
Use NLP techniques like Latent Dirichlet Allocation (LDA) to uncover key
research topics.
Analyze how the focus of research has shifted over time using time-series
analysis of the topics.
5. Data Visualization:
Visualize sentiment trends over time and key research areas using graphs, word
clouds, and topic models.


# UPDATE 10/23
At this point, the project is successful at:
- utilizing ArXiv's API to gather research titles and abstracts
- Use BeautifulSoup4 and Pandas packages to parse the content, create a DataFrame, and save to a .csv file
- identify most common keywords using NLTK package (tokenize, stopwords, lemmatizer), reading from DataFrame
- ascribe a rough sentiment score to each paper (followed by an overall positive or negative classification) using NLTK SentimentIntesityAnalyzer, Seaborn
- Create 5 general topics based on a combination of keywords, and sort the papers into the percieved topic, also ranking top papers representative for each topic model (Scikit-Learn (LatentDirichletAllocation, CoutVectorizer), numpy, seaborn)
- Create visualizations based in matplotlib and seaborn libraries: keyword-word cloud, bar and line graphs (sentiment distribution and score over time, overall sentiments over time, topic distribution and proportion over time, publications over time)

This initial draft documents will be placed in a folder for version control. (See: Version1 )
Now, I will improve this project as it desperately needs, to more accurately identify the specific developments and trends rather than basic keywords, adjust sentiment and topic modeling approach, and produce more accurate visualizations to represent valuable information regarding developments.

VERSION 1.1
For this update, I:
- removed the 'chemistry' keyword, seeking semiconductor results wholly outside of chemistry related searches. This increased the papers roughly 400% (1000 total count)
- Updated the text preprocessing using Bigrams and Trigrams (top technical phrases, most frequent technical terms
- We can now see an expected difference in the visualizations for sentiment, publications, and distributions over time
- I am tracking these updates simply to keep track of changes


