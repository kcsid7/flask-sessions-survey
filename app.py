from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import personality_quiz

answers_key = "survey_answers"

app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret_Survey"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def root_route():
    """Start the Survey"""
    return render_template("survey_root.html", survey = personality_quiz)


@app.route("/start", methods=["POST"])
def start_route():
    session[answers_key] = []
    return redirect("/questions/0")


@app.route("/questions/<int:ques_id>")
def questions_route(ques_id):
    """Show current question"""
    question = personality_quiz.questions[ques_id]
    responses = session.get(answers_key)

    if (ques_id != len(responses)):
        flash(f"Question {ques_id} not available")
        return redirect(f"/questions/{len(responses)}")

    if (len(personality_quiz.questions) == len(responses)):
        return redirect("/finished")

    return render_template("question.html", ques_id = ques_id, question = question)


@app.route("/answer", methods=["POST"])
def answer_route():
    """ Save the answer to the responses list and redirect to next question"""
    ans = request.form["answer"]

    responses = session[answers_key]
    responses.append(ans)
    session[answers_key] = responses

    if (len(personality_quiz.questions) == len(responses)):
        return redirect("/finished")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/finished")
def finished_survey():
    """ Survery Completion Message"""
    return render_template("finished.html")