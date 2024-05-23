


import logging

from cms.db import Question, Announcement, Message
from cms.db import Emotion
from cms.db.contest import Contest
from cms.db.task import Task
from cms.db.user import FormsEmotions, User
from cmscommon.datetime import make_timestamp


logger = logging.getLogger(__name__)


# Dummy function to mark translatable strings.
def N_(msgid):
    return msgid

def accept_emotion(sql_session, user_id, timestamp, task_id, contest_id, emotions, form_emotion_id):
    """Add a contestant-submitted question to the database.

    Validate and add a question received from a contestant (usually
    through CWS) to the database.

    sql_session (Session): the SQLAlchemy database session to use.
    participation (Participation): the participation of the user who
        posed the question.
    timestamp (datetime): when the question was asked.
    subject (str): the subject of the question.
    text (str): the body of the question.

    return (Question): the question that was added to the database.

    raise (QuestionsNotAllowed): if the contest doesn't allow
        contestants to ask questions.
    raise (UnacceptableQuestion): if some conditions necessary to
        accept the questions were not met.

    """
    task = sql_session.query(Task).filter(Task.id == task_id).first()
    contest = sql_session.query(Contest).filter(Contest.id == contest_id).first()
    form_emotion = sql_session.query(FormsEmotions).filter(FormsEmotions.id == form_emotion_id).first()
    user = sql_session.query(User).filter(User.id == user_id).first()

    # Create a instance of Emotion with the values 
    new_entry = Emotion(emotion_timestamp=timestamp,
                            task=task,
                            contest=contest,
                            emotions=emotions,
                            form_emotion=form_emotion,
                            user=user)
    sql_session.add(new_entry)

    return new_entry