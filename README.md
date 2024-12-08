# SemiconductorTrends
This project aims to analyze scientific abstracts on semiconductors from arXiv to uncover trends and sentiments in research progress.  [https://arxiv.org/]

I used arXiv’s API to collect paper abstracts, perform text preprocessing, apply sentiment analysis to understand
the overall tone of research, and use topic modeling to identify key research trends over time.

This provides insights into how research on semiconductors is evolving.

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


# VERSION 1
At this point, the project is successful at:
- utilizing ArXiv's API to gather research titles and abstracts
- Use BeautifulSoup4 and Pandas packages to parse the content, create a DataFrame, and save to a .csv file
- identify most common keywords using NLTK package (tokenize, stopwords, lemmatizer), reading from DataFrame
- ascribe a rough sentiment score to each paper (followed by an overall positive or negative classification) using NLTK SentimentIntesityAnalyzer, Seaborn
- Create 5 general topics based on a combination of keywords, and sort the papers into the percieved topic, also ranking top papers representative for each topic model (Scikit-Learn (LatentDirichletAllocation, CoutVectorizer), numpy, seaborn)
- Create visualizations based in matplotlib and seaborn libraries: keyword-word cloud, bar and line graphs (sentiment distribution and score over time, overall sentiments over time, topic distribution and proportion over time, publications over time)

Now, I will improve this project as it desperately needs, to more accurately identify the specific developments and trends rather than basic keywords, adjust sentiment and topic modeling approach, and produce more accurate visualizations to represent valuable information regarding developments.


# VERSION 2
I will now add more accuracy and comparison to the project in the following areas: 
- removed the 'chemistry' keyword, seeking semiconductor results wholly outside of chemistry related searches. This increased the papers roughly 400% (1000 total count) per run
- Updated the text preprocessing using Bigrams and Trigrams (top technical phrases, most frequent technical terms)
- Import common research keywords to avoid collection of irrelevant tokens

We can now see an expected difference in the visualizations for sentiment, publications, and distributions over time


# VERSION 3 
Each module was enhanced to work together more effectively, with better error handling and more sophisticated analysis techniques.

Module 1: Data Collection
- Improved how the program collects research papers from arXiv, making it more reliable and able to handle errors better. We also removed some restrictions to get a wider range of relevant papers.

Module 2: Text Preprocessing
- Enhanced how the program understands scientific text by teaching it to recognize important technical terms and filter out common words that don't add meaning. We also improved how it handles mathematical formulas and chemical names.
    Technical Changes:

    - Added TECHNICAL_STOPWORDS set with domain-specific terms
    -  Implemented POS (Part of Speech) tagging
    -  Added BigramCollocationFinder and TrigramCollocationFinder
    -  Enhanced regex patterns for cleaning mathematical notation
    -  Added technical phrase extraction with PMI scoring
    -  Improved handling of hyphenated terms and chemical formulas
    -  Added WordNetLemmatizer for term standardization

Module 3: Sentiment Analysis
- Updated the system to understand the tone of scientific writing, which is very different from regular text. The system now recognizes technical confidence, research progress, and uncertainty in scientific papers.
    Technical Changes:

    - Added SCIENTIFIC_INDICATORS dictionary with:
        Positive indicators (e.g., 'breakthrough', 'efficient')
        Negative indicators (e.g., 'limitation', 'drawback')
        Progress markers (e.g., 'demonstrate', 'develop')
        Uncertainty markers (e.g., 'may', 'possible')
    
    - Updated custom ScientificSentimentAnalyzer class
        Changed weighting and parameters for: technical_confidence scoring, result_strength analysis, citation_impact measurement
  

Module 4: Topic Modeling
- Improved how the program groups similar research papers together and identifies main research themes. The program now better understands the relationships between papers and can track how research topics change over time.
    Technical Changes:

    - Enhanced LDA parameters:
        Changed batch_size to 128
        Added n_jobs=-1 for parallel processing
        Added learning_method='online'
        Added evaluate_every=5

    - Implemented auto_name_topic function
        Added temporal analysis functions

    - Enhanced vectorization parameters:
        Changed min_df from 2 to 3
        Added ngram_range=(1,3)
        Modified token_pattern for compound terms


Module 5: Data Visualization
- Cleaned up the graphing of results. The visualizations now show more clear patterns in research trends and sentiment over time.
    Technical Changes:

    - Added SENTIMENT_COLORS dictionary
    - Added percentage annotations to plots
    - Enhanced figure sizing and formatting
    - Improved color schemes and legend handling



# Future Areas of Improvement 
- Multiple Runs
    - It will be helpful to record the results from 5 runs, and use this variance in data to find a more accurate description of general trends and topics.
    - No variance was found over the 5 runs, indicating reproducability within the results
- Extend the Dataset: Collect data from other sources to compare results.
    - I will include new research sites:  Zenodo [https://zenodo.org/]; MDPI [https://www.mdpi.com/search?q=semiconductor]
    - Compare differences in results
    - common research themes
    - Trends over time
- Incorporate SQL Database
    - This will be used to save the runs
    - See any changes over each run
    - and be used to compare data sources
- PowerBI visualization migration
    - Practice using PowerBI
    - Create a wholistic dashboard accessible for technical/non-technical users

- End project for now, avoid scope creep


