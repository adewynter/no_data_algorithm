# The No-Data Algorithm
Code and data for the paper Labelling Data With Unkown References. 
This paper shows that it is possible to ascertain trust in an evaluator via an algorithm (the No-Data Algorithm). The algorithm is a zero-knowledge proof; i.e., it is **cryptographically secure** (think of how authentication and blockchain are done). 

The paper some stats to show that it adjusts to the predictions (including LLMs-as-judges and reasoning models); including empirical tests (in `No-Data-Algorithm.ipynb`) and a sample application to a low-resource language (West Frisian, in `NLEvaluatorAM.ipynb`). The code in this repository is for repro purposes. 

Please note that you will need to bring your own code (namely, API keys and whatnot) to call the models. To simplify this, you just need to modify `llmclient.py` as indicated.

If you find this paper/code useful, feel free to cite this paper:

```
Anonymised
```

>_Note_: the original paper uses φ as the flip rate. The code implementation uses 1 - φ for readability. 

# Licence

MIT Licence for everything that is not part of the Frisian data. The Frisian data was sourced from [OpenOrca](https://huggingface.co/datasets/Open-Orca/OpenOrca), [MMLU](https://huggingface.co/datasets/cais/mmlu), [OpenCode](https://huggingface.co/datasets/nvidia/OpenCodeReasoning), and [WildChat](https://huggingface.co/datasets/allenai/WildChat-1M). They contain their own licences.
