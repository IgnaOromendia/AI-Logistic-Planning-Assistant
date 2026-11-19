from rag.search import search

def generate_answer(question):
    results = search(question)

    context = "\n\n".join(
        f"Fuente: {r['source']}\n{r['text']}"
        for r in results
    )

    messages = [
        {
            "role": "system",
            "content": "Sos un asistente de logística. Respondé únicamente con la información del contexto proporcionado. Si no encontrás la respuesta, indicalo."
        },
        {
            "role": "user",
            "content": f"""
                        Contexto:
                        {context}

                        Pregunta:
                        {question}
                        """
        }
    ]

    return messages