# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__,static_url_path="/static")

#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    print(request.form['msg'])
    res = list()
    for fir in request.form['msg'].split("，"):
        res.append(fir)
    res_set = set(res)
    # remove some duplicated lyrics
    for i in range(10):
        n = 4
        while len(basic_tokenizer("，".join(res[-n:]))) > 65 and n > 1:
            n -= 1
        cand = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, u'，'.join(res[-n:]))
        while cand in res_set and n > 1:
            n -= 1
            cand = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, u'，'.join(res[-n:]))
        if cand != res[-1]:
            while len(res) > 1 and res[-1] == res[-2]:
                res.pop()		
        res.append(cand)
        res_set.add(cand)
    while len(res) > 1 and res[-1] == res[-2]:
        res.pop()
    return jsonify( { 'text': "\n".join(res) } )

@app.route("/")
def index():
    return render_template("index.html")
#############

'''
Init seq2seq model

    1. Call main from execute.py
    2. Create decode_line function that takes message as input
'''
#_________________________________________________________________
import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import tensorflow as tf
import execute
from data_utils import basic_tokenizer

sess = tf.Session()
sess, model, enc_vocab, rev_dec_vocab = execute.init_session(sess, conf='seq2seq_serve.ini')
#_________________________________________________________________

# start app
if (__name__ == "__main__"):
    app.run(port = 5000)
