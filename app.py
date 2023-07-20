import os
import openai
from flask import Flask, render_template, request, session
from openai_utils import *

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
        
    session['message_queue'] = [] 
    session['image_url_queue'] = []
        
    if request.method == "POST":

        # Use a single prompt to generate both images and copy to get the flow started
        session['message_queue'] = queue_copy(request.form["initial_prompt"], session['message_queue'])
        session['image_url_queue'] = queue_images(request.form["initial_prompt"], session['image_url_queue'])

        return render_template("editor.html", 
                                ad_copy = session['message_queue'][-1]['content'], 
                                ad_images = session['image_url_queue'][-1])

    return render_template("index.html")


@app.route("/editor", methods=("GET", "POST"))
def editor():
        
    if request.method == "POST":

        if 'user_copy_prompt' in request.form:
            # Generate new copy if a non-empty prompt is submitted on the copy form
            if request.form["user_copy_prompt"] != '':
                session['message_queue'] = queue_copy(request.form["user_copy_prompt"], session['message_queue'])

        if 'user_image_prompt' in request.form:
            # Generate new images if a non-empty prompt is submitted on the image form
            if request.form["user_image_prompt"] != '':
                session['image_url_queue'] = queue_images(request.form["user_image_prompt"], session['image_url_queue'])

        return render_template("editor.html", 
                           ad_copy = session['message_queue'][-1]['content'], 
                           ad_images = session['image_url_queue'][-1])

    # static page result
    return render_template("editor.html", 
                           ad_copy = session['message_queue'][-1]['content'], 
                           ad_images = session['image_url_queue'][-1])