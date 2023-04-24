from fastapi import APIRouter
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.
    """

    # TODO: Remove the following two lines. This is just a placeholder to show
    # how you could implement persistent storage.

    # validate Json data w existing data in db
        # check if movie_id exists
        # check if character_1_id exists and has same movie_id
        # check if character_2_id exists and has same movie_id
        # check if character_1_id != character_2_id
        # check if each line has either character_1_id or character_2_id

    # add conversation to db
    # add lines to db
    # return conversation_id

    print(conversation)
    db.logs.append({"post_call_time": datetime.now(), "movie_id_added_to": movie_id})
    db.upload_new_log()
