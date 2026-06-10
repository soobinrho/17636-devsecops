import time
from multiprocessing.shared_memory import ShareableList

IPC_SHAREABLE_LIST_NAME_INPUT = "17636-service-second-input"
IPC_SHAREABLE_LIST_NAME_OUTPUT = "17636-service-second-output"
SECONDS_RETRY_INTERVAL = 1
RETRY_MAX = 10


def get_grep_matched_lines_from_second_service(
    keyword: str, list_lines_romeo_and_juliet: list
) -> list | None:
    # Use shared memory blocks to communicate between the first service
    # and the second service.
    # Source: https://docs.python.org/3/library/multiprocessing.shared_memory.html
    list_input = [keyword] + list_lines_romeo_and_juliet
    try:
        shared_list_input = ShareableList(
            list_input, name=IPC_SHAREABLE_LIST_NAME_INPUT
        )
        shared_list_input.shm.close()
    except FileExistsError:
        shared_list_input = ShareableList(name=IPC_SHAREABLE_LIST_NAME_INPUT)
        shared_list_input.shm.unlink()
        shared_list_input = ShareableList(
            list_input, name=IPC_SHAREABLE_LIST_NAME_INPUT
        )
        shared_list_input.shm.close()

    # Wait until the second service completes.
    shared_list_output = None
    retry_count = 0
    while shared_list_output is None and retry_count < RETRY_MAX:
        time.sleep(SECONDS_RETRY_INTERVAL)
        try:
            shared_list_output = ShareableList(name=IPC_SHAREABLE_LIST_NAME_OUTPUT)
        except FileNotFoundError:
            retry_count += 1

    list_matched_lines = None
    if shared_list_output is not None and 0 < len(shared_list_output):
        list_matched_lines = list(shared_list_output)
        shared_list_output.shm.unlink()
    else:
        print(
            f"[ERROR] len(shared_list_output) = 0 and RETRY_MAX = {RETRY_MAX:,} reached."
        )

    if list_matched_lines is None or len(list_matched_lines) == 0:
        return None
    return list_matched_lines
