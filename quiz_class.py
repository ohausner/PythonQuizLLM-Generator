from utils import *

class quizzer:
    def __init__(self):
        self.history_questions = []
        self.user_score = 0
        self.total_score = 0
        self.current_hint = None
        self.current_question = None
        self.current_answer = None
        self.last_subject = None
        self.last_difficulty = None
        self.last_quiz_type = None

        self.already_answered = False

    def reset_quiz(self):
        self.history_questions = []
        self.user_score = 0
        self.total_score = 0
        self.current_hint = None
        self.current_question = None
        self.current_answer = None
        self.last_subject = None
        self.last_difficulty = None
        self.last_quiz_type = None

        self.already_answered = False
    
    def new_question(self, subject=None, difficulty=None, quiz_type=None):
        self.already_answered = False
        output = generate_question(subject, difficulty, quiz_type, self.history_questions)
        self.current_question = output["question"].replace("\\n", "\n")
        self.history_questions.append(self.current_question)
        self.current_hint = output["hint"]
        self.current_answer = output["answer"]
        return self.current_question
    
    def evaluate_user_answer(self, user_answer):
        if self.already_answered:
            return "This question was already answered, please move to the next question.", ""
        self.already_answered = True
        evaluation = evaluate(self.current_question,self.current_answer, user_answer)
        verdict = evaluation["verdict"]
        explanation = evaluation["explanation"]
        self.total_score += 1

        if verdict == "Correct":
            self.user_score += 1
        elif verdict == "Partial":
            self.user_score += 0.5
        else:
            self.user_score += 0
        return verdict, explanation
    
    def get_current_hint(self):
        return self.current_hint