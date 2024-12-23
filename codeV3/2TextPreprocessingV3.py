import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures, TrigramCollocationFinder
nltk.download('averaged_perceptron_tagger_eng')
import re
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Download necessary NLTK data
for package in ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']:
    nltk.download(package)

TECHNICAL_STOPWORDS = {
    # General science terms
    'study', 'result', 'show', 'using', 'method', 'analysis', 'experimental',
    'measured', 'measurement', 'data', 'research', 'process', 'used', 'based',
    'shown', 'present', 'investigated', 'obtained', 'performed', 'developed',
    'observed', 'found', 'reported', 'sample', 'test', 'testing', 'results',

    # General physics terms
    'energy', 'state', 'system', 'effect', 'field', 'high', 'potential',
    'temperature', 'structure', 'property', 'properties', 'model',
    'application', 'charge', 'force', 'rate', 'value', 'level', 'density',

    # General semiconductor terms
    'semiconductor', 'electron', 'band', 'coupling', 'carrier',
    'control', 'gap', 'theory', 'dynamic', 'different', 'strong',
    'device', 'type', 'based', 'material', 'parameter', 'network',
    'accuracy', 'light', 'current', 'voltage', 'power', 'signal',
    'quantum', 'spin', 'laser', 'topological'  # Only filtered when standalone
}

PRESERVE_COMPOUNDS = {
    # Quantum-related compounds
    'quantum dot', 'quantum well', 'quantum computing', 'quantum state',
    'quantum information', 'quantum transport', 'quantum memory',
    
    # Band-related compounds
    'band gap', 'band structure', 'band alignment',
    
    # Spin-related compounds
    'spin qubit', 'spin transport', 'spin current', 'spin valve',
    'spin polarization',
    
    # Laser-related compounds
    'laser diode', 'laser emission', 'laser cavity',
    
    # Topological compounds
    'topological insulator', 'topological state', 'topological phase',
    
    # Other important compounds
    'field effect', 'carrier transport', 'electron transport',
    'josephson junction', 'molecular beam'
}

def protect_compounds(text: str) -> str:
    """Replace preserved compounds with single tokens."""
    protected_text = text.lower()
    for compound in sorted(PRESERVE_COMPOUNDS, key=len, reverse=True):
        if compound in protected_text:
            protected_token = compound.replace(' ', '_')
            protected_text = protected_text.replace(compound, protected_token)
    return protected_text

def restore_compounds(text: str) -> str:
    """Restore protected compounds back to original form."""
    restored_text = text
    for compound in PRESERVE_COMPOUNDS:
        protected_token = compound.replace(' ', '_')
        restored_text = restored_text.replace(protected_token, compound)
    return restored_text

def preprocess_text(text):
    """Enhanced preprocessing with compound preservation."""
    if isinstance(text, float):
        return ""
    
    # Convert to lowercase and protect compounds
    text = protect_compounds(text.lower())
    
    # Remove URLs and references
    text = re.sub(r'http\S+|www\S+|\[.*?\]|\(.*?\)', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # POS tagging
    pos_tags = nltk.pos_tag(tokens)
    
    # Custom filtering
    stop_words = set(stopwords.words('english')).union(TECHNICAL_STOPWORDS)
    filtered_tokens = []
    
    for token, pos in pos_tags:
        if ('_' in token or  # Preserved compound
            (token not in stop_words and
             len(token) > 2 and
             (pos.startswith(('NN', 'JJ')) or
              '-' in token or
              any(char.isdigit() for char in token)))):
            filtered_tokens.append(token)
    
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Restore protected compounds
    processed_text = restore_compounds(' '.join(tokens))
    
    return processed_text

def extract_technical_phrases(text):
    """Extract technical phrases considering preserved compounds."""
    text = protect_compounds(text)
    sentences = sent_tokenize(text)
    all_words = []
    
    for sentence in sentences:
        cleaned = re.sub(r'[^\w\s-]', ' ', sentence)
        words = word_tokenize(cleaned)
        all_words.extend(words)
    
    # Extract bigrams
    bigram_measures = BigramAssocMeasures()
    bigram_finder = BigramCollocationFinder.from_words(all_words)
    bigram_finder.apply_freq_filter(5)
    bigrams = bigram_finder.nbest(bigram_measures.pmi, 30)
    
    # Extract trigrams
    trigram_measures = TrigramAssocMeasures()
    trigram_finder = TrigramCollocationFinder.from_words(all_words)
    trigram_finder.apply_freq_filter(3)
    trigrams = trigram_finder.nbest(trigram_measures.pmi, 30)
    
    # Restore compounds in extracted phrases
    bigrams = [tuple(restore_compounds(' '.join(bg)).split()) for bg in bigrams]
    trigrams = [tuple(restore_compounds(' '.join(tg)).split()) for tg in trigrams]
    
    return bigrams, trigrams

def preprocess_dataframe(df):
    """Preprocess the dataframe with enhanced technical term extraction."""
    logging.info("Starting text preprocessing...")
    
    df['processed_title'] = df['title'].apply(preprocess_text)
    df['processed_abstract'] = df['abstract'].apply(preprocess_text)
    df['technical_phrases'] = df['abstract'].apply(
        lambda x: [' '.join(phrase) for phrase in extract_technical_phrases(x)[0] + extract_technical_phrases(x)[1]]
    )
    
    logging.info("Preprocessing complete.")
    return df

if __name__ == "__main__":
    df = pd.read_csv('arxiv_semiconductors.csv')
    df_processed = preprocess_dataframe(df)
    
    output_filename = 'arxiv_semiconductors_preprocessed.csv'
    df_processed.to_csv(output_filename, index=False)
    
    print("\nMost Frequent Technical Terms:")
    all_text = ' '.join(df_processed['processed_abstract'])
    term_frequencies = Counter(word_tokenize(all_text))
    print(pd.Series(term_frequencies).sort_values(ascending=False).head(20))
    
    print("\nPreprocessing Statistics:")
    print(f"Average technical phrases per abstract: {df_processed['technical_phrases'].str.len().mean():.2f}")
    print(f"Total unique technical phrases identified: {len(set([phrase for phrases in df_processed['technical_phrases'] for phrase in phrases]))}")