# The No-Data Algorithm
Code and data for the paper ['Labelling Data With Unkown References'](https://arxiv.org/abs/2506.03083), by Adrian de Wynter. 
This paper shows that it is possible to ascertain trust in an evaluator via an algorithm (the No-Data Algorithm). The algorithm is a zero-knowledge proof; i.e., it is **cryptographically secure** (think of how authentication and blockchain are done). 

The paper some stats to show that it adjusts to the predictions (including LLMs-as-judges and reasoning models); including empirical tests (in `No-Data-Algorithm.ipynb`) and a sample application to a low-resource language (West Frisian, in `NLEvaluatorAM.ipynb`). The code in this repository is for repro purposes. 

Please note that you will need to bring your own code (namely, API keys and whatnot) to call the models. To simplify this, you just need to modify `llmclient.py` as indicated.

If you find this paper/code useful, feel free to cite this paper:

```
@misc{dewynter2025labellingdataunknownreferences,
      title={Labelling Data with Unknown References}, 
      author={Adrian de Wynter},
      year={2025},
      eprint={2506.03083},
      archivePrefix={arXiv},
      primaryClass={cs.DS},
      url={https://arxiv.org/abs/2506.03083}, 
}
```

# Licence

MIT Licence for everything that is not part of the Frisian data. The Frisian data was sourced from [OpenOrca](https://huggingface.co/datasets/Open-Orca/OpenOrca), [MMLU](https://huggingface.co/datasets/cais/mmlu), [OpenCode](https://huggingface.co/datasets/nvidia/OpenCodeReasoning), and [WildChat](https://huggingface.co/datasets/allenai/WildChat-1M). They contain their own licences.