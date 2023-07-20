import os
import openai
from flask import Flask, render_template, request
from collections import deque
from openai_utils import *

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

message_queue = deque(maxlen = 20)
image_url_queue = deque(maxlen = 1)

@app.route("/", methods=("GET", "POST"))
def index():
        
        if request.method == "POST":

            # Use a single prompt to generate both images and copy to get the flow started
            queue_copy(request.form["initial_prompt"], message_queue)
            queue_images(request.form["initial_prompt"], image_url_queue)

            return render_template("editor.html", 
                                   ad_gen_copy = message_queue[-1]['content'], 
                                   ad_gen_images = image_url_queue[0])

        return render_template("index.html")


@app.route("/editor", methods=("GET", "POST"))
def editor():
        
    if request.method == "POST":

        if 'user_copy_prompt' in request.form:
            # Generate new copy if a non-empty prompt is submitted on the copy form
            if request.form["user_copy_prompt"] != '':
                queue_copy(request.form["user_copy_prompt"], message_queue)

        if 'user_image_prompt' in request.form:
            # Generate new images if a non-empty prompt is submitted on the image form
            if request.form["user_image_prompt"] != '':
                queue_copy(request.form["user_image_prompt"], image_url_queue)

        return render_template("editor.html", 
                                ad_gen_copy = message_queue[-1]['content'], 
                                ad_gen_images = image_url_queue[0])

    # static page result
    return render_template("editor.html", 
                           ad_gen_copy = message_queue[-1]['content'], 
                           ad_gen_images = image_url_queue[0])