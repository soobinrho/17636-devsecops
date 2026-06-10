import signal
import time
from multiprocessing.shared_memory import ShareableList

IPC_SHAREABLE_LIST_NAME_INPUT = "17636-service-second-input"
IPC_SHAREABLE_LIST_NAME_OUTPUT = "17636-service-second-output"
SECONDS_LISTEN_INTERVAL = 0.3


# Handle SIGTERM. Without this, the container cannot exit gracefully.
# Source: https://stackoverflow.com/a/31464349
class class_sig_term_handler:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def main():
    print("[INFO] Starting to listen for 17636-service-first")

    cache_keyword = None
    cache_list_lines_romeo_and_juliet = None
    sig_term_handler = class_sig_term_handler()
    while not sig_term_handler.kill_now:
        shared_list_input = None
        try:
            # Wait until the first service sends the parameters.
            # Example: [keyword, list_lines_romeo_and_juliet]
            shared_list_input = ShareableList(name=IPC_SHAREABLE_LIST_NAME_INPUT)
        except FileNotFoundError:
            time.sleep(SECONDS_LISTEN_INTERVAL)
            continue
        keyword = None
        list_lines_romeo_and_juliet = None
        if 1 < len(shared_list_input):
            keyword = shared_list_input[0]
            list_lines_romeo_and_juliet = []
            for i in range(1, len(shared_list_input)):
                try:
                    list_lines_romeo_and_juliet.append(shared_list_input[i])
                except Exception:
                    # Required for fixing `UnicodeDecodeError: unexpected end of data`.
                    continue
        elif len(shared_list_input) == 1:
            print(
                f"[ERROR] 1 < len(shared_list_input) expected but got {shared_list_input}"
            )

        if keyword is not None and list_lines_romeo_and_juliet is not None:
            # If the cached values and the current values are the same, that means
            # that the output values don't have to be recalculated.
            if (
                keyword == cache_keyword
                and list_lines_romeo_and_juliet == cache_list_lines_romeo_and_juliet
            ):
                continue
            cache_keyword = keyword
            cache_list_lines_romeo_and_juliet = list_lines_romeo_and_juliet

            # Perform grep.
            keyword = str(keyword).lower()
            list_matched_lines = []
            print(f"[INFO] Searching for keyword = {keyword}")
            for line in list_lines_romeo_and_juliet:
                line = str(line).lower()
                if keyword in line:
                    list_matched_lines.append(line)
            if 0 < len(list_matched_lines):
                shared_list_output = ShareableList(
                    list_matched_lines, name=IPC_SHAREABLE_LIST_NAME_OUTPUT
                )
                shared_list_output.shm.close()
                print(f"[INFO] Found {len(list_matched_lines):,} matches.")

        time.sleep(SECONDS_LISTEN_INTERVAL)


if __name__ == "__main__":
    main()
