# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .text_models import summarize_text_pegasus2,summarize_text_bart, baseline_summarizer, summarize_text_t5, summarize_text_pegasus,calculate_bleu ,calculate_rouge_scores
from docx import Document
import PyPDF2
import os
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def summarize(request):
    if request.method == 'POST':
        input_text = ''
        results = {}
        
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            file_extension = os.path.splitext(uploaded_file.name)[1]

            # Check file extension and extract text accordingly
            if file_extension.lower() == '.pdf':
                input_text = extract_text_from_pdf(uploaded_file)
            elif file_extension.lower() == '.docx':
                input_text = extract_text_from_docx(uploaded_file)
            else:
                return HttpResponse("Unsupported file format")
        else:
            input_text = request.POST.get('text', '')

        selected_models = request.POST.getlist('models')

        # Mapping of model names to functions
        model_functions = {
            'Baseline': baseline_summarizer,
            'Pegasus2':summarize_text_pegasus2,
            'BART': summarize_text_bart,
            'T5': summarize_text_t5,
            'Pegasus': summarize_text_pegasus,
        }
       
        # Call the selected model functions
        for model_name in selected_models:
            if model_name in model_functions:
                model_function = model_functions[model_name]
                summarized_text = model_function(input_text)
                rouge_scores = calculate_rouge_scores(input_text, summarized_text)
                bleu_score = calculate_bleu(summarized_text,input_text)
                results[model_name] = {
                    'summarized_text': summarized_text,
                    'rouge1_precision': rouge_scores['rouge1'].precision,
                    'rouge1_recall': rouge_scores['rouge1'].recall,
                    'rouge1_f1': rouge_scores['rouge1'].fmeasure,
                    'rouge2_precision': rouge_scores['rouge2'].precision,
                    'rouge2_recall': rouge_scores['rouge2'].recall,
                    'rouge2_f1': rouge_scores['rouge2'].fmeasure,
                    'rougel_precision': rouge_scores['rougeL'].precision,
                    'rougel_recall': rouge_scores['rougeL'].recall,
                    'rougel_f1': rouge_scores['rougeL'].fmeasure,
                    'bleu_score':bleu_score,
                }
        
        # Extracting the metrics for each model
        model_names = list(results.keys())
        rouge1_f1_scores = [results[model]['rouge1_f1'] for model in model_names]
        rouge2_f1_scores = [results[model]['rouge2_f1'] for model in model_names]
        rougel_f1_scores = [results[model]['rougel_f1'] for model in model_names]
        bleu_scores = [results[model]['bleu_score'] for model in model_names]
        # Plotting the bar chart
        bar_width = 0.2
        index = np.arange(len(model_names))

        plt.bar(index, rouge1_f1_scores, bar_width, label='Rouge-1')
        plt.bar(index + bar_width, rouge2_f1_scores, bar_width, label='Rouge-2')
        plt.bar(index + 2 * bar_width, rougel_f1_scores, bar_width, label='Rouge-L')
        plt.bar(index + 3 * bar_width, bleu_scores, bar_width, label='Bleu')
        plt.xlabel('Models')
        plt.ylabel('Scores')
        plt.title('Summarization Model Performance')
        plt.xticks(index + bar_width, model_names)
        plt.legend()

        plt.tight_layout()

        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        buffer_data = buffer.getvalue()
        buffer.close()

        # Encode the image bytes as base64 to pass to the template
        graph_base64 = base64.b64encode(buffer_data).decode('utf-8')
        
        # Prepare context to pass to the template
        context = {
            'input_text': input_text,
            'results': results,
            'graph_base64': graph_base64  # Pass the base64 encoded image to the template
        }

        return render(request, 'output.html', context)   
    
    return render(request, 'index.html')
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


def extract_text_from_pdf(file):
    
    text = ''
    pdf_reader = PyPDF2.PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text
def extract_text_from_docx(file):
    
    doc = Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
def services(request):
    return render(request,'services.html')
def index (request):
    return render(request,'index.html')
def output(request):
    return render(request, "output.html")
def team(request):
    return render(request, "team.html")