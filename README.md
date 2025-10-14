# Konduit RAG (Retrieval Augmented Generation)

### Overview:
This project implements a small Retrieval-Augmented Generation (RAG) service built in Python. Its primary function is to crawl a starting URL, index the content, and answer user questions strictly based on the pages collected, citing all sources.

The entire RAG pipeline works **offline**, prioritizing grounded answers and reproducibility. If supporting evidence is lacking, the system explicitly returns:

NOT_FOUND_IN_CRAWLED_CONTENT


---

### How It Works:

| Step | Action | Tools Used |
|------|--------|------------|
| Crawl | Goes through in-domain pages (polite, max 50 pages) | requests, beautifulSoup4, urllib |
| Clean | Extracts and normalizes readable text | beautifulSoup4 |
| Chunk + Index | Splits text, converts to vector embeddings (TF-IDF), and stores them | scikit-learn, faiss |
| Retrieve + Answer | Finds top relevant chunks and generates a grounded answer | Custom Python Logic (optionally uses transformers==4.29.2 + torch if small LLM is integrated) |

---

### Setup:

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt
How to Run:
  Step	                                  Purpose                                                             Command Example
1: Crawl	                 Scrape pages from the target domain	               python main.py --crawl https://www.python.org/about/ --max_pages 3 --crawl_delay 1.0
2: Index	                 Build TF-IDF embeddings and FAISS index             python main.py --index data/pages/crawl_python.org.json
3: Ask (Answerable)        Test successful grounding and citation	             python main.py --ask "What is Python used for?"
4: Ask (Refusal)	         Test the safety guardrail	                         python main.py --ask "Who founded Google?"

Example Output:
Answerable:
Answer: Python is used for software development, web development, data analysis, scripting, and automation.
Source: https://www.python.org/about/

Refusal / Unanswerable:
Answer: NOT_FOUND_IN_CRAWLED_CONTENT

### Design Choices and Tooling

| Aspect | Choice | Justification |
|--------|--------|---------------|
| Embedding | TF-IDF (scikit-learn) | Lightweight, fully offline, no external API needed |
| Politeness | 1.0s Crawl Delay | Avoids overloading host websites |
| Retrieval | FAISS (faiss-cpu) | Efficient similarity search on sparse vectors |
| Refusal | Tuned Threshold | Ensures system refuses to answer if evidence is weak |
| Tools Used | Python 3.10, requests, beautifulsoup4, transformers==4.29.2, torch, faiss-cpu, numpy, scikit-learn | Full list for reproducibility and offline RAG functionality |

### Tooling Disclosure

| Type | Library / Model |
|------|----------------|
| Embedding | scikit-learn (TF-IDF) |
| Vector Search | faiss-cpu |
| Crawler | requests, beautifulsoup4 |
| Base LLM (Conceptual / Optional) | transformers==4.29.2, torch |
| Numerical & Utilities | numpy |


Verification        Screenshots
Screenshot	        Description
Crawl Output  	    Verifies successful data acquisition
Index Output	      Verifies indexing using offline TF-IDF
Ask (Answerable)	  Verifies grounding and source citation
Ask (Unanswerable)	Verifies refusal logic and safety guardrail

Summary:
Fully working offline RAG pipeline
Simple CLI interface
Returns answers only when supported by crawled content
Clean refusal for unsupported queries

Author: Nishant Namboodiri
Built in: PyCharm
Type: RAG 


