import openai

def get_chat_completion(ad_text_gen, message_queue):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= ad_text_gen + list(message_queue),
        max_tokens=200,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
    )

    return completion
