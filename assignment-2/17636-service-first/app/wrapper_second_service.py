# IPC to communicate with the second service.

# Source: https://docs.python.org/3/library/multiprocessing.shared_memory.html


def get_grep_matched_lines_from_second_service(
    keyword: str, list_lines_romeo_and_juliet: list
) -> list | None:
    matched_lines = []
    #  list_lines_romeo_and_juliet, keyword
    if len(matched_lines) == 0:
        return None
    return matched_lines
