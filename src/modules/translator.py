"""
Module for translating text using Deep Translator.
"""
from typing import List
from deep_translator import GoogleTranslator

def chunk_text(text: str, max_length: int = 4500) -> List[str]:
    """
    Split text into chunks that respect sentence boundaries and max length.
    
    Args:
        text (str): Text to split
        max_length (int): Maximum length of each chunk
        
    Returns:
        List[str]: List of text chunks
    """
    # Split into sentences (roughly)
    sentences = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        sentence_length = len(sentence)
        
        if current_length + sentence_length + 1 <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length + 1
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def translate_text(text: str, target_lang: str = "de") -> str:
    """
    Translates text to target language using Deep Translator.
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code (default: "de" for German)
        
    Returns:
        str: Translated text
    """
    try:
        # Initialize translator
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Split text into chunks
        chunks = chunk_text(text)
        print(f"Split text into {len(chunks)} chunks for translation")
        
        # Translate each chunk
        translated_chunks = []
        for i, chunk in enumerate(chunks, 1):
            print(f"Translating chunk {i}/{len(chunks)}...")
            translated = translator.translate(chunk)
            translated_chunks.append(translated)
        
        # Combine translated chunks
        return ' '.join(translated_chunks)
        
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
