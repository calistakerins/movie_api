from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db

router = APIRouter()

def get_convo_lines(conversation):
    all_lines = filter(lambda line: line.conv_id == conversation.id, db.lines.values())
    convo_lines = []

    for line in sorted(all_lines, key=lambda line: line.line_sort):
        convo_lines.append({
            "character": db.characters.get(line.c_id).name,
            "line_text": line.line_text
        })
    
    return convo_lines


@router.get("/conversations/{id}", tags=["conversations"])
def get_convo(id: int):
    """
    This endpoint returns a single conversation by its identifier. For each conversation
    it returns:
    * `convo_id`: the internal id of the conversation. Can be used to query the
      `/conversations/{conversation_id}` endpoint.
    * `movie`: The movie the character is from.
    * `character1`: The name of the first character.
    * `character2`: The name of the second character.
    * `conversation_lines`: A list of the lines in the conversation. The lines are listed according to the given 'line_sort'. These lines are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character`: The name of the character.
    * `line_text`: The line the character is speaking.
    """
    convo = db.conversations.get(id)

    if convo:
        movie = db.movies.get(convo.movie_id)
        result = {"convo_id": convo.id,
                 "movie": movie and movie.title, 
                 "character1": db.characters.get(convo.c1_id).name, 
                 "character2": db.characters.get(convo.c2_id).name, 
                 "conversation_lines": get_convo_lines(convo)
        }
        return result

    raise HTTPException(status_code=404, detail="conversation not found.")



@router.get("/conversations/", tags=["conversations"])
def list_convos(
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0)
):
    """
    This endpoint returns a list of conversations. For each conversation it returns:
    * `convo_id`: the internal id of the conversation. Can be used to query the
      `/conversations/{conversation_id}` endpoint.
    * `movie`: The movie the character is from.
    * `character1`: The name of the first character.
    * `character2`: The name of the second character.
    * `number_of_lines`: The number of lines in the conversation.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    items = list(db.conversations.values())
    json = (
        {
            "convo_id": c.id,
            "movie": db.movies[c.movie_id].title,
            "character1": db.characters[c.c1_id].name,
            "character2": db.characters[c.c2_id].name,
            "number_of_lines": c.num_lines
        }
        for c in items[offset : offset + limit]
    )
    return json


@router.get("/lines/{movie_id}", tags=["lines"])
def get_script(movie_id: int):
    """
    This endpoint returns a list of lines in a specified movie. For each line it returns:
    * `character`: The name of the character speaking the line.
    * `line_text`: The line the character is speaking.
    """
    all_lines = filter(lambda line: line.movie_id == movie_id, db.lines.values())
    lines = []

    for line in all_lines:
        lines.append({
            "character": db.characters.get(line.c_id).name,
            "line_text": line.line_text
        })

    return lines