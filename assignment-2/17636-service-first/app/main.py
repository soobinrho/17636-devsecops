from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

from .wrapper_second_service import (
    get_grep_matched_lines_from_second_service,
)

PATH_ROMEO_AND_JULIET = "./pg1513.txt"

# In FastAPI, the optimal way to load the Romeo and Juliet text is to initialize
# it as a part of FastAPI lifespan.
# Reference: https://fastapi.tiangolo.com/advanced/events/#lifespan
list_lines_romeo_and_juliet = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    path_romeo_and_juliet = Path(PATH_ROMEO_AND_JULIET)
    if not path_romeo_and_juliet.is_file():
        raise Exception(f"[ERROR] {PATH_ROMEO_AND_JULIET} not found.")
    with open(PATH_ROMEO_AND_JULIET, "r", encoding="UTF-8") as f:
        for line in f:
            list_lines_romeo_and_juliet.append(line.rstrip())
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Grep service for Romeo and Juliet",
    description="17636 Assignment 2",
)


def is_valid_search_keyword(keyword: str) -> bool:
    keyword = str(keyword)
    if len(keyword) == 0:
        return False
    return True


@app.get(
    "/romeo-and-juliet/{keyword}",
    status_code=status.HTTP_200_OK,
)
def get_grep_matched_lines(keyword: str):
    if not is_valid_search_keyword(keyword):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid search keyword."},
        )
    matched_lines = get_grep_matched_lines_from_second_service(
        keyword, list_lines_romeo_and_juliet
    )
    if matched_lines is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return matched_lines
