#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2010-2014 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2015 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2012 Matteo Boscariol <boscarim@hotmail.com>
# Copyright © 2012-2014 Luca Wehrstedt <luca.wehrstedt@gmail.com>
# Copyright © 2013 Bernard Blackham <bernard@largestprime.net>
# Copyright © 2014 Artem Iglikov <artem.iglikov@gmail.com>
# Copyright © 2014 Fabian Gundlach <320pointsguy@gmail.com>
# Copyright © 2015-2016 William Di Luigi <williamdiluigi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Communication-related handlers for CWS.

"""


try:
    import tornado4.web as tornado_web
except ImportError:
    import tornado.web as tornado_web
import logging
from cms.db.user import FormsEmotions
from cms.server.contest.emotion import accept_emotion
from cms.server import multi_contest
from .contest import ContestHandler

from ..phase_management import actual_phase_required


import json




# Dummy function to mark translatable strings.
def N_(msgid):
    return msgid

logger = logging.getLogger(__name__)

# def accept_emotion(sql_session, participation, timestamp, task, emotions):
#     """Add a contestant-submitted question to the database.

#     Validate and add a question received from a contestant (usually
#     through CWS) to the database.

#     sql_session (Session): the SQLAlchemy database session to use.
#     participation (Participation): the participation of the user who
#         posed the question.
#     timestamp (datetime): when the question was asked.
#     subject (str): the subject of the question.
#     text (str): the body of the question.

#     return (Question): the question that was added to the database.

#     raise (QuestionsNotAllowed): if the contest doesn't allow
#         contestants to ask questions.
#     raise (UnacceptableQuestion): if some conditions necessary to
#         accept the questions were not met.

#     """
#     # if not participation.contest.allow_questions:
#     #     raise QuestionsNotAllowed()

#     # subject_length = len(subject)
#     # text_length = len(text)
#     # if subject_length > Question.MAX_SUBJECT_LENGTH \
#     #         or text_length > Question.MAX_TEXT_LENGTH:
#     #     logger.warning("Long question (%d, %d) dropped for user %s.",
#     #                    subject_length, text_length,
#     #                    participation.user.username)
#     #     raise UnacceptableQuestion(
#     #         N_("Question too long!"),
#     #         N_("Subject must be at most %(max_subject_length)d characters, "
#     #            "content at most %(max_text_length)d."),
#     #         {"max_subject_length": Question.MAX_SUBJECT_LENGTH,
#     #          "max_text_length": Question.MAX_TEXT_LENGTH})

#     emotion = Emotion(emotion_timestamp=timestamp, task=task, emotions=emotions, participation_id=participation)
#     sql_session.add(emotion)

#     # logger.info("Emotion submitted by user %s.", participation.user.username)

#     return emotion


class EmotionHandler(ContestHandler):
    """


    """
    @tornado_web.authenticated
    @actual_phase_required(0, 3)
    @multi_contest
    def get(self, task_name):
        task = self.get_task(task_name)
        data = self.sql_session.query(FormsEmotions).filter(FormsEmotions.id == task.form_emotion).first()
        if data is not None:
            name = data.name
            questions_data = json.loads(data.questions)

            number_questions = questions_data["number_questions"]
            questions = questions_data["questions"]
            
            self.render("emotion.html", task=task, questions=questions, number_questions=number_questions, name=name, **self.r_params)
        else:
            self.redirect(self.contest_url("tasks", task_name, "submissions"))

            
        
    @tornado_web.authenticated
    @actual_phase_required(0, 3)
    @multi_contest
    def post(self, task_name):
        task = self.get_task(task_name)
        number_questions = int(self.get_argument("number_questions"))
        emotions = dict()
        for i in range(1, number_questions+1):
            emotions[f"question_{i}"] = self.get_argument(f"question_{i}", default=None)
        if task is None:
            raise tornado_web.HTTPError(404)
        
        participation_id = self.current_user.id 
        emotions_str = str(emotions).replace("\'", "\"")

        try:
            accept_emotion(sql_session=self.sql_session, 
                           user_id=self.current_user.id, 
                           timestamp=self.timestamp,
                            task_id=task.id,
                            contest_id=self.contest.id,
                            emotions=emotions_str,
                            form_emotion_id=task.form_emotion)
            self.sql_session.commit()
        except Exception as e:
            self.notify_error("Upss Error","Error",f"{e}")
        else:
            self.notify_success(N_("Emociones recibidas"),
                                N_("Tus emociones han sido registradas"
                                   "muchas gracias, puedes continuar."))


        self.redirect(self.contest_url("tasks", task.name, "submissions"))