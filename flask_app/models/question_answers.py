from flask_app.config.mysqlconnection import connectToMySQL

class QuestionAnswer:
    DB = 'flash_card'
    def __init__(self, data):
        self.id = data.get('id')
        self.flashcard_id = data.get('flashcard_id')
        self.question = data.get('question')
        self.answer = data.get('answer')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    