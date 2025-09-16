import ollama

def answer_with_model(question, context):
    """
    Ask Ollama model with given context.
    """
    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": "You are a financial assistant."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
    ])
    return response["message"]["content"]

def simple_lookup(question, metrics):
    """
    Try to match user question with extracted metrics.
    """
    q = question.lower()
    for key, value in metrics.items():
        if key.lower() in q:
            return f"{key}: {value}"
    return None
