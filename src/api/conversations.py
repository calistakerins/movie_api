from fastapi import APIRouter, HTTPException
from src import database as db
from src.datatypes import Conversation, Line
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

    if(db.movies.get(movie_id) is None):
        raise HTTPException(status_code=422, detail="Movie not found.")
    if(conversation.character_1_id not in db.characters or conversation.character_2_id not in db.characters):
        raise HTTPException(status_code=422, detail="Character ID not found")
    if(conversation.character_1_id == conversation.character_2_id):
        raise HTTPException(status_code=422, detail="Character IDs must be different")
    for line in conversation.lines:
        if(line.character_id != conversation.character_1_id and line.character_id != conversation.character_2_id):
            raise HTTPException(status_code=422, detail="Line character ID does not match conversation character IDs")
    if(db.characters[conversation.character_1_id].movie_id != movie_id or db.characters[conversation.character_2_id].movie_id != movie_id):
        raise HTTPException(status_code=422, detail="Characters must be part of the referenced movie")

    # add conversation to db
    convo_id = len(db.convo_list)
    #db.conversations[convo_id] = Conversation(convo_id, movie_id, conversation.character_1_id, conversation.character_2_id, len(conversation.lines))
    db.convo_list.append({"conversation_id": convo_id, "movie_id": movie_id, "character1_id": conversation.character_1_id, "character2_id": conversation.character_2_id})
    # add lines to db
    line_num = 0
    for line in conversation.lines:
        line_id = len(db.lines)
        #db.lines[line_id] = Line(line_id, line.character_id, movie_id, convo_id, line_num, line.line_text)
        db.lines_list.append({"line_id": line_id, "character_id": line.character_id, "movie_id": movie_id, "conversation_id": convo_id, "line_sort": line_num, "line_text": line.line_text})
        line_num += 1
    
    print(conversation)
    db.logs.append({"post_call_time": datetime.now(), "movie_id_added_to": movie_id})
    db.upload_new_log()
    db.upload_new_conversation()
    db.upload_new_lines()
