
try:
    import tornado4.web as tornado_web
except ImportError:
    import tornado.web as tornado_web

from cms.db.user import FormsEmotions, Emotion
from cms.server import multi_contest


from cms.db import Contest, Submission, UserTest, Task
from cms.server.admin.handlers.contest import ContestHandler
import json

from .base import BaseHandler, SimpleHandler, require_permission


class AllEmotionsHandler(BaseHandler):
    

    @require_permission(BaseHandler.AUTHENTICATED)
    def get(self, contest_id):
        self.contest = self.safe_get_item(Contest, contest_id)

        self.r_params = self.render_params()
        self.r_params["contest"] = self.contest

        contest_id = self.contest.id

        data = self.sql_session.query(Emotion).filter(Emotion.contest_id == contest_id).all()
        for emotion in data:
            emotion.emotions = json.loads(emotion.emotions)
        
        self.render("all_emotions.html", all_emotions=data, **self.r_params)


class FormEmotionUserResponseHandler(BaseHandler):

    @require_permission(BaseHandler.PERMISSION_ALL)
    def post(self, contest_id, emotion_entry_id):
        data = self.get_argument("emotions_value").replace("'", '"')
        result_questions = json.loads(data)

        form_id = int(self.get_argument("form_emotion_id_value"))

        username = self.get_argument("username_value")

        task_name = self.get_argument("task_name_value")
        

        data = self.sql_session.query(FormsEmotions).filter(FormsEmotions.id == form_id).first()
        name = data.name
        questions_data = json.loads(data.questions)

        questions = questions_data["questions"]
        for i, clave in enumerate(result_questions):
            questions[i]["result"] = result_questions[clave] 
        self.r_params = self.render_params()
        
        self.render("emotion_context.html", questions=questions, username=username, task_name=task_name, name=name, **self.r_params)



class AddQuestionsEmotionsHandler(
        SimpleHandler("add_question_emotions.html", permission_all=True)):
    """Adds a new contest.

    """
    @require_permission(BaseHandler.PERMISSION_ALL)
    def post(self):    
        name = self.get_argument("name_questionnaire")
        if name == "":
            name = self.get_argument("name_questionnaire_create")

        
        result = self.get_argument("json_data")
        
        
        form_emotions = FormsEmotions()
        form_emotions.name = name
        form_emotions.questions = f'{result}'
        self.sql_session.add(form_emotions)
        self.sql_session.commit()
        
        self.redirect(self.url("contests"))

class FormEmotionHandler(BaseHandler):
    @require_permission(BaseHandler.AUTHENTICATED)
    def get(self, form_id):
        data = self.sql_session.query(FormsEmotions).filter(FormsEmotions.id == form_id).first()
        if data is not None:
            name = data.name
            questions_data = json.loads(data.questions)

            number_questions = questions_data["number_questions"]
            questions = questions_data["questions"]
            self.r_params = self.render_params()
            self.render("emotion.html", questions=questions, number_questions=number_questions, name=name, **self.r_params)
        else:
            self.redirect(self.contest_url("contests"))


class AllFormEmotionsHandler(SimpleHandler("emotions.html")):
    pass
        
