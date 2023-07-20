import openai
from instructions import fixed_copy_prompt, fixed_image_prompt


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


def queue_copy(prompt, message_queue):
    '''
    Manages the message_queue by appending to it a complete interaction between the user and the API.
    Requires both parameters as input, the user message (prompt) and the message queue to manange (message_queue). 
    '''

    message_queue.append({'role': 'user', 'content': prompt})
    completion = get_chat_completion(message_queue)
    message_queue.append({'role': 'assistant', 'content': completion['choices'][0]['message']['content']})

    return message_queue


def queue_images(prompt, image_url_queue):
    '''
    Manages the image_url_queue by appending to it a complete interaction between the user and the API.
    Requires both parameters as input, the user message (prompt) and the image queue to manange (image_url_queue). 
    '''

    img_result = get_image_from_prompt(prompt)
    image_url_queue.append([item['url'] for item in img_result['data']])

    return image_url_queue