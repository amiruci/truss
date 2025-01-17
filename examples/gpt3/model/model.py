from typing import Dict, List

import openai


def _run_gpt3(gpt3_input: dict):
    # Using completion API, much more here to uncover,
    # see https://beta.openai.com/docs/api-reference/completions/create
    prompt = gpt3_input.pop("prompt")
    response = openai.Completion.create(engine="davinci", prompt=prompt, **gpt3_input)
    completion = response.choices[0].text
    return {"output": completion}


class GPT3Model(object):
    def __init__(self, **kwargs) -> None:
        self._config = kwargs["config"]
        openai.api_key = self._config["secrets"]["openai_api_key"]

    def predict(self, request: Dict) -> Dict[str, List]:
        """
        request (Dict): Must have a key 'inputs' that maps to a list of
            dicts that contain keys 'prompt' with a str value.
            Example: {"inputs" : [{"prompt" : "Hello world!"}]}
        """
        inputs = request["inputs"]
        predictions = []
        for gpt3_input in inputs:
            predictions.append(_run_gpt3(gpt3_input))
        return {"predictions": predictions}
