# DUMPI Python Bindings

Python bindings for the SST-DUMPI Trace Library.

## Prerequisites

The dumpi library must be installed first - simply
clone the repo https://github.com/sstsimulator/sst-dumpi and run

```bash
./bootstrap.sh
./configure --prefix=/usr
sudo make && sudo make install
```

You can of course install the library wherever you want,
but it must be available on the path somewhere.


## Usage Example

Inherit from DumpiTrace and override the callbacks you are interested in.
All available callbacks are listed in *callbacks.py*.

```python
from dumpi.undumpi import DumpiTrace


class MessageTrace(DumpiTrace):

    def __init__(self, file_name):
        super(MessageTrace, self).__init__(file_name)
        self.message_count = 0

    def on_isend(self, data, thread, cpu_time, wall_time, perf_info):
        self.message_count += 1


file_path = "trace.bin" # path to a binary dumpi trace file

with MessageTrace(file_path) as trace:
    trace.print_header()
    trace.read_stream()
    print(trace.message_count)
```
