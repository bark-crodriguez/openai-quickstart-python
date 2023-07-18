import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from collections import deque
from instructions import ad_text_gen, image_text_gen

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

message_queue = deque(maxlen = 20)

@app.route("/", methods=("GET", "POST"))
def index():

    # execute when submit button is pressed
    if request.method == "POST":

        # copy prompt
        if 'initial_prompt' in request.form:

            user_copy_prompt = request.form["initial_prompt"]
            user_image_prompt = request.form["initial_prompt"]

        # if 'user_copy_prompt' in request.form:

        #     user_copy_prompt = request.form["initial_prompt"]

        message_queue.append({'role': 'user', 'content': user_copy_prompt})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= ad_text_gen + list(message_queue),
            max_tokens=200,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0
        )

        # image prompt
        img_result = openai.Image.create(
            prompt='''
            {}
            {}'''.format(image_text_gen, user_image_prompt),
            n=3,
            size="1024x1024"
            )

        message_queue.append({'role': 'assistant', 'content': completion['choices'][0]['message']['content']})
        image_urls = [item['url'] for item in img_result['data']]

        return redirect(url_for("index", 
                                ad_gen_copy = message_queue[-1]['content'],
                                ad_gen_image = image_urls))

    # static page result
    ad_gen_copy = request.args.get("ad_gen_copy")
    ad_gen_image = request.args.getlist("ad_gen_image")
    return render_template("index.html", 
                           ad_gen_copy = ad_gen_copy, 
                           ad_gen_image = ad_gen_image)