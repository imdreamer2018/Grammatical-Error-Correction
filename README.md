# Grammatical-Error-Correction

Grammatical-Error-Correction is an NLP-based spelling and grammar correction tool that accepts articles as well as raw text and returns a corrected sentence. Grammatical-Error-Correction is built using Python, powered by data and makes use of core NLP techniques. It is mainly based on `AllenNLP` and `transformers`.

------

![Grammatical-Error-Correction](https://imdreamer.oss-cn-hangzhou.aliyuncs.com/picGo/Grammatical-Error-Correction.png)

------

## Example usage

Grammatical-Error-Correction can correct the spelling and grammar of sentences.

```shell
he go to scholl -> He goes to school
```

#### From the interpreter:

```python
>>> from src.checker import grammar_correction
>>> input_sentence = 'he go to scholl'
>>> correct_sentence = grammar_correction(False, input_sentence)
>>> correct_sentence
'He goes to school'
```

#### Api Support:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"text":"he go to a school by bika every day."}' http://127.0.0.1:21046/api/texts
#return -> He goes to school by bike every day.
```

## Install

```shell
#environment python3.6
https://github.com/imdreamer2018/Grammatical-Error-Correction.git
pip install -r requirements.txt
python app.py
```

click http://127.0.0.1:21046

------

## Prerequisites

- python3.6
- Java8

## Docker depoly

You can build your docker images or pull my docker images.

#### Build your docker images

```shell
docker build .
docker run -itd --name grammatical-error-correction -p 21046:21046 -d [your docker image id]
```

#### Pull my docker images

```shell
docker pull imdreamer/grammatical-error-correction:v1.0
docker run -itd --name grammatical-error-correction -p 21046:21046 -d [your docker image id]
```

## Tree

```shell
.
├── Dockerfile
├── README.md
├── app.py
├── data
│   ├── output_vocabulary
│   ├── predict_for_file
│   └── verb-form-vocab.txt
├── gector
│   ├── bert_token_embedder.py
│   ├── datareader.py
│   ├── gec_model.py
│   ├── seq2labels_model.py
│   ├── trainer.py
│   └── wordpiece_indexer.py
├── model
│   └── bert_0_gector.th
├── requirements.txt
├── src
│   └── checker.py
├── templates
│   └── index.html
└── utils
    ├── helpers.py
    ├── prepare_clc_fce_data.py
	  └── preprocess_data.py
```

## Reference

- **[language_check](https://github.com/myint/language-check)** (great spelling-correction library with extensive support for simple grammar suggestions, punctuation errors)
- **[GECToR](https://github.com/grammarly/gector)**(training and testing state-of-the-art models for grammatical error correction with the official PyTorch)

## License

[MIT](https://github.com/imdreamer2018/Grammatical-Error-Correction/blob/master/LICENSE) © Imdreamer

