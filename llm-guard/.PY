from langchain.llms import Ollama

llm = Ollama(model="llama2")

def summarize_incident(log_data):
    prompt = f"""
    Analyze the following inference logs and summarize root cause:

    {log_data}
    """

    response = llm(prompt)
    return response

if __name__ == "__main__":
    sample_log = "High latency spike on model v2.1, PSI increased to 0.35."
    summary = summarize_incident(sample_log)
    print(summary)
