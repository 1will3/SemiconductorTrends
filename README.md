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

