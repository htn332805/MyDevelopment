# analysis/summarizer.py

"""
Text Summarization Utilities for Framework0.

This module provides functions to perform various text summarization tasks,
including extractive and abstractive summarization. These utilities can be
utilized across different analysis tasks to ensure consistency and reusability.

Features:
- `extractive_summary(text, num_sentences=5)`: Extracts the most important
  sentences from the input text.
- `abstractive_summary(text)`: Generates a concise summary of the input text
  using a pre-trained transformer model.
"""

from typing import List
from transformers import pipeline
import nltk

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')

# Initialize the transformer model for abstractive summarization
abstractive_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extractive_summary(text: str, num_sentences: int = 5) -> str:
    """
    Extracts the most important sentences from the input text.

    Args:
        text (str): The input text to summarize.
        num_sentences (int): The number of sentences to include in the summary.

    Returns:
        str: A summary consisting of the most important sentences.
    """
    sentences = nltk.sent_tokenize(text)
    word_frequencies = {}
    for word in nltk.word_tokenize(text.lower()):
        if word.isalnum():
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] /= max_frequency
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_score = 0
        for word in nltk.word_tokenize(sentence.lower()):
            if word.isalnum() and word in word_frequencies:
                sentence_score += word_frequencies[word]
        sentence_scores[i] = sentence_score
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = ' '.join([sentences[i] for i in ranked_sentences[:num_sentences]])
    return summary

def abstractive_summary(text: str) -> str:
    """
    Generates a concise summary of the input text using a pre-trained transformer model.

    Args:
        text (str): The input text to summarize.

    Returns:
        str: A concise summary of the input text.
    """
    summary = abstractive_summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']
