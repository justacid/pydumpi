# SST-DUMPI Python Bindings
Python bindings for the SST-DUMPI Trace Library.

## Prerequisites
The libundumpi library must be installed and on the path - clone 
the repository from https://github.com/sstsimulator/sst-dumpi and run:

```bash
./bootstrap.sh
./configure --prefix=/usr
sudo make && make install
```

libundumpi can of course be installed wherever desired, but you
must make sure that it can be found somwhere on the path.

## Installation
Clone this repository and install the package with pip, e.g:

```bash
git clone http://github.com/justacid/pydumpi
cd myproject
source myvenv/bin/activate
pip install ../pydumpi
```

## Usage Example
Inherit from DumpiTrace and override the callbacks you are interested in.
Every MPI function has an available callback. A complete list can be found 
in *dumpi/callbacks.py*.

```python
from dumpi.undumpi import DumpiTrace


class MyTrace(DumpiTrace):

    def __init__(self, file_name):
        super(MyTrace, self).__init__(file_name)
        self.message_count = 0

    def on_send(self, data, thread, cpu_time, wall_time, perf_info):
        self.message_count += 1
        time_diff = wall_time.stop - wall_time.start
        print(f"Time elapsed in 'MPI_Send': {time_diff.to_ms()} milliseconds.")

    def on_recv(self, data, thread, cpu_time, wall_time, perf_info):
        print(f"Message received on thread '{thread}' from thread '{data.source}'.")


with MessageTrace("path/to/some/trace.bin") as trace:
    trace.print_header()
    trace.read_stream()
    print(trace.message_count)
```

You can inspect the meta data of a dumpi trace by printing the header and
footer. In particular the footer prints a list of all MPI functions that 
were called during a trace - this information can help guide you in deciding
which callbacks need to be overriden for further analysis.

```python
with DumpiTrace("path/to/some/trace.bin") as trace:
    trace.print_header()
    trace.print_footer()
```
