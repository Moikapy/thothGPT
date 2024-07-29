
import ollama
def pick_ollama_model(target_model='llama3.1:latest'):
    """
    Ensures the specified OLLAMA model is installed.

    If not installed, it will be pulled from the repository.

    Args:
        ollama (OLLAMA instance): The OLLAMA instance to interact with.
        target_model (str, optional): The desired model name. Defaults to 'llama3.1:latest'.

    Returns:
        list: A list of installed model names.
    """
    installed = ollama.list()
    if not installed['models']:
        ollama.pull(target_model)
    return [model['name'] for model in installed['models']]
