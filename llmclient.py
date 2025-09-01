import transformers
from transformers import pipeline
#transformers.logging.set_verbosity_error()

class LLMClient():

    def __init__(self, params: dict, model_id: str, is_dumb=False):
        """
        Base skeleton class for the LLM Client. 
        Pass in a dictionary of call parameters (e.g., `params={"max_tokens": 6}`),
        and a `model_id` (qwen-2.5-vl... etc).
        `is_dumb` is for compatibility for these models that for some reason have temperature set between [0, 2].
        """
        self._pipeline = pipeline(
            "text-generation",
            model=model_id,
            device_map="auto",
        )
        self._is_dumb = is_dumb 
        self._params = params
        self._model = model_id

    def send_request(self, assembled_prompt: list):
        '''
        The `assembled_prompt` should already be in a format admissible by the model.
        This means that it should be a list of the form [{"role": "whatever", "content": "etc"}]
        '''
        outputs = self._pipeline(assembled_prompt, 
                           temperature=self._params["temperature"] if self._is_dumb else self._params["temperature"]/2, 
                           max_new_tokens=self._params["max_tokens"],
                           pad_token_id = self._pipeline.tokenizer.eos_token_id)
        return outputs

    def update_params(self, params: dict):
        '''
        Perform a parameter update. It will only overwrite the chosen parameters (e.g., temperature)
        '''
        for k, v in params.items():
            self._params[k] = v


def get_llm_response(model: LLMClient, assembled_prompt: list, debug=False, force=False):
    """
    Basic skeleton function to call LLMs. When you work with HF stuff, this is
    borderline redundant. But if you call an API you should include here retry logic.
    That's what `force` is for: if you set it to `true`, your retry logic should force it to return regardless.
    """
    resp = model.send_request(assembled_prompt)
    if debug: print(resp)
    return resp[0]["generated_text"][-1]["content"]
