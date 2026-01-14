# Constants for Question Generator LLM 

system_q_generator_message = """
You are a python quiz generator. Your task is to generate a python code quiz based on several parmeters:
- Difficulty: Easy, Medium, Hard
- Subject: e.g., Python, Data Science, Machine Learning, etc.
- quiz_type: e.g., multiple choice, true/false, open question, Spot the Bug, etc.


### Important
- Ensure all newlines and quotes inside the JSON values are properly escaped so the JSON is valid.
- Do not output markdown code blocks (like ```json). Return raw JSON only.
- Question should be short and concise, such that the answer to is not more than 2-3 sentences.

Note that the user was asked about these previous codes, so please don't repeat them:

"""


CORE_TOPICS = [
    "String Slicing & Indexing",
    "f-strings and Formatting",
    "List Comprehensions",
    "Dictionary Methods (.get, .items)",
    "Set Operations (union, intersection)",
    "Tuple Unpacking",
    "While Loops & Break/Continue",
    "For Loops with enumerate() and zip()",
    "Function *args and **kwargs",
    "Lambda Functions",
    "Type Conversion (int vs str vs float)",
    "Basic File I/O (open/read/write)",
    "The 'in' operator keyword",
    "Boolean Logic (and, or, not)",
    "Other Core Topics"
]

ADVANCED_TOPICS = [
    "Decorators (@wraps)",
    "Generators and the 'yield' keyword",
    "Context Managers ('with' statement)",
    "Class Inheritance & super()",
    "Dunder Methods (__init__, __str__, __len__)",
    "Mutable vs Immutable types (pass-by-reference)",
    "Default Mutable Arguments trap",
    "Global vs Local Scope",
    "Exception Handling (try/except/else/finally)",
    "The 'is' vs '==' operator",
    "Recursion",
    "Other Advanced Topics"
]

json_q_generator_schema = {
    "name": "python_quiz",
    "strict": True,  # Highly recommended for reliability
    "schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "A beautiful markdown text with the question regarding the subject (if code needed, include it as markdown code). If quiz_type is multiple choices, include here the choices with line breaks.",
            },
            "hint": {
                "type": "string",
                "description": "a hint to help the user if he struggles."
            },
            "answer": {
                "type": "string",
                "description": "The correct answer to the question."
            }
        },
        "required": [
            "question", 
            "hint", 
            "answer"],
        "additionalProperties": False  # REQUIRED when strict is True
    }
}

## Constants for Evaluator LLM

system_evaluator_message = """
You are a python quiz evaluator. Your task is to evaluate a the user's answer according to the true answer provided.
You are given the next parameters:
- question: The question asked to the user.
- true_answer: The correct answer to the question.
- user_answer: The user's answer to the question.

## important: if the answer seems like a choice in a multiple choices question, it is enough for the user to specify the number/letter of the choice.
Your response should be a json object containing exactly these keys:
{
    "verdict": "verdict keyword selected from: 'Correct', 'Wrong', 'Partial'"
    "explanation": "A short markdown text with the explanation regarding the user's answer. Use evaluating phrases such as 'Good job!', 'Almost there!', etc. elaborate only if not correct."
}

"""

json_evaluator_schema = {
    "name": "evaluator_json",
    "strict": True,  # Highly recommended for reliability
    "schema": {
        "type": "object",
        "properties": {
            "verdict": {
                "type": "string",
                "description": "verdict keyword selected from: 'Correct', 'Wrong', 'Partial'"
            },
            "explanation": {
                "type": "string",
                "description": "A markdown text with the explanation regarding the user's answer. Use evaluating phrases such as 'Good job!', 'Almost there!', etc."
            }
        },
        "required": ["verdict", "explanation"],
        "additionalProperties": False  # REQUIRED when strict is True
    }
}