from operator import itemgetter

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # type: ignore
from langchain.memory import ConversationBufferMemory # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore
from langchain_core.runnables import RunnableLambda, RunnablePassthrough # type: ignore
from langchain_core.messages import get_buffer_string # type: ignore
from langchain_core.prompts import format_document # type: ignore
from langchain.prompts.prompt import PromptTemplate # type: ignore

#WizardLM2 Prompt for best results
#A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. #USER: Hi ASSISTANT: Hello.</s>USER: Who are you? ASSISTANT: I am WizardLM.</s>......

condense_question = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.

Chat History:
{chat_history}

Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question)

answer = """
### Instruction:
You are a customer support agent from Tier 1 team of MCMP, an internal Cisco IT platform. Your job is to answer any questions posed to you, based on the context provided. You are allowed to make an intelligent decision to club multiple answers together, but as points. If you're unsure, just say "I would suggest getting more details on this case.

## Context:
{context}

## Question:
{question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(answer)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="Source Document: {source}, Page {page}:\n{page_content}"
)


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


memory = ConversationBufferMemory(
    return_messages=True, output_key="answer", input_key="question"
)


def getStreamingChain(question: str, memory, llm, db):
    retriever = db.as_retriever(search_kwargs={"k": 5})
    loaded_memory = RunnablePassthrough.assign(
        chat_history=RunnableLambda(
            lambda x: "\n".join(
                [f"{item['role']}: {item['content']}" for item in x["memory"]]
            )
        ),
    )

    standalone_question = {
        "standalone_question": {
            "question": lambda x: x["question"],
            "chat_history": lambda x: x["chat_history"],
        }
        | CONDENSE_QUESTION_PROMPT
        | llm
    }

    retrieved_documents = {
        "docs": itemgetter("standalone_question") | retriever,
        "question": lambda x: x["standalone_question"],
    }

    final_inputs = {
        "context": lambda x: _combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    answer = final_inputs | ANSWER_PROMPT | llm

    final_chain = loaded_memory | standalone_question | retrieved_documents | answer

    return final_chain.stream({"question": question, "memory": memory})


def getChatChain(llm, db):
    retriever = db.as_retriever(search_kwargs={"k": 10})

    loaded_memory = RunnablePassthrough.assign(
        chat_history=RunnableLambda(memory.load_memory_variables)
        | itemgetter("history"),
    )

    standalone_question = {
        "standalone_question": {
            "question": lambda x: x["question"],
            "chat_history": lambda x: get_buffer_string(x["chat_history"]),
        }
        | CONDENSE_QUESTION_PROMPT
        | llm
    }

    # Now we retrieve the documents
    retrieved_documents = {
        "docs": itemgetter("standalone_question") | retriever,
        "question": lambda x: x["standalone_question"],
    }

    # Now we construct the inputs for the final prompt
    final_inputs = {
        "context": lambda x: _combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    # And finally, we do the part that returns the answers
    answer = {
        "answer": final_inputs
        | ANSWER_PROMPT
        | llm.with_config(callbacks=[StreamingStdOutCallbackHandler()]),
        "docs": itemgetter("docs"),
    }

    final_chain = loaded_memory | standalone_question | retrieved_documents | answer

    def chat(question: str):
        inputs = {"question": question}
        result = final_chain.invoke(inputs)
        memory.save_context(inputs, {"answer": result["answer"]})

    return chat
