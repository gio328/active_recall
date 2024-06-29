from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.question_answers import QuestionAnswer
from flask import flash, session

class Flashcard:
    DB = 'flash_card'
    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.QA = None

    @classmethod
    def get_all(cls, id):
        query = """
            SELECT * FROM flashcards
            JOIN question_answers
            ON flashcards.id = question_answers.flashcard_id
            WHERE user_id = %(id)s;
        """
        data = connectToMySQL(cls.DB).query_db(query, {'id': id})
        
        flashcard_group = []
        # arrange data into flashcard groups
        if data:
            flashcard = [data[0]]

            for item in data[1:]:
                if flashcard[-1]['id'] == item['id']:
                    flashcard.append(item)
                else:
                    flashcard_group.append(flashcard)
                    flashcard = [item]

            # Append the last flashcard group
            flashcard_group.append(flashcard)


        flashcard_instances = []

        for flashcard in flashcard_group:
            flashcard_instance = Flashcard.organize_card_info(flashcard)
            flashcard_instances.append(flashcard_instance)

        return flashcard_instances

    @staticmethod
    def organize_card_info(flashcard):
        question_answers = []
        flashcard_instances = []
        flashcard_instance = None
        isExecuted = False

        for card in flashcard:

            if not isExecuted:
                card_info = {
                    'id': card.get('id'),
                    'user_id': card.get('user_id'),
                    'title': card.get('title'),
                    'description': card.get('description'),
                    'created_at': card.get('created_at'),
                    'updated_at': card.get('updated_at'),
                }
                flashcard_instance = Flashcard(card_info)
                isExecuted = True

            qa_data = { # retrieve question and answer info
                'id': card.get('question_answers.id'),
                'flashcard_id': card.get('flashcard_id'),
                'question': card.get('question'),
                'answer': card.get('answer'),
                'created_at': card.get('question_answers.created_at'),
                'updated_at': card.get('question_answers.updated_at'),
            }
            # print('qa_data:', qa_data)
            # question_answers.append(QuestionAnswer(qa_data))
            question_answers.append(qa_data) # put in list for now

        flashcard_instance.QA = question_answers
        
        return flashcard_instance

    @classmethod
    def get_one(cls, id):
        query = """
            SELECT * FROM flashcards
            JOIN question_answers
            ON flashcards.id = question_answers.flashcard_id
            WHERE flashcard_id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, {'id': id})
        return Flashcard.organize_card_info(result)
        # return cls(result[0])

    @classmethod
    def save(cls, form_data, question_answer_pair):

        query = """
            INSERT INTO flashcards (user_id, title, description)
            VALUES (%(user_id)s, %(title)s, %(description)s );
        """
        data = {
            'user_id': form_data.get('user_id'),
            'title': form_data.get('title'),
            'description': form_data.get('description'),
        }

        flashcard_id = connectToMySQL(cls.DB).query_db(query, data)

        data_list = []
        for item in question_answer_pair:
            data_list.append({'flashcard_id': flashcard_id, 'question': item[0], 'answer': item[1]})

        print('data_list:', data_list)
        # Construct the query dynamically
        query_parts = []
        data = []
        for i, entry in enumerate(data_list):
            query_parts.append(f"(%(flashcard_id_{i})s, %(question_{i})s, %(answer_{i})s)")
            data.append({f'flashcard_id_{i}': entry['flashcard_id'], f'question_{i}': entry['question'], f'answer_{i}': entry['answer']})

        # Combine all parts into a single query
        query2 = f"""
            INSERT INTO question_answers (flashcard_id, question, answer)
            VALUES {', '.join(query_parts)}
        """

        # Merge all dictionaries into one for the query
        query_data = {k: v for d in data for k, v in d.items()}

        question_answer_id = connectToMySQL(cls.DB).query_db(query2, query_data)

        return question_answer_id
        
    @classmethod
    def update(cls,  form_data, question_answer_pair):
        # Update the flashcard
        update_flashcard_query = """
            UPDATE flashcards
            SET title = %(title)s, description = %(description)s
            WHERE user_id = %(user_id)s AND id = %(flashcard_id)s;
        """
        flashcard_data = {
            'flashcard_id': form_data.get('flashcard_id'),
            'user_id': form_data.get('user_id'),
            'title': form_data.get('title'),
            'description': form_data.get('description'),
        }

        connectToMySQL(cls.DB).query_db(update_flashcard_query, flashcard_data)

        # Update question and answer pairs
        update_question_answer_query_parts = []
        data = []
        for i, entry in enumerate(question_answer_pair):
            update_question_answer_query_parts.append(f"""
                UPDATE question_answers
                SET question = %(question_{i})s, answer = %(answer_{i})s
                WHERE flashcard_id = %(flashcard_id_{i})s AND id = %(question_answer_id_{i})s
            """)
            data.append({
                f'flashcard_id_{i}': form_data.get('flashcard_id'),
                f'question_{i}': entry[0],
                f'answer_{i}': entry[1],
                f'question_answer_id_{i}': entry[2],  # Assuming the third element in entry is the question_answer_id
            })

        # Execute each update query
        for query_part, query_data in zip(update_question_answer_query_parts, data):
            connectToMySQL(cls.DB).query_db(query_part, query_data)

        return True  # Or any other return value if needed


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM flashcards WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, {'id': id})
    
    @staticmethod
    def validate(data):
        print('validating form data => ', data)
        is_valid = True

        if data['title'] == "":
            flash("title is required")
            is_valid = False
        if len(data['title']) < 3:
            flash('Title must be at least 3 characters')
            is_valid = False
        if data['question'] == "":
            flash("qustion cant be empty")
            is_valid = False
        if len(data['question']) < 3:
            flash('question must be at least 3 characters')
            is_valid = False
        if data['answer'] == "":
            flash("answer cant be empty")
            is_valid = False
        if len(data['answer']) < 3:
            flash('answer must be at least 3 characters')
            is_valid = False
        return is_valid