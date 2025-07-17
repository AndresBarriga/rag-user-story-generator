import tiktoken

PRICING = {
    "gpt-4o-mini": {"input": 0.0005, "output": 0.0015},  # USD per 1K tokens
    "gpt-4o": {"input": 0.005, "output": 0.015},
    # Puedes agregar más modelos si los usas
}

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """
    Cuenta el número de tokens en un texto para un modelo dado.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback encoding si el modelo no está registrado
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def estimate_cost(input_text: str, output_text: str, model: str = "gpt-4o-mini") -> dict:
    """
    Estima el coste en USD para la petición de entrada y la respuesta de salida.
    """
    input_tokens = count_tokens(input_text, model)
    output_tokens = count_tokens(output_text, model)
    input_cost = (input_tokens / 1000) * PRICING[model]["input"]
    output_cost = (output_tokens / 1000) * PRICING[model]["output"]
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_cost_usd": round(input_cost + output_cost, 6),
    }
if __name__ == "__main__":
    print("cost_estimator.py loaded successfully")