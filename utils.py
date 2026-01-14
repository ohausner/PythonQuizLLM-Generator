import os
import glob
from dotenv import load_dotenv
from pathlib import Path
import gradio as gr
from openai import OpenAI
from IPython.display import display, Markdown
import json
import random

from const import *

# ---------------------------------
#      Set up OpenAI API Key
# ---------------------------------

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# MODEL_q_generator = "gpt-5-nano-2025-08-07"
MODEL_q_generator = "o4-mini-2025-04-16"
MODEL_evaluator = "o4-mini-2025-04-16"

openai_client = OpenAI()

# ---------------------------------
#             Functions
# ---------------------------------

def system_generator_message(history=None, system_prefix=system_q_generator_message):
    """
    Generates a system message based on the provided history.
    
    Parameters:
    history (list): A list of previous messages.
    system_prefix (str): The prefix for the system message.
    
    Returns:
    str: The generated system message.
    """
    if not history:
        history = []
    system_message = system_prefix + "\n".join(history)

    return system_message 

def get_topics(level):
    """
    Returns a list of topics based on the provided level.
    
    Parameters:
    level (str): The difficulty level of the question.
    
    Returns:
    list: A list of topics.
    """
    if level == "Easy":
        return CORE_TOPICS
    elif level == "Medium":
        return CORE_TOPICS
    elif level == "Hard":
        return ADVANCED_TOPICS + CORE_TOPICS
    else:
        return CORE_TOPICS
    

def user_input(subject=None, difficulty=None, quiz_type=None):
    """
    Generates a prompt for a question based on the provided subject, difficulty, and quiz type.
    
    Parameters:
    subject (str): The subject of the question.
    difficulty (str): The difficulty level of the question.
    quiz_type (str): The type of quiz (e.g., multiple choice, true/false, open question).
    
    Returns:
    str: The prompt for the question.
    """
    for param in [subject, difficulty, quiz_type]:
        if not param:
            param = f"no specific {param} was given."
            
    return f"""
    Please, generate a unique python code question based on the following parameters:
    - Subject: {subject}
    - Difficulty: {difficulty}
    - quiz type: {quiz_type}

    The question should not be too long, such that an answer to is not more than 2-3 sentences.
    Be creative and unique, don't repeat codes and think about this random seed to encourage you to be creative: {random.random()}

    You can use this bank of topics as a reference to choose the code to be tested (be sure to follow the requested subject):
    {random.choices(get_topics(difficulty), k=4)}
    """

def generate_question(subject=None, difficulty=None, quiz_type=None, history=None):
    """
    Generates a question for a given subject, difficulty, and quiz type.
    
    Parameters:
    subject (str): The subject of the question.
    difficulty (str): The difficulty level of the question.
    quiz_type (str): The type of quiz (e.g., multiple choice, true/false, open question).
    
    Returns:
    dict: A dictionary containing the question, hint, and answer.
    """
        
    user_prompt = user_input(subject, difficulty, quiz_type)
    
    try:
        messages = [
            {"role": "system", "content": system_generator_message(history)},
            {"role": "user", "content": user_prompt}
        ]
        
        response = openai_client.chat.completions.create(
            model=MODEL_q_generator,
            messages=messages,
            response_format={"type": "json_schema", "json_schema": json_q_generator_schema},
            # presence_penalty=0.6
        )
        
        # Parse the JSON string into a Python Dictionary
        result_content = response.choices[0].message.content
        quest_dict = json.loads(result_content)

        quest_dict['question'] = quest_dict['question'].replace('\\n', '\n')
        # quest_dict['code'] = quest_dict['code'].replace('\\n', '\n')
        return quest_dict
        
    except Exception as e:
        return f"Error: {str(e)}", ""
    

def evaluate(question, true_answer, user_answer):
    """
    Evaluates a user's answer to a question based on the true answer.
    
    Parameters:
    question (str): The question asked to the user.
    true_answer (str): The correct answer to the question.
    user_answer (str): The user's answer to the question.
    
    Returns:
    dict: A dictionary containing the evaluation verdict and explanation.
    """

    user_prompt = f""" Please evaluate my answer to the following question:
    - question: {question}
    - true_answer: {true_answer}
    - user_answer: {user_answer}
    """

    try:
        messages = [
            {"role": "system", "content": system_evaluator_message},
            {"role": "user", "content": user_prompt}
        ]
        
        response = openai_client.chat.completions.create(
            model=MODEL_evaluator,
            messages=messages,
            response_format={"type": "json_schema", "json_schema": json_evaluator_schema}
        )
        
        # Parse the JSON string into a Python Dictionary
        result_content = response.choices[0].message.content
        parsed_data = json.loads(result_content)
        
        return parsed_data
        
    except Exception as e:
        return f"Error: {str(e)}", ""
    



