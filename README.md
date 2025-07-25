# The No-Data Algorithm
Code and data for the paper ['Labelling Data With Unkown References'](https://arxiv.org/abs/2506.03083), by Adrian de Wynter. 
This paper shows that it is possible to ascertain trust in an evaluator via an algorithm (the No-Data Algorithm). The algorithm is a zero-knowledge proof; i.e., it is **cryptographically secure** (think of how authentication and blockchain are done). 

The paper some stats to show that it adjusts to the predictions (including LLMs-as-judges and reasoning models), but my favourite bit is that it based of a formal proof (of the zero-knowledge proof). 
The code in this repository is for repro purposes. 

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
