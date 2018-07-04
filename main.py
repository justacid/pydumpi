from dumpi.util import trace_files_from_dir
from dumpi.undumpi import DumpiTrace
import matplotlib.pyplot as plt
from pathlib import Path
import sys


class MessageTrace(DumpiTrace):

    def __init__(self, file_name):
        super(MessageTrace, self).__init__(file_name)
        self.message_count = 0
        self.message_sizes = []

    def on_isend(self, data, thread, cpu_time, wall_time, perf_info):
        self.message_count += 1
        size_of_type = self.type_sizes[data.datatype]
        self.message_sizes.append(data.count * size_of_type)

    
if __name__ == "__main__":

    folder = sys.argv[1]
    if not Path(folder).is_dir():
        raise ValueError(f"{folder} is not a folder.")

    message_count = 0
    message_sizes = []

    for i, path in enumerate(trace_files_from_dir(folder)):
        with MessageTrace(path) as trace:
            if i == 0:
                trace.print_header()
                trace.print_sizes()

            trace.print_footer()
            trace.read_stream()
            message_count += trace.message_count
            message_sizes.extend(trace.message_sizes)

            print(f"{trace.message_count} messages parsed.")
            print(f"Done with file '{path}'...\n")

    print(f"Total messages sent: {message_count}")
    # convert sizes to kbyte
    message_sizes = [s / 1024 for s in message_sizes]
    plt.hist(message_sizes, bins="auto")
    plt.title("Message Sizes")
    plt.xlabel("message sizes in kbytes")
    plt.ylabel("count")
    plt.show()
