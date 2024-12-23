import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter
import logging
from datetime import datetime
from typing import List, Dict, Set
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

GENERIC_TERMS = {
    'based', 'using', 'via', 'new', 'novel', 'improved', 'high', 'low',
    'approach', 'method', 'system', 'type', 'performance', 'application',
    'device', 'material', 'study', 'analysis', 'research', 'general',
    'data', 'experimental', 'numerical', 'theoretical', 'applied',
    'and', 'the', 'with', 'for', 'from', 'by', 'at', 'to', 'in', 'on', 'of',
    'work', 'result', 'time', 'first', 'second', 'used', 'based'
}

def clean_term(term: str) -> str:
    """Clean a single term while preserving meaningful compounds."""
    term = re.sub(r'[^a-zA-Z\s-]', '', term)
    term = re.sub(r'\b[a-zA-Z]\b', '', term)
    return term.strip()

def find_compound_terms(text: str) -> List[str]:
    """Find meaningful technical compound terms."""
    compounds = []
    hyphenated = re.findall(r'\w+(?:-\w+)+', text.lower())
    if hyphenated:
        compounds.extend(hyphenated)
    
    text = text.lower()
    if 'quantum dot' in text: compounds.append('quantum dot')
    if 'quantum computing' in text: compounds.append('quantum computing')
    if 'solar cell' in text: compounds.append('solar cell')
    if 'photonic crystal' in text: compounds.append('photonic crystal')
    if 'topological quantum' in text: compounds.append('topological quantum')
    if 'semiconductor laser' in text: compounds.append('semiconductor laser')
    if 'epitaxial growth' in text: compounds.append('epitaxial growth')
    if 'thin film' in text: compounds.append('thin film')
    
    return compounds

def get_significant_terms(keywords: List[str], papers: List[str]) -> List[str]:
    """Get significant terms prioritizing compounds."""
    clean_keywords = [clean_term(k) for k in keywords if k not in GENERIC_TERMS]
    
    paper_text = ' '.join(papers).lower()
    compounds = find_compound_terms(paper_text)
    
    significant_terms = []
    for compound in compounds:
        if any(kw in compound for kw in clean_keywords):
            significant_terms.append(compound)
            if len(significant_terms) == 2:
                break
    
    while len(significant_terms) < 2 and clean_keywords:
        term = clean_keywords.pop(0)
        if term and not any(term in t for t in significant_terms):
            significant_terms.append(term)
    
    return significant_terms

def format_topic_name(terms: List[str], used_names: Set[str]) -> str:
    """Format terms into a unique, clean topic name."""
    if not terms:
        return "Semiconductor Research"
        
    if len(terms) >= 2:
        name = ' '.join(t.title() for t in terms[:2])
        if name not in used_names:
            return name
    
    if terms:
        base = terms[0].title()
        for modifier in terms[1:]:
            name = f"{modifier.title()} {base}"
            if name not in used_names:
                return name
            name = f"{base} {modifier.title()}"
            if name not in used_names:
                return name
    
    base = terms[0].title()
    suffix = 1
    while f"{base} {suffix}" in used_names:
        suffix += 1
    return f"{base} {suffix}"

def get_topic_name(keywords: List[str], papers: List[str], used_names: Set[str]) -> str:
    """Generate a clean, unique topic name from LDA results."""
    significant_terms = get_significant_terms(keywords, papers)
    return format_topic_name(significant_terms, used_names)

def prepare_data_for_lda(df: pd.DataFrame, text_column: str):
    vectorizer = CountVectorizer(
        max_df=0.95,
        min_df=2,
        stop_words='english',
        ngram_range=(1, 2)
    )
    doc_term_matrix = vectorizer.fit_transform(df[text_column])
    return vectorizer, doc_term_matrix

def perform_lda(doc_term_matrix, num_topics=5):
    lda_model = LatentDirichletAllocation(
        n_components=num_topics,
        max_iter=25,
        learning_method='online',
        random_state=42,
        batch_size=128,
        n_jobs=-1
    )
    lda_output = lda_model.fit_transform(doc_term_matrix)
    return lda_model, lda_output

def analyze_topic_patterns(model, feature_names, lda_output, df):
    topic_info = {}
    used_names = set()
    
    for topic_idx, topic in enumerate(model.components_):
        top_words_idx = topic.argsort()[:-20:-1]
        top_words = [feature_names[i] for i in top_words_idx]
        
        doc_probabilities = lda_output[:, topic_idx]
        top_doc_indices = doc_probabilities.argsort()[-5:][::-1]
        top_docs = [df.iloc[idx]['title'] for idx in top_doc_indices]
        
        topic_name = get_topic_name(top_words, top_docs, used_names)
        used_names.add(topic_name)
        
        topic_info[topic_idx] = {
            'name': topic_name,
            'keywords': top_words[:10],
            'example_papers': top_docs[:3],
            'probabilities': doc_probabilities[top_doc_indices]
        }
        
        print(f"\nTopic {topic_idx + 1}: {topic_name}")
        print("Top Keywords:", ", ".join(top_words[:10]))
        print("\nMost Representative Papers:")
        for title, prob in zip(top_docs[:3], doc_probabilities[top_doc_indices][:3]):
            print(f"- {title} (Probability: {prob:.3f})")
        print("-" * 50)
    
    return topic_info

def save_topic_analysis(topic_info: Dict, df: pd.DataFrame, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Topic Analysis Report\n")
        f.write("===================\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for topic_idx, info in topic_info.items():
            f.write(f"\nTopic {topic_idx + 1}: {info['name']}\n")
            f.write("-" * 50 + "\n")
            f.write(f"Keywords: {', '.join(info['keywords'])}\n\n")
            
            f.write("Most Representative Papers:\n")
            for title, prob in zip(info['example_papers'], info['probabilities']):
                f.write(f"- {title} (Probability: {prob:.3f})\n")
            
            topic_docs = df[df['assigned_topic'] == topic_idx]
            f.write(f"\nTopic Statistics:\n")
            f.write(f"Number of papers: {len(topic_docs)}\n")
            f.write("\n" + "="*50 + "\n")

if __name__ == "__main__":
    logging.info("Loading data...")
    df = pd.read_csv('arxiv_semiconductors_with_sentiment.csv')
    
    logging.info("Preparing data for topic modeling...")
    vectorizer, doc_term_matrix = prepare_data_for_lda(df, 'processed_abstract')
    
    logging.info("Performing topic modeling...")
    num_topics = 5
    lda_model, lda_output = perform_lda(doc_term_matrix, num_topics)
    
    logging.info("Analyzing topic patterns...")
    topic_info = analyze_topic_patterns(
        lda_model,
        vectorizer.get_feature_names_out(),
        lda_output,
        df
    )
    
    df['assigned_topic'] = lda_output.argmax(axis=1)
    df['topic_name'] = df['assigned_topic'].map({idx: info['name'] 
                                                for idx, info in topic_info.items()})
    
    logging.info("Saving analysis report...")
    save_topic_analysis(topic_info, df, 'topic_analysis_report.txt')
    df.to_csv('arxiv_semiconductors_with_topics.csv', index=False)
    
    logging.info("Analysis complete!")