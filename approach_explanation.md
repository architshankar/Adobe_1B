Approach Explanation: Persona-Driven Document Intelligence
The goal of our solution is to build a **generic, lightweight document intelligence system** that extracts and ranks the most relevant sections and sentences from a diverse set of PDF documents based on a given *persona* and their *job-to-be-done*. The architecture is designed to be domain-agnostic, performant on CPU, and under the 1GB model size constraint — with execution times under 60 seconds for collections of 3–5 documents.

1.Input Understanding & Query Formation

The system begins by reading `challenge1b_input.json`, which contains:
* A persona definition (e.g., "PhD Researcher in Computational Biology")
* job-to-be-done (e.g., "Prepare a literature review on GNNs for drug discovery")
We concatenate these into a semantic query, which becomes the basis for relevance scoring against the document content.

2.PDF Section Extraction

We use PyMuPDF (`fitz`) to extract raw text from PDFs and split it into semantically meaningful sections**. A rule-based heuristic identifies headers and section breaks:

* Headers are detected by checking if lines are in **UPPERCASE** or **Title Case** with limited word count.
* Content under each heading is grouped into a section with title, text, page number, and document name.
This step ensures structure across various document types like research papers, textbooks, or reports.

3.Text Embedding and Relevance Scoring
To evaluate semantic relevance:

* We use the **SentenceTransformer** model `all-MiniLM-L6-v2` (∼80MB), suitable for CPU and under the 1GB limit.
* The persona+job query and all section texts are embedded into vectors using the model.
* We compute **cosine similarity** between the query and each section embedding to get a relevance score.

The top 5 sections are ranked by this similarity and selected for output.
4. Fine-Grained Sub-Section Extraction

Each selected section undergoes sentence-level analysis

* Sentences are split using spaCy’s lightweight `sentencizer`.
* Each sentence is embedded and scored for similarity against the query.
* The **top 2 sentences** per section are selected as the most granular, actionable insights.

5. Output Generation
 The final output is written to `challenge1b_output.json` and includes:

* Metadata (documents, persona, job, timestamp)
* Top 5 ranked sections (with page number, title, document)
* Top 10 refined sentences from these sections for fine-grained insight

Why This Works

* Generic: Works across any domain due to embedding-based semantic understanding.
* Efficient: Lightweight model, fast text parsing, CPU-optimized.
* Relevant: Dual-level (section + sentence) ranking boosts precision.
* Interpretable: Clearly labeled sections and source pages for transparency.