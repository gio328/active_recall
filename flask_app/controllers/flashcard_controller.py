from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.utils.helpers import login_required
from functools import wraps
from flask_app.models.flashcard import Flashcard

@app.route('/main_page')
def main_page():
    result = Flashcard.get_all(session['loggedin.id'])
    for item in result:
        # print(item.QA)
        store_qa_session(item.QA)

    return render_template('main_page.html', flashcards=result)

@app.route('/flashcard/<int:flashcard_id>')
def flashcard(flashcard_id):
    # print('session: ',session[str(flashcard_id)])
    data = session[str(flashcard_id)]
    return render_template('flashcard.html', data=data, flashcard_id=flashcard_id)

@app.route('/flashcard/new')
def new_flashcard():
    return render_template('new_flashcard.html')

@app.route('/flashcard/new', methods=['POST'])
def create_flashcard():
    if not Flashcard.validate(request.form.to_dict()):
        return redirect('/flashcard/new')

    form_data = request.form.to_dict()
    questions = request.form.getlist('question')
    answer = request.form.getlist('answer')
    question_answer_pair = list(zip(questions, answer))
    # print(question_answer_pair)
    result = Flashcard.save(form_data, question_answer_pair)
    # print('result:', result)
    return redirect(url_for('main_page'))

@app.route('/flashcard/edit/<int:flashcard_id>')
def edit_flashcard(flashcard_id):
    result = Flashcard.get_one(flashcard_id)
    return render_template('edit_flashcard.html', flashcard=result)

@app.route('/flashcard/edit/<int:flashcard_id>', methods=['POST'])
def update_flashcard(flashcard_id):
    form_data = request.form.to_dict()
    # print('form_data:', form_data)
    question_answer_id = request.form.getlist('question_answer_id')
    # print('question_answer_id:', question_answer_id)
    questions = request.form.getlist('question')
    # print('questions:', questions)
    answer = request.form.getlist('answer')
    # print('answer:', answer)
    question_answer_pair = list(zip(questions, answer, question_answer_id))
    # print('question_answer_pair:', question_answer_pair)
    result = Flashcard.update(form_data, question_answer_pair)
    return redirect(url_for('main_page'))

@app.route('/flashcard/delete/<int:flashcard_id>')
def delete_flashcard(flashcard_id):
    print('flashcard_id:', flashcard_id)
    Flashcard.delete(flashcard_id)
    return redirect(url_for('main_page'))

@app.route('/flashcard/memory_result/<int:flashcard_id>')
def memory_result(flashcard_id):
    print('flashcard_id:', flashcard_id)
    return render_template('memory_result.html', flashcard_id=flashcard_id)

def store_qa_session(qa):
    flahshcard_id = None
    isExecuted = False
    qa_pairs = []
    
    for item in qa:
        if not isExecuted:
            flashcard_id = item.get('flashcard_id')
            isExecuted = True

        pairs = {
            'question': item.get('question'),
            'answer': item.get('answer')
        }

        qa_pairs.append(pairs)
    # print('qa_pairs:', qa_pairs)
    session[str(flashcard_id)] = qa_pairs
    # if str(flashcard_id) in session:
    #     session.pop(str(flashcard_id))
        
    # session[flahshcard_id] = qa_pairs
    # if 'flashcards' in session:
    #     session.pop('flashcards')
    # session['flashcards'] = result




# @app.route('/shows/new', methods=['POST'])
# @login_required
# def add_new_show():
#     form_data = request.form.to_dict()
#     if not Tvshow.validate(form_data):
#         return redirect('/shows/new')
#     if title_exist(form_data): #check if title already exists
#         return redirect('/shows/new')
#     Tvshow.save(form_data)
#     delete_session()
#     return redirect('/shows')

# @app.route('/shows/<int:id>')
# @login_required
# def details(id):
#     show_details = Tvshow.get_show_with_id(id)
#     messages = Message.get_messages(id)
#     return render_template('details.html', show=show_details, messages=messages)

# @app.route('/shows/<int:id>', methods=['POST'])
# @login_required
# def post_message(id):
#     form_data = request.form.to_dict()
#     Message.post_message(form_data)
#     return redirect('/shows/'+str(id))

# @app.route('/delete_comment/<int:msg_id>/<int:user_id>/<int:id>/')
# @login_required
# def delete_comment(msg_id, user_id, id):
#     if session['loggedin.id'] != user_id:
#         return redirect('/shows')
#     Message.delete_comment(msg_id)
#     return redirect('/shows/'+str(id))

# @app.route('/shows/edit/<int:id>')
# @login_required
# def edit_show(id):
#     show_details = Tvshow.get_show_with_id(id)
#     return render_template('edit.html', show=show_details)

# @app.route('/update_show', methods=['POST'])
# @login_required
# def update_show():
#     form_data = request.form.to_dict()
#     if not Tvshow.validate(form_data):
#         return redirect('/shows/edit/'+form_data['id'])
    
#     Tvshow.update_show(form_data)
#     delete_session()
#     return redirect('/shows')

# @app.route('/shows/delete/<int:id>')
# @login_required
# def delete_show(id):
#     Tvshow.delete_show(id)
#     return redirect('/shows')

# def title_exist(form_data):
#     result = Tvshow.get_show_by_title(form_data)
#     if not result:
#         return False
#     if 'title' in result:
#         flash('Title already exists')
#         return True

# def delete_session():
#     if 'title' in session:
#         session.pop('title')
#     if 'network' in session:
#         session.pop('network')
#     if 'release_date' in session:
#         session.pop('release_date')
#     if 'comments' in session:
#         session.pop('comments')
    

