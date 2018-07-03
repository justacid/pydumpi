from dumpi.undumpi import DumpiTrace
from dumpi.constants import DataType
import matplotlib.pyplot as plt
from pathlib import Path
from os import listdir
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
    files = listdir(folder);
    # don't count the meta file
    file_count = len(files)-1;

    message_count = 0
    message_sizes = []

    for i, file_name in enumerate(files):
        binary_dump = Path(folder) / file_name

        # get number of processes from meta file for sanity check
        if file_name.rfind("meta") != -1:
            num_procs = None
            with open(binary_dump, "r") as meta_file:
                for line in meta_file:
                    if line.startswith("numprocs"):
                        num_procs = int(line.split("=")[1])
            assert num_procs == file_count
            continue

        # analyze binary dumps
        with MessageTrace(binary_dump) as trace:
            trace.print_header()
            trace.print_footer()
            trace.print_sizes()

            trace.read_stream()
            message_count += trace.message_count
            message_sizes.extend(trace.message_sizes)

            print(f"{trace.message_count} messages parsed.")
            print(f"Done with file '{file_name}'...\n")


    print(f"Total messages sent: {message_count}")
    # convert sizes to kbyte
    message_sizes = [s / 1024 for s in message_sizes]
    plt.hist(message_sizes, bins="auto")
    plt.title("Message Sizes")
    plt.xlabel("message sizes in kbytes")
    plt.ylabel("count")
    plt.show()
