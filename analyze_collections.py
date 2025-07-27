
import os
import json
from datetime import datetime
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import sys

MODEL_NAME = 'all-MiniLM-L6-v2'

nlp = spacy.blank('en')
nlp.add_pipe('sentencizer')


def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        current_section = {'title': f'Page {page_num+1}', 'text': '', 'page': page_num+1}
        for line in lines:
            if (line.isupper() or (line.istitle() and len(line.split()) < 10)) and len(line) > 5:
                if current_section['text']:
                    sections.append(current_section)
                current_section = {'title': line.strip(), 'text': '', 'page': page_num+1}
            else:
                current_section['text'] += line + '\n'
        if current_section['text']:
            sections.append(current_section)
    return sections


def embed_texts(texts, model):
    return model.encode(texts, show_progress_bar=False)


def process_collection(collection_path, collection_name):
    input_json = os.path.join(collection_path, 'challenge1b_input.json')
    with open(input_json, 'r', encoding='utf-8') as f:
        config = json.load(f)
    persona = config['persona']['role']
    job = config['job_to_be_done']['task']
    pdf_dir = os.path.join(collection_path, 'PDFs')
    pdf_files = [os.path.join(pdf_dir, doc['filename']) for doc in config['documents']]
    pdf_filenames = [doc['filename'] for doc in config['documents']]

    model = SentenceTransformer(MODEL_NAME)
    query = persona + ' ' + job
    query_emb = embed_texts([query], model)[0]

    all_sections = []
    for pdf, pdf_filename in zip(pdf_files, pdf_filenames):
        if not os.path.exists(pdf):
            continue
        sections = extract_sections_from_pdf(pdf)
        for sec in sections:
            sec['document'] = pdf_filename
            all_sections.append(sec)

    section_texts = [sec['title'] + '\n' + sec['text'] for sec in all_sections]
    if section_texts:
        section_embs = embed_texts(section_texts, model)
        if len(section_embs) > 0:
            sims = cosine_similarity([query_emb], section_embs)[0]
            ranked = sorted(zip(all_sections, sims), key=lambda x: -x[1])
        else:
            sims = []
            ranked = []
    else:
        section_embs = []
        sims = []
        ranked = []

    extracted_sections = []
    subsection_analysis = []
    for rank, (sec, sim) in enumerate(ranked[:5], 1):
        extracted_sections.append({
            'document': sec['document'],
            'section_title': sec['title'],
            'importance_rank': rank,
            'page_number': sec['page']
        })
        # Sub-section: split into sentences, pick top 2 by similarity
        sentences = [s.text for s in nlp(sec['text']).sents] if sec['text'] else []
        if not sentences:
            sentences = sec['text'].split('. ')
        sent_embs = embed_texts(sentences, model) if sentences else []
        if len(sent_embs) > 0:
            sent_sims = cosine_similarity([query_emb], sent_embs)[0]
            top_idx = sorted(range(len(sent_sims)), key=lambda i: -sent_sims[i])[:2]
            for idx in top_idx:
                subsection_analysis.append({
                    'document': sec['document'],
                    'refined_text': sentences[idx].strip(),
                    'page_number': sec['page']
                })

    output = {
        'metadata': {
            'input_documents': pdf_filenames,
            'persona': persona,
            'job_to_be_done': job,
            'processing_timestamp': datetime.now().isoformat()
        },
        'extracted_sections': extracted_sections,
        'subsection_analysis': subsection_analysis
    }

    # Write output to the same directory as the input JSON
    out_path = os.path.join(collection_path, 'challenge1b_output.json')

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
    print(f'Processed {collection_path}, output written to {out_path}')

def main():
    # base_dir = "."
    base_dir = "/app/input"

    if len(sys.argv) > 1:
        collection = sys.argv[1]
        collection_path = os.path.join(base_dir, collection)
        if os.path.isdir(collection_path) and os.path.exists(os.path.join(collection_path, 'challenge1b_input.json')):
            process_collection(collection_path, collection)
        else:
            print(f"Collection {collection} not found or missing input JSON.")
    else:
        for collection in os.listdir(base_dir):
            collection_path = os.path.join(base_dir, collection)
            if os.path.isdir(collection_path) and os.path.exists(os.path.join(collection_path, 'challenge1b_input.json')):
                process_collection(collection_path, collection)


if __name__ == '__main__':
    main()