# 🧠 Python Quizzer - using an LLM to generate questions & evaluate answers

A dynamic, AI-powered quiz application that generates infinite questions on any subject. Built with **Python**, **Gradio**, and **OpenAI**, this tool creates questions, provides hints, and evaluates user answers in real-time.

## 🚀 Features

* **Infinite Question Generation:** Generates unique python question based on:
    * **Topic:** Free text input (e.g., "Python Lists", "Recursive Functions", "Strings & Integers").
    * **Difficulty:** Easy, Medium, Hard.
    * **Type:** Multiple Choice or Open Question.
* **Smart Evaluation:** The AI evaluates user answers semantically, accepting partial matches and providing explanations.
* **Hint System:** Provides context-aware hints without revealing the answer.
* **State Management:** Tracks user score and history within the session.
* **Structured Outputs:** Uses OpenAI's JSON Schema to ensure reliable data formatting.

## 🛠️ Tech Stack

* **Python 3.10+**
* **Gradio:** For the web interface and state management.
* **OpenAI API:** For generating content and logic.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ohausner/PythonQuizLLM-Generato.git](https://github.com/ohausner/PythonQuizLLM-Generato.git)
    cd ai-quiz-generator
    ```

2.  **Install dependencies:**
    ```bash
    pip install openai gradio
    ```

3.  **Set up your API Key:**
    Create a `.env` file or export your key in the terminal:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```

## 🖥️ Usage

Run the application locally:

```bash
python app.py
```
