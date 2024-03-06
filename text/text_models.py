from transformers import BartForConditionalGeneration, BartTokenizer, T5ForConditionalGeneration, T5Tokenizer, PegasusForConditionalGeneration, PegasusTokenizer
from rouge_score import rouge_scorer
from nltk.tokenize import sent_tokenize
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

def baseline_summarizer(document):
    # Tokenize text into sentences
    sentences = sent_tokenize(document)
    summary_ratio = 0.2  # Set the ratio of sentences to include in the summary

    # Calculate the length of the summary
    summary_length = max(1, int(len(sentences) * summary_ratio))  # Ensure summary_length is at least 1

    # Select the first 'summary_length' sentences as the summary
    summary = sentences[:summary_length]

    # Join the sentences to form the final summary
    summary = ' '.join(summary)

    return summary

def summarize_text_bart(document):
    # Load pre-trained BART model and tokenizer
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    # Generate summary
    inputs = tokenizer.encode("summarize: " + document, return_tensors="pt", truncation=True)
    max_summary_length = int(len(inputs[0]) * 0.5)
    outputs = model.generate(inputs, max_length=max_summary_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary

def summarize_text_t5(document):
    # Load pre-trained T5 model and tokenizer
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')

    # Tokenize and encode the document
    inputs = tokenizer("summarize: " + document, return_tensors='pt')

    # Generate summary
    max_summary_length = int(len(tokenizer.encode(document)) * 0.5)
    summary_ids = model.generate(inputs['input_ids'], max_length=max_summary_length, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def summarize_text_pegasus(document):
    # Load pre-trained model and tokenizer
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-cnn_dailymail")
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-cnn_dailymail")

    # Generate summary
    inputs = tokenizer([document], return_tensors="pt", truncation=True)
    max_length = int(len(tokenizer.encode(document)) * 0.5)
    outputs = model.generate(inputs["input_ids"], max_length=max_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary

def summarize_text_pegasus2(document):
    # Load pre-trained model and tokenizer
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-large")
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-large")

    # Generate summary
    inputs = tokenizer([document], return_tensors="pt", truncation=True)
    max_length = int(len(tokenizer.encode(document)) * 0.5)
    outputs = model.generate(inputs["input_ids"], max_length=max_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary


def calculate_bleu(input_text, summary):
    # Tokenize input text and summary into sentences
    reference_sentences = sent_tokenize(input_text)
    hypothesis_sentences = sent_tokenize(summary)

    # Calculate BLEU score for all sentence pairs
    smoothing = SmoothingFunction().method1
    bleu_scores = [sentence_bleu([ref_sentence], hyp_sentence, smoothing_function=smoothing) 
                   for ref_sentence in reference_sentences for hyp_sentence in hypothesis_sentences]

    # Average the BLEU scores for all sentence pairs
    avg_bleu_score = sum(bleu_scores) / len(bleu_scores)
    
    return avg_bleu_score


def calculate_rouge_scores(input_text, summary):
    # Calculate ROUGE scores
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(input_text, summary)

    return scores
