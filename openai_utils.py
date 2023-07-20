import openai
from instructions import fixed_copy_prompt, fixed_image_prompt
from collections import deque


def get_chat_completion(message_queue):
    '''
    Make a call to the openai API chat completions endpoint.
    All calls append a short message queue (message_queue) to a predefined prompt (fixed_copy_prompt).
    '''

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= fixed_copy_prompt + list(message_queue),
        max_tokens=200,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
    )

    return completion



def get_image_from_prompt(user_image_prompt):
    '''
    Make a call to the openai API image creation endpoint.
    All calls append a short message (user_image_prompt) to a predefined prompt (fixed_image_prompt).
    '''

    img_result = openai.Image.create(
    prompt='''
    {}
    {}'''.format(fixed_image_prompt, user_image_prompt),
    n=3,
    size="1024x1024"
    )

    return img_result


def queue_copy(prompt, message_list):
    '''
    Manages the message_queue by appending to it a complete interaction between the user and the API.
    Requires both parameters as input, the user message (prompt) and the message list (message_list) to manange 
    as a queue. 
    '''
    queue = deque(maxlen = 20)
    for message in message_list:
        queue.append(message)

    queue.append({'role': 'user', 'content': prompt})
    completion = get_chat_completion(queue)
    queue.append({'role': 'assistant', 'content': completion['choices'][0]['message']['content']})

    return list(queue)


def queue_images(prompt, image_url_list):
    '''
    Manages the image_url_queue by appending to it a complete interaction between the user and the API.
    Requires both parameters as input, the user message (prompt) and the image url list (image_url_list) to manange as a queue. 
    '''

    queue = deque(maxlen = 5)
    for url in image_url_list:
        queue.append(url)

    img_result = get_image_from_prompt(prompt)
    queue.append([item['url'] for item in img_result['data']])

    return list(queue)