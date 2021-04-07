from utils.helpers import read_lines
from gector.gec_model import GecBERTModel
import language_check as lc
import os
import requests
import sys

tool = lc.LanguageTool('en-US')


def download_model():
    link = "http://imdreamer.oss-cn-hangzhou.aliyuncs.com/bert_0_gector.th"
    with open('./model/bert_0_gector.th', "wb") as f:
        print('Downloading grammatical error correction model [bert_0_gector]! Please wait a minute!')
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()


def language_checker(text):
    matches = tool.check(text)
    correct_text = lc.correct(text, matches)
    return correct_text


def predict_for_file(input_file, output_file, model, batch_size=32):
    test_data = read_lines(input_file)
    predictions = []
    cnt_corrections = 0
    batch = []
    for sent in test_data:
        batch.append(language_checker(sent).split())
        if len(batch) == batch_size:
            preds, cnt = model.handle_batch(batch)
            predictions.extend(preds)
            cnt_corrections += cnt
            batch = []
    if batch:
        preds, cnt = model.handle_batch(batch)
        predictions.extend(preds)
        cnt_corrections += cnt

    with open(output_file, 'w') as f:
        f.write("\n".join([" ".join(x) for x in predictions]) + '\n')
    return cnt_corrections


def predict_for_string(input_string, model):
    predictions = []
    cnt_corrections = 0
    batch = [language_checker(input_string).split()]
    if batch:
        preds, cnt = model.handle_batch(batch)
        predictions.extend(preds)
        cnt_corrections += cnt
    return [" ".join(x) for x in predictions]


def grammar_correction(is_file_or_string, input_message_string):
    """
    vocab_path: Path to the vocab file.
    model_paths: Path to the model file.
    max_len: The max sentence length(all longer will be truncated). type->int
    min_len: The minimum sentence length(all longer will be returned w/o changes) type-> int
    iterations: The number of iterations of the model. type->int
    min_error_probability: Minimum probability for each action to apply.
                           Also, minimum error probability, as described in the paper. type->float
    lowercase_tokens: The number of iterations of the model. type->int
    model_name: Name of the transformer model.you can chose['bert', 'gpt2', 'transformerxl', 'xlnet', 'distilbert', 'roberta', 'albert']
    special_tokens_fix: Whether to fix problem with [CLS], [SEP] tokens tokenization.
                        For reproducing reported results it should be 0 for BERT/XLNet and 1 for RoBERTa. type->int
    confidence: How many probability to add to $KEEP token. type->float
    is_ensemble: Whether to do ensembling. type->int
    weigths: Used to calculate weighted average.
    batch_size: The size of hidden unit cell.
    :return:
    """
    if not os.path.exists('./model/bert_0_gector.th'):
        download_model()

    model = GecBERTModel(vocab_path='./data/output_vocabulary',
                         model_paths=['./model/bert_0_gector.th'],
                         max_len=50, min_len=3,
                         iterations=5,
                         min_error_probability=0.0,
                         lowercase_tokens=0,
                         model_name='bert',
                         special_tokens_fix=0,
                         log=False,
                         confidence=0,
                         is_ensemble=0,
                         weigths=None)
    if is_file_or_string:
        predict_for_file('./data/predict_for_file/input.txt',
                                           './data/predict_for_file/output.txt',
                                           model,
                                           batch_size=128)
        return 'process incorrect input file successful!'
    else:
        correct_commit_msg = predict_for_string(input_message_string, model)
        return correct_commit_msg[0]
