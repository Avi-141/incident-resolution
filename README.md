# incident-resolution-v1-basic-works-better?

1. Download Ollama
2. Pull required language models of your choice
3. Pull nomic-embeddings as the os embedding model
4. Embeddings will be created locally in a json file acting as a "DB"

```python3 rag_ollama_basic.py```



# incident-resolution-v2-streamlit-langchain

Ollama needed
1. Start ollama.
2. Chroma DB as inmemory vector DB
3. (Create venv) -- good pracc

```pip install -r requirements.txt```
```streamlit run ui.py```


UI running on localhost.
Index documents located in "incidents" folder
Talk to LLM Bot

