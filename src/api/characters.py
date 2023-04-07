from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
import json

router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: int):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """
    jsonObject = None

    for character in db.characters:
        if character["character_id"] == id:
            print("character found")

            #get movie name from db.movies using movie_id
            movie_name = next(movie for movie in db.movies if movie["movie_id"] == character["movie_id"])["title"]

            #get top conversations
            #filter conversations by character1_id => (gets all conversations w/ that character)
            all_conversations = [convo for convo in db.conversations if (convo['character1_id'] == character["character_id"] or convo['character2_id'] == character["character_id"])] 
            top_conversations = []

            #for each conversation w character:
            for convo in all_conversations:
                #get convo id
                #filter db.lines by convo_id and count num lines
                #if num lines > than some threshold, add current convo dict to top_conversations #top_conversations = []
                convo_lines = [line for line in db.lines if line['conversation_id'] == convo['conversation_id']]
                other_char = next(char for char in db.characters if char["character_id"] == convo["character2_id"])
                top_conversations.append({
                        "character_id": convo["character2_id"],
                        "character":other_char["name"],
                        "gender": other_char["gender"],
                        "number_of_lines_together": len(convo_lines)
                    })
                
            #sort top_conversations by `number_of_lines_together` (most to least)
            top_conversations = sorted(top_conversations, key=lambda c: c["number_of_lines_together"], reverse=True) 

            jsonObject = { "character_id": character["movie_id"],
                "character": character["name"],
                "movie":  movie_name,
                "gender":  character["gender"],
                "top_conversations": json.dumps(top_conversations)
            }

        
    if jsonObject is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return jsonObject



class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: character_sort_options = character_sort_options.character,
):
    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    json = None
    return json
