from langchain_community.llms import Ollama # type: ignore
from langchain_community.embeddings import OllamaEmbeddings # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain_community.vectorstores import Chroma # type: ignore
# from langchain.retrievers import BM25Retriever, HybridRetriever #type: ignore
# Weaviate Hybrid search chroma
#from langchain.chains import ReRankerChain

from models import check_if_model_is_available
from document_loader import load_documents_into_database
import argparse
import sys

from llm import getChatChain


def main(llm_model_name: str, embedding_model_name: str, documents_path: str) -> None:
    # Check to see if the models available, if not attempt to pull them
    try:
        check_if_model_is_available(llm_model_name)
        check_if_model_is_available(embedding_model_name)
    except Exception as e:
        print(e)
        sys.exit()

    # Creating database form documents
    try:
        db = load_documents_into_database(embedding_model_name, documents_path)
        # documents = db.get_all_documents()
        # bm25_retriever = BM25Retriever.from_documents(documents)
        # #hybrid_retriever = HybridRetriever(retrievers=[db.as_retriever(), bm25_retriever])
    except FileNotFoundError as e:
        print(e)
        sys.exit()

    llm = Ollama(model=llm_model_name)
    # reranker = ReRankerChain(llm=llm, retriever=hybrid_retriever)
    chat = getChatChain(llm,db) # hybrid_retriever, #reranker)

    while True:
        try:
            user_input = input(
                "\n\nPlease enter your question (or type 'exit' to end): "
            )
            if user_input.lower() == "exit":
                break

            chat(user_input)
        except KeyboardInterrupt:
            break


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local LLM with RAG with Ollama.")
    parser.add_argument(
        "-m",
        "--model",
        default="mistral",
        help="The name of the LLM model to use.",
    )
    parser.add_argument(
        "-e",
        "--embedding_model",
        default="nomic-embed-text",
        help="The name of the embedding model to use.",
    )
    parser.add_argument(
        "-p",
        "--path",
        default="Research",
        help="The path to the directory containing documents to load.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.model, args.embedding_model, args.path)
