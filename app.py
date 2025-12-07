from flask import Flask, render_template, request, session, redirect, url_for
from db.crud import get_quizes, get_question_after, check_right_answer
from random import shuffle


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

def start_session(quiz_id=0):
    session["quiz_id"] = quiz_id
    session["last_question_id"] = 0
    session["correct_ans"] = 0
    session["wrong_ans"] = 0
    session["total"] = 0

def question_form(question):
    answers_list = [
        question[2],
        question[3],
        question[4],
        question[5],
    ]
    shuffle(answers_list)
    return render_template("test.html", question_id=question[0], quest=question[1], ans_list=answers_list)


def check_answer(question_id, selected_answer):
    if check_right_answer(question_id, selected_answer):
        session["correct_ans"] += 1
    else:
        session["wrong_ans"] +=1
    session["total"] += 1



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        quizes = get_quizes()
        start_session(-1)
        return render_template("index.html", quizes_list=quizes)
    else:
        quiz_id = request.form.get("quiz")
        start_session(quiz_id)
        return redirect(url_for("test"))

@app.route("/test", methods=["GET", "POST"])
def test():
    if not ("quiz_id" in session) or int(session["quiz_id"]) < 0:
        return redirect(url_for("index"))
    else:
        if request.method == "POST":
            selected_answer = request.form.get("ans")
            question_id = int(request.form.get("quest_id"))
            check_answer(question_id, selected_answer)
            session['last_question_id'] = question_id


        new_question = get_question_after(session["quiz_id"], session["last_question_id"])
        if new_question is None:
            return redirect(url_for("result"))
        else:
            return question_form(new_question)
    

@app.route("/result")
def result():
    return render_template("result.html",
                            right=session['correct_ans'],
                            wrong=session['wrong_ans'],
                            total=session['total'])
                            


if __name__ == '__main__':
    app.run()

