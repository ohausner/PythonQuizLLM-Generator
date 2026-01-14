from quiz_class import quizzer
import gradio as gr

def create_app():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        # State Management: Initialize the class for every unique user session
        quiz_state = gr.State(quizzer())

        gr.Markdown("# 🧠 AI Quiz Generator")

        with gr.Row():
            with gr.Column(scale=1):
                # Inputs
                inp_subject = gr.Textbox(label="1. Topic/Subject", placeholder="e.g. Python Lists")
                inp_difficulty = gr.Dropdown(choices=["Easy", "Medium", "Hard"], value="Medium", label="2. Difficulty")
                inp_type = gr.Dropdown(choices=["Multiple Answers", "Open Question", "True/False", "Spot the Bug"], value="Open Question", label="3. Question Type")
                
                btn_generate = gr.Button("Generate Question", variant="primary")
                
                # Stats Display
                out_score = gr.Markdown("### Score: 0/0")
                btn_reset = gr.Button("Reset Quiz", variant="stop")

            with gr.Column(scale=2):
                # Question Area
                out_question = gr.Markdown("### Question will appear here...", min_height=190)
                
                # Hint Area
                with gr.Accordion("Need help?", open=False):
                    btn_hint = gr.Button("Get Hint", size="sm")
                    out_hint = gr.Markdown("")

                # Answer Area
                gr.Markdown("---")
                inp_answer = gr.Textbox(label="4. Your Answer", placeholder="Type here...", lines=3)
                btn_submit = gr.Button("Submit Answer")
                
                # Evaluation Area
                out_eval_verdict = gr.Markdown("")
                out_eval_explanation = gr.Markdown("")

        # --- EVENT FUNCTIONS ---
        
        def on_generate(quiz, subject, diff, q_type):
            # Logic wrapper
            q_text = quiz.new_question(subject, diff, q_type)
            print(quiz.history_questions)
            return (
                quiz,                           # Update State
                q_text,                         # Show Question
                "",                             # Clear Hint
                "",                             # Clear Answer box
                "",                             # Clear Verdict
                ""                              # Clear Explanation
            )

        def on_hint(quiz):
            return quiz.get_current_hint()

        def on_submit(quiz, answer):
            verdict, explanation = quiz.evaluate_user_answer(answer)
            score_text = f"### Score: {quiz.user_score}/{quiz.total_score} ({quiz.user_score/quiz.total_score*100}%)"
            
            # Formatting verdict color
            if verdict == "Correct":
                verdict_md = f"### ✅ {verdict}"
            elif verdict == "Answered":
                verdict_md = f"### ⚠️ {verdict}"
            else:
                verdict_md = f"### ❌ {verdict}"
            
            return quiz, verdict_md, explanation, score_text

        def on_reset(quiz):
            quiz.reset_quiz()
            return (
                quiz, 
                "### Score: 0/0", 
                "### Question will appear here...", 
                "", 
                "", 
                "", 
                ""
            )

        # --- WIRING BUTTONS ---
        
        btn_generate.click(
            on_generate, 
            inputs=[quiz_state, inp_subject, inp_difficulty, inp_type], 
            outputs=[quiz_state, out_question, out_hint, inp_answer, out_eval_verdict, out_eval_explanation]
        )

        btn_hint.click(
            on_hint,
            inputs=[quiz_state],
            outputs=[out_hint]
        )

        btn_submit.click(
            on_submit,
            inputs=[quiz_state, inp_answer],
            outputs=[quiz_state, out_eval_verdict, out_eval_explanation, out_score]
        )

        btn_reset.click(
            on_reset,
            inputs=[quiz_state],
            outputs=[quiz_state, out_score, out_question, out_hint, inp_answer, out_eval_verdict, out_eval_explanation]
        )

    return demo

if __name__ == "__main__":
    app = create_app()
    app.launch(debug=True)