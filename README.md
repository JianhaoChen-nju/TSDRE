# TSDRE
This is the code for our ACL 2024 paper [**Timeline-based Sentence Decomposition with In-Context Learning for Temporal Fact Extraction**]([2405.10288 (arxiv.org)](https://arxiv.org/pdf/2405.10288)).

Our work involves training multiple models and calling the ChatGPT API, making it difficult to run our code directly. Therefore, this repository mainly provides datasets for your interest in our work, as well as timeline-based decomposition results for your reference.

## Dataset

- data_process.py: Data processing functions before scoring

- scoring.py: Scoring function

- test.py: Scoring using scoring functions

  Run test.py after changing the two parameters **path_gold** and **path_pred**. The **path_gold** parameter is the dataset test file path(usually Datasets/HyperRED-Temporal/test.json or Datasets/ComplexTRED/test.json), and the **path_pred** parameter is the model prediction file path.

**Datasets** folder: Files for two datasets **HyperRED-Temporal** and **ComplexTRED**.

## Timeline-based Sentence Decomposition

**Decomposition** folder: Decomposition prompt and results.

## Results

**Results** folder: TSDRE SOTA results on two datasets **HyperRED-Temporal** and **ComplexTRED**.

## Citation

```
@inproceedings{chen2024timeline,
  title={Timeline-based Sentence Decomposition with In-Context Learning for Temporal Fact Extraction},
  author={Chen, Jianhao and Ouyang, Haoyuan and Ren, Junyang and Ding, Wentao and Hu, Wei and Qu, Yuzhong},
  booktitle={Annual Meeting of the Association for Computational Linguistics},
  year={2024}
}
```

