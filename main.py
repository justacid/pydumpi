from dumpi.util import trace_files_from_dir
from dumpi.undumpi import DumpiTrace
from collections import defaultdict
import matplotlib.pyplot as plot
from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm
import numpy as np
import sys


class MessageTrace(DumpiTrace):

    def __init__(self, file_name):
        super(MessageTrace, self).__init__(file_name)
        self.last_time = {}
        self.idle_times = defaultdict(list)

    def on_send(self, data, thread, cpu_time, wall_time, perf_info):
        self._measure_idle(thread, wall_time)

    def on_recv(self, data, thread, cpu_time, wall_time, perf_info):
        self._measure_idle(thread, wall_time)

    def on_barrier(self, data, thread, cpu_time, wall_time, perf_info):
        self._measure_idle(thread, wall_time)

    def on_bcast(self, data, thread, cpu_time, wall_time, perf_info):
        self._measure_idle(thread, wall_time)

    def on_allreduce(self, data, thread, cpu_time, wall_time, perf_info):
        self._measure_idle(thread, wall_time)

    def on_wtime(self, data, thread, cpu_time, wall_time, perf_info):
        self._measure_idle(thread, wall_time)

    def _measure_idle(self, thread, time):
        last_time = self.last_time.get(thread, None)
        if last_time:
            time_diff = last_time - time.start
            self.idle_times[thread].append(time_diff.to_ms())
        self.last_time[thread] = time.stop


def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        https://stackoverflow.com/questions/11882393/matplotlib-disregard-outliers-when-plotting

        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


def analyze(args):
    process_id, paths = args
    idle_times = []
    for path in tqdm(paths, position=process_id):
        with MessageTrace(path) as trace:
            trace.read_stream()
            # collect all idle times from this trace
            for thread_id in trace.idle_times:
                idle_times.extend(trace.idle_times[thread_id])
    return idle_times


def chunks(iterable, size):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


if __name__ == "__main__":

    folder = sys.argv[1]
    if not Path(folder).is_dir():
        raise ValueError(f"{folder} is not a folder.")
    trace_files = trace_files_from_dir(folder)

    num_procs = int(sys.argv[2])
    num_procs = 1 if num_procs <= 0 else num_procs

    chunk_size = len(trace_files) // num_procs
    trace_chunks = list(chunks(trace_files, chunk_size))

    print(f"Running with {num_procs} processes...")

    with Pool(processes=num_procs) as pool:
        idle_times = []
        for result in pool.imap_unordered(analyze, enumerate(trace_chunks)):
            idle_times.extend(result)

    idle_times = np.array(idle_times)
    filtered = idle_times[~is_outlier(idle_times)]
    hist = plot.hist(filtered, bins=10)
    plot.show()

