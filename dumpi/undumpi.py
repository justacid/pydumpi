from ctypes import cast, POINTER
from .callbacks import DumpiCallbacks, CALLBACK
from .constants import DataType
from .dtypes import *
import time


libundumpi = CDLL("libundumpi.so.8")
libc = CDLL("libc.so.6")
undumpi_open = libundumpi.undumpi_open
undumpi_open.argtypes = [c_char_p]
undumpi_open.restype = POINTER(DumpiProfile)
undumpi_close = libundumpi.undumpi_close
undumpi_close.argtypes = [POINTER(DumpiProfile)]
undumpi_close.restype = c_int
undumpi_read_header = libundumpi.undumpi_read_header
undumpi_read_header.argtypes = [POINTER(DumpiProfile)]
undumpi_read_header.restype = POINTER(DumpiHeader)
undumpi_read_footer = libundumpi.undumpi_read_footer
undumpi_read_footer.argtypes = [POINTER(DumpiProfile)]
undumpi_read_footer.restype = POINTER(DumpiFooter)
undumpi_read_datatype_sizes = libundumpi.dumpi_read_datatype_sizes
undumpi_read_datatype_sizes.argtypes = [POINTER(DumpiProfile), POINTER(DumpiSizeof)]
undumpi_read_datatype_sizes.restype = c_int
undumpi_read_stream = libundumpi.undumpi_read_stream
undumpi_read_stream.argtypes = [POINTER(DumpiProfile), POINTER(DumpiCallbacks), c_void_p]
undumpi_read_stream.restype = c_int
undumpi_clear_callbacks = libundumpi.libundumpi_clear_callbacks
undumpi_clear_callbacks.argtypes = [POINTER(DumpiCallbacks)]


class DumpiTrace:

    def __init__(self, file_name):
        self.file_name = file_name
        self._type_sizes = None
        self._profile = None

        self.cbacks = DumpiCallbacks()
        undumpi_clear_callbacks(byref(self.cbacks))

        if hasattr(self, "on_send"):
            self.cbacks.on_send = CALLBACK(self.__on_send)
        if hasattr(self, "on_recv"):
            self.cbacks.on_recv = CALLBACK(self.__on_recv)
        if hasattr(self, "on_get_count"):
            self.cbacks.on_get_count = CALLBACK(self.__on_get_count)
        if hasattr(self, "on_bsend"):
            self.cbacks.on_bsend = CALLBACK(self.__on_bsend)
        if hasattr(self, "on_ssend"):
            self.cbacks.on_ssend = CALLBACK(self.__on_ssend)
        if hasattr(self, "on_rsend"):
            self.cbacks.on_rsend = CALLBACK(self.__on_rsend)
        if hasattr(self, "on_buffer_attach"):
            self.cbacks.on_buffer_attach = CALLBACK(self.__on_buffer_attach)
        if hasattr(self, "on_buffer_detach"):
            self.cbacks.on_buffer_detach = CALLBACK(self.__on_buffer_detach)
        if hasattr(self, "on_isend"):
            self.cbacks.on_isend = CALLBACK(self.__on_isend)
        if hasattr(self, "on_ibsend"):
            self.cbacks.on_ibsend = CALLBACK(self.__on_ibsend)
        if hasattr(self, "on_issend"):
            self.cbacks.on_issend = CALLBACK(self.__on_issend)
        if hasattr(self, "on_irsend"):
            self.cbacks.on_irsend = CALLBACK(self.__on_irsend)
        if hasattr(self, "on_irecv"):
            self.cbacks.on_irecv = CALLBACK(self.__on_irecv)
        if hasattr(self, "on_wait"):
            self.cbacks.on_wait = CALLBACK(self.__on_wait)
        if hasattr(self, "on_test"):
            self.cbacks.on_test = CALLBACK(self.__on_test)
        if hasattr(self, "on_request_free"):
            self.cbacks.on_request_free = CALLBACK(self.__on_request_free)
        if hasattr(self, "on_waitany"):
            self.cbacks.on_waitany = CALLBACK(self.__on_waitany)
        if hasattr(self, "on_testany"):
            self.cbacks.on_testany = CALLBACK(self.__on_testany)
        if hasattr(self, "on_waitall"):
            self.cbacks.on_waitall = CALLBACK(self.__on_waitall)
        if hasattr(self, "on_testall"):
            self.cbacks.on_testall = CALLBACK(self.__on_testall)
        if hasattr(self, "on_waitsome"):
            self.cbacks.on_waitsome = CALLBACK(self.__on_waitsome)
        if hasattr(self, "on_testsome"):
            self.cbacks.on_testsome = CALLBACK(self.__on_testsome)
        if hasattr(self, "on_iprobe"):
            self.cbacks.on_iprobe = CALLBACK(self.__on_iprobe)
        if hasattr(self, "on_probe"):
            self.cbacks.on_probe = CALLBACK(self.__on_probe)
        if hasattr(self, "on_cancel"):
            self.cbacks.on_cancel = CALLBACK(self.__on_cancel)
        if hasattr(self, "on_test_cancelled"):
            self.cbacks.on_test_cancelled = CALLBACK(self.__on_test_cancelled)
        if hasattr(self, "on_send_init"):
            self.cbacks.on_send_init = CALLBACK(self.__on_send_init)
        if hasattr(self, "on_bsend_init"):
            self.cbacks.on_bsend_init = CALLBACK(self.__on_bsend_init)
        if hasattr(self, "on_ssend_init"):
            self.cbacks.on_ssend_init = CALLBACK(self.__on_ssend_init)
        if hasattr(self, "on_rsend_init"):
            self.cbacks.on_rsend_init = CALLBACK(self.__on_rsend_init)
        if hasattr(self, "on_recv_init"):
            self.cbacks.on_recv_init = CALLBACK(self.__on_recv_init)
        if hasattr(self, "on_start"):
            self.cbacks.on_start = CALLBACK(self.__on_start)
        if hasattr(self, "on_startall"):
            self.cbacks.on_startall = CALLBACK(self.__on_startall)
        if hasattr(self, "on_sendrecv"):
            self.cbacks.on_sendrecv = CALLBACK(self.__on_sendrecv)
        if hasattr(self, "on_sendrecv_replace"):
            self.cbacks.on_sendrecv_replace = CALLBACK(self.__on_sendrecv_replace)
        if hasattr(self, "on_type_contiguous"):
            self.cbacks.on_type_contiguous = CALLBACK(self.__on_type_contiguous)
        if hasattr(self, "on_type_vector"):
            self.cbacks.on_type_vector = CALLBACK(self.__on_type_vector)
        if hasattr(self, "on_type_hvector"):
            self.cbacks.on_type_hvector = CALLBACK(self.__on_type_hvector)
        if hasattr(self, "on_type_indexed"):
            self.cbacks.on_type_indexed = CALLBACK(self.__on_type_indexed)
        if hasattr(self, "on_type_hindexed"):
            self.cbacks.on_type_hindexed = CALLBACK(self.__on_type_hindexed)
        if hasattr(self, "on_type_struct"):
            self.cbacks.on_type_struct = CALLBACK(self.__on_type_struct)
        if hasattr(self, "on_address"):
            self.cbacks.on_address = CALLBACK(self.__on_address)
        if hasattr(self, "on_type_extent"):
            self.cbacks.on_type_extent = CALLBACK(self.__on_type_extent)
        if hasattr(self, "on_type_size"):
            self.cbacks.on_type_size = CALLBACK(self.__on_type_size)
        if hasattr(self, "on_type_lb"):
            self.cbacks.on_type_lb = CALLBACK(self.__on_type_lb)
        if hasattr(self, "on_type_ub"):
            self.cbacks.on_type_ub = CALLBACK(self.__on_type_ub)
        if hasattr(self, "on_type_commit"):
            self.cbacks.on_type_commit = CALLBACK(self.__on_type_commit)
        if hasattr(self, "on_type_free"):
            self.cbacks.on_type_free = CALLBACK(self.__on_type_free)
        if hasattr(self, "on_get_elements"):
            self.cbacks.on_get_elements = CALLBACK(self.__on_get_elements)
        if hasattr(self, "on_pack"):
            self.cbacks.on_pack = CALLBACK(self.__on_pack)
        if hasattr(self, "on_unpack"):
            self.cbacks.on_unpack = CALLBACK(self.__on_unpack)
        if hasattr(self, "on_pack_size"):
            self.cbacks.on_pack_size = CALLBACK(self.__on_pack_size)
        if hasattr(self, "on_barrier"):
            self.cbacks.on_barrier = CALLBACK(self.__on_barrier)
        if hasattr(self, "on_bcast"):
            self.cbacks.on_bcast = CALLBACK(self.__on_bcast)
        if hasattr(self, "on_gather"):
            self.cbacks.on_gather = CALLBACK(self.__on_gather)
        if hasattr(self, "on_gatherv"):
            self.cbacks.on_gatherv = CALLBACK(self.__on_gatherv)
        if hasattr(self, "on_scatter"):
            self.cbacks.on_scatter = CALLBACK(self.__on_scatter)
        if hasattr(self, "on_scatterv"):
            self.cbacks.on_scatterv = CALLBACK(self.__on_scatterv)
        if hasattr(self, "on_allgather"):
            self.cbacks.on_allgather = CALLBACK(self.__on_allgather)
        if hasattr(self, "on_allgatherv"):
            self.cbacks.on_allgatherv = CALLBACK(self.__on_allgatherv)
        if hasattr(self, "on_alltoall"):
            self.cbacks.on_alltoall = CALLBACK(self.__on_alltoall)
        if hasattr(self, "on_alltoallv"):
            self.cbacks.on_alltoallv = CALLBACK(self.__on_alltoallv)
        if hasattr(self, "on_reduce"):
            self.cbacks.on_reduce = CALLBACK(self.__on_reduce)
        if hasattr(self, "on_op_create"):
            self.cbacks.on_op_create = CALLBACK(self.__on_op_create)
        if hasattr(self, "on_op_free"):
            self.cbacks.on_op_free = CALLBACK(self.__on_op_free)
        if hasattr(self, "on_allreduce"):
            self.cbacks.on_allreduce = CALLBACK(self.__on_allreduce)
        if hasattr(self, "on_reduce_scatter"):
            self.cbacks.on_reduce_scatter = CALLBACK(self.__on_reduce_scatter)
        if hasattr(self, "on_scan"):
            self.cbacks.on_scan = CALLBACK(self.__on_scan)
        if hasattr(self, "on_group_size"):
            self.cbacks.on_group_size = CALLBACK(self.__on_group_size)
        if hasattr(self, "on_group_rank"):
            self.cbacks.on_group_rank = CALLBACK(self.__on_group_rank)
        if hasattr(self, "on_group_translate_ranks"):
            self.cbacks.on_group_translate_ranks = CALLBACK(self.__on_group_translate_ranks)
        if hasattr(self, "on_group_compare"):
            self.cbacks.on_group_compare = CALLBACK(self.__on_group_compare)
        if hasattr(self, "on_comm_group"):
            self.cbacks.on_comm_group = CALLBACK(self.__on_comm_group)
        if hasattr(self, "on_group_union"):
            self.cbacks.on_group_union = CALLBACK(self.__on_group_union)
        if hasattr(self, "on_group_intersection"):
            self.cbacks.on_group_intersection = CALLBACK(self.__on_group_intersection)
        if hasattr(self, "on_group_difference"):
            self.cbacks.on_group_difference = CALLBACK(self.__on_group_difference)
        if hasattr(self, "on_group_incl"):
            self.cbacks.on_group_incl = CALLBACK(self.__on_group_incl)
        if hasattr(self, "on_group_excl"):
            self.cbacks.on_group_excl = CALLBACK(self.__on_group_excl)
        if hasattr(self, "on_group_range_incl"):
            self.cbacks.on_group_range_incl = CALLBACK(self.__on_group_range_incl)
        if hasattr(self, "on_group_range_excl"):
            self.cbacks.on_group_range_excl = CALLBACK(self.__on_group_range_excl)
        if hasattr(self, "on_group_free"):
            self.cbacks.on_group_free = CALLBACK(self.__on_group_free)
        if hasattr(self, "on_comm_size"):
            self.cbacks.on_comm_size = CALLBACK(self.__on_comm_size)
        if hasattr(self, "on_comm_rank"):
            self.cbacks.on_comm_rank = CALLBACK(self.__on_comm_rank)
        if hasattr(self, "on_comm_compare"):
            self.cbacks.on_comm_compare = CALLBACK(self.__on_comm_compare)
        if hasattr(self, "on_comm_dup"):
            self.cbacks.on_comm_dup = CALLBACK(self.__on_comm_dup)
        if hasattr(self, "on_comm_create"):
            self.cbacks.on_comm_create = CALLBACK(self.__on_comm_create)
        if hasattr(self, "on_comm_split"):
            self.cbacks.on_comm_split = CALLBACK(self.__on_comm_split)
        if hasattr(self, "on_comm_free"):
            self.cbacks.on_comm_free = CALLBACK(self.__on_comm_free)
        if hasattr(self, "on_comm_test_inter"):
            self.cbacks.on_comm_test_inter = CALLBACK(self.__on_comm_test_inter)
        if hasattr(self, "on_comm_remote_size"):
            self.cbacks.on_comm_remote_size = CALLBACK(self.__on_comm_remote_size)
        if hasattr(self, "on_comm_remote_group"):
            self.cbacks.on_comm_remote_group = CALLBACK(self.__on_comm_remote_group)
        if hasattr(self, "on_intercomm_create"):
            self.cbacks.on_intercomm_create = CALLBACK(self.__on_intercomm_create)
        if hasattr(self, "on_intercomm_merge"):
            self.cbacks.on_intercomm_merge = CALLBACK(self.__on_intercomm_merge)
        if hasattr(self, "on_keyval_create"):
            self.cbacks.on_keyval_create = CALLBACK(self.__on_keyval_create)
        if hasattr(self, "on_keyval_free"):
            self.cbacks.on_keyval_free = CALLBACK(self.__on_keyval_free)
        if hasattr(self, "on_attr_put"):
            self.cbacks.on_attr_put = CALLBACK(self.__on_attr_put)
        if hasattr(self, "on_attr_get"):
            self.cbacks.on_attr_get = CALLBACK(self.__on_attr_get)
        if hasattr(self, "on_attr_delete"):
            self.cbacks.on_attr_delete = CALLBACK(self.__on_attr_delete)
        if hasattr(self, "on_topo_test"):
            self.cbacks.on_topo_test = CALLBACK(self.__on_topo_test)
        if hasattr(self, "on_cart_create"):
            self.cbacks.on_cart_create = CALLBACK(self.__on_cart_create)
        if hasattr(self, "on_dims_create"):
            self.cbacks.on_dims_create = CALLBACK(self.__on_dims_create)
        if hasattr(self, "on_graph_create"):
            self.cbacks.on_graph_create = CALLBACK(self.__on_graph_create)
        if hasattr(self, "on_graphdims_get"):
            self.cbacks.on_graphdims_get = CALLBACK(self.__on_graphdims_get)
        if hasattr(self, "on_graph_get"):
            self.cbacks.on_graph_get = CALLBACK(self.__on_graph_get)
        if hasattr(self, "on_cartdim_get"):
            self.cbacks.on_cartdim_get = CALLBACK(self.__on_cartdim_get)
        if hasattr(self, "on_cart_get"):
            self.cbacks.on_cart_get = CALLBACK(self.__on_cart_get)
        if hasattr(self, "on_cart_rank"):
            self.cbacks.on_cart_rank = CALLBACK(self.__on_cart_rank)
        if hasattr(self, "on_cart_coords"):
            self.cbacks.on_cart_coords = CALLBACK(self.__on_cart_coords)
        if hasattr(self, "on_graph_neighbors_count"):
            self.cbacks.on_graph_neighbors_count = CALLBACK(self.__on_graph_neighbors_count)
        if hasattr(self, "on_graph_neighbors"):
            self.cbacks.on_graph_neighbors = CALLBACK(self.__on_graph_neighbors)
        if hasattr(self, "on_cart_shift"):
            self.cbacks.on_cart_shift = CALLBACK(self.__on_cart_shift)
        if hasattr(self, "on_cart_sub"):
            self.cbacks.on_cart_sub = CALLBACK(self.__on_cart_sub)
        if hasattr(self, "on_cart_map"):
            self.cbacks.on_cart_map = CALLBACK(self.__on_cart_map)
        if hasattr(self, "on_graph_map"):
            self.cbacks.on_graph_map = CALLBACK(self.__on_graph_map)
        if hasattr(self, "on_get_processor_name"):
            self.cbacks.on_get_processor_name = CALLBACK(self.__on_get_processor_name)
        if hasattr(self, "on_get_version"):
            self.cbacks.on_get_version = CALLBACK(self.__on_get_version)
        if hasattr(self, "on_errhandler_create"):
            self.cbacks.on_errhandler_create = CALLBACK(self.__on_errhandler_create)
        if hasattr(self, "on_errhandler_set"):
            self.cbacks.on_errhandler_set = CALLBACK(self.__on_errhandler_set)
        if hasattr(self, "on_errhandler_get"):
            self.cbacks.on_errhandler_get = CALLBACK(self.__on_errhandler_get)
        if hasattr(self, "on_errhandler_free"):
            self.cbacks.on_errhandler_free = CALLBACK(self.__on_errhandler_free)
        if hasattr(self, "on_error_string"):
            self.cbacks.on_error_string = CALLBACK(self.__on_error_string)
        if hasattr(self, "on_error_class"):
            self.cbacks.on_error_class = CALLBACK(self.__on_error_class)
        if hasattr(self, "on_wtime"):
            self.cbacks.on_wtime = CALLBACK(self.__on_wtime)
        if hasattr(self, "on_wtick"):
            self.cbacks.on_wtick = CALLBACK(self.__on_wtick)
        if hasattr(self, "on_init"):
            self.cbacks.on_init = CALLBACK(self.__on_init)
        if hasattr(self, "on_finalize"):
            self.cbacks.on_finalize = CALLBACK(self.__on_finalize)
        if hasattr(self, "on_initialized"):
            self.cbacks.on_initialized = CALLBACK(self.__on_initialized)
        if hasattr(self, "on_abort"):
            self.cbacks.on_abort = CALLBACK(self.__on_abort)
        if hasattr(self, "on_close_port"):
            self.cbacks.on_close_port = CALLBACK(self.__on_close_port)
        if hasattr(self, "on_comm_accept"):
            self.cbacks.on_comm_accept = CALLBACK(self.__on_comm_accept)
        if hasattr(self, "on_comm_connect"):
            self.cbacks.on_comm_connect = CALLBACK(self.__on_comm_connect)
        if hasattr(self, "on_comm_disconnect"):
            self.cbacks.on_comm_disconnect = CALLBACK(self.__on_comm_disconnect)
        if hasattr(self, "on_comm_get_parent"):
            self.cbacks.on_comm_get_parent = CALLBACK(self.__on_comm_get_parent)
        if hasattr(self, "on_comm_join"):
            self.cbacks.on_comm_join = CALLBACK(self.__on_comm_join)
        if hasattr(self, "on_comm_spawn"):
            self.cbacks.on_comm_spawn = CALLBACK(self.__on_comm_spawn)
        if hasattr(self, "on_comm_spawn_multiple"):
            self.cbacks.on_comm_spawn_multiple = CALLBACK(self.__on_comm_spawn_multiple)
        if hasattr(self, "on_lookup_name"):
            self.cbacks.on_lookup_name = CALLBACK(self.__on_lookup_name)
        if hasattr(self, "on_open_port"):
            self.cbacks.on_open_port = CALLBACK(self.__on_open_port)
        if hasattr(self, "on_publish_name"):
            self.cbacks.on_publish_name = CALLBACK(self.__on_publish_name)
        if hasattr(self, "on_unpublish_name"):
            self.cbacks.on_unpublish_name = CALLBACK(self.__on_unpublish_name)
        if hasattr(self, "on_accumulate"):
            self.cbacks.on_accumulate = CALLBACK(self.__on_accumulate)
        if hasattr(self, "on_get"):
            self.cbacks.on_get = CALLBACK(self.__on_get)
        if hasattr(self, "on_put"):
            self.cbacks.on_put = CALLBACK(self.__on_put)
        if hasattr(self, "on_win_complete"):
            self.cbacks.on_win_complete = CALLBACK(self.__on_win_complete)
        if hasattr(self, "on_win_create"):
            self.cbacks.on_win_create = CALLBACK(self.__on_win_create)
        if hasattr(self, "on_win_fence"):
            self.cbacks.on_win_fence = CALLBACK(self.__on_win_fence)
        if hasattr(self, "on_win_free"):
            self.cbacks.on_win_free = CALLBACK(self.__on_win_free)
        if hasattr(self, "on_win_get_group"):
            self.cbacks.on_win_get_group = CALLBACK(self.__on_win_get_group)
        if hasattr(self, "on_win_lock"):
            self.cbacks.on_win_lock = CALLBACK(self.__on_win_lock)
        if hasattr(self, "on_win_post"):
            self.cbacks.on_win_post = CALLBACK(self.__on_win_post)
        if hasattr(self, "on_win_start"):
            self.cbacks.on_win_start = CALLBACK(self.__on_win_start)
        if hasattr(self, "on_win_test"):
            self.cbacks.on_win_test = CALLBACK(self.__on_win_test)
        if hasattr(self, "on_win_unlock"):
            self.cbacks.on_win_unlock = CALLBACK(self.__on_win_unlock)
        if hasattr(self, "on_win_wait"):
            self.cbacks.on_win_wait = CALLBACK(self.__on_win_wait)
        if hasattr(self, "on_alltoallw"):
            self.cbacks.on_alltoallw = CALLBACK(self.__on_alltoallw)
        if hasattr(self, "on_exscan"):
            self.cbacks.on_exscan = CALLBACK(self.__on_exscan)
        if hasattr(self, "on_add_error_class"):
            self.cbacks.on_add_error_class = CALLBACK(self.__on_add_error_class)
        if hasattr(self, "on_add_error_code"):
            self.cbacks.on_add_error_code = CALLBACK(self.__on_add_error_code)
        if hasattr(self, "on_add_error_string"):
            self.cbacks.on_add_error_string = CALLBACK(self.__on_add_error_string)
        if hasattr(self, "on_comm_call_errhandler"):
            self.cbacks.on_comm_call_errhandler = CALLBACK(self.__on_comm_call_errhandler)
        if hasattr(self, "on_comm_create_keyval"):
            self.cbacks.on_comm_create_keyval = CALLBACK(self.__on_comm_create_keyval)
        if hasattr(self, "on_comm_delete_attr"):
            self.cbacks.on_comm_delete_attr = CALLBACK(self.__on_comm_delete_attr)
        if hasattr(self, "on_comm_free_keyval"):
            self.cbacks.on_comm_free_keyval = CALLBACK(self.__on_comm_free_keyval)
        if hasattr(self, "on_comm_get_attr"):
            self.cbacks.on_comm_get_attr = CALLBACK(self.__on_comm_get_attr)
        if hasattr(self, "on_comm_get_name"):
            self.cbacks.on_comm_get_name = CALLBACK(self.__on_comm_get_name)
        if hasattr(self, "on_comm_set_attr"):
            self.cbacks.on_comm_set_attr = CALLBACK(self.__on_comm_set_attr)
        if hasattr(self, "on_comm_set_name"):
            self.cbacks.on_comm_set_name = CALLBACK(self.__on_comm_set_name)
        if hasattr(self, "on_file_call_errhandler"):
            self.cbacks.on_file_call_errhandler = CALLBACK(self.__on_file_call_errhandler)
        if hasattr(self, "on_grequest_complete"):
            self.cbacks.on_grequest_complete = CALLBACK(self.__on_grequest_complete)
        if hasattr(self, "on_grequest_start"):
            self.cbacks.on_grequest_start = CALLBACK(self.__on_grequest_start)
        if hasattr(self, "on_init_thread"):
            self.cbacks.on_init_thread = CALLBACK(self.__on_init_thread)
        if hasattr(self, "on_is_thread_main"):
            self.cbacks.on_is_thread_main = CALLBACK(self.__on_is_thread_main)
        if hasattr(self, "on_query_thread"):
            self.cbacks.on_query_thread = CALLBACK(self.__on_query_thread)
        if hasattr(self, "on_status_set_cancelled"):
            self.cbacks.on_status_set_cancelled = CALLBACK(self.__on_status_set_cancelled)
        if hasattr(self, "on_status_set_elements"):
            self.cbacks.on_status_set_elements = CALLBACK(self.__on_status_set_elements)
        if hasattr(self, "on_type_create_keyval"):
            self.cbacks.on_type_create_keyval = CALLBACK(self.__on_type_create_keyval)
        if hasattr(self, "on_type_delete_attr"):
            self.cbacks.on_type_delete_attr = CALLBACK(self.__on_type_delete_attr)
        if hasattr(self, "on_type_dup"):
            self.cbacks.on_type_dup = CALLBACK(self.__on_type_dup)
        if hasattr(self, "on_type_free_keyval"):
            self.cbacks.on_type_free_keyval = CALLBACK(self.__on_type_free_keyval)
        if hasattr(self, "on_type_get_attr"):
            self.cbacks.on_type_get_attr = CALLBACK(self.__on_type_get_attr)
        if hasattr(self, "on_type_get_contents"):
            self.cbacks.on_type_get_contents = CALLBACK(self.__on_type_get_contents)
        if hasattr(self, "on_type_get_envelope"):
            self.cbacks.on_type_get_envelope = CALLBACK(self.__on_type_get_envelope)
        if hasattr(self, "on_type_get_name"):
            self.cbacks.on_type_get_name = CALLBACK(self.__on_type_get_name)
        if hasattr(self, "on_type_set_attr"):
            self.cbacks.on_type_set_attr = CALLBACK(self.__on_type_set_attr)
        if hasattr(self, "on_type_set_name"):
            self.cbacks.on_type_set_name = CALLBACK(self.__on_type_set_name)
        if hasattr(self, "on_type_match_size"):
            self.cbacks.on_type_match_size = CALLBACK(self.__on_type_match_size)
        if hasattr(self, "on_win_call_errhandler"):
            self.cbacks.on_win_call_errhandler = CALLBACK(self.__on_win_call_errhandler)
        if hasattr(self, "on_win_create_keyval"):
            self.cbacks.on_win_create_keyval = CALLBACK(self.__on_win_create_keyval)
        if hasattr(self, "on_win_delete_attr"):
            self.cbacks.on_win_delete_attr = CALLBACK(self.__on_win_delete_attr)
        if hasattr(self, "on_win_free_keyval"):
            self.cbacks.on_win_free_keyval = CALLBACK(self.__on_win_free_keyval)
        if hasattr(self, "on_win_get_attr"):
            self.cbacks.on_win_get_attr = CALLBACK(self.__on_win_get_attr)
        if hasattr(self, "on_win_get_name"):
            self.cbacks.on_win_get_name = CALLBACK(self.__on_win_get_name)
        if hasattr(self, "on_win_set_attr"):
            self.cbacks.on_win_set_attr = CALLBACK(self.__on_win_set_attr)
        if hasattr(self, "on_win_set_name"):
            self.cbacks.on_win_set_name = CALLBACK(self.__on_win_set_name)
        if hasattr(self, "on_alloc_mem"):
            self.cbacks.on_alloc_mem = CALLBACK(self.__on_alloc_mem)
        if hasattr(self, "on_comm_create_errhandler"):
            self.cbacks.on_comm_create_errhandler = CALLBACK(self.__on_comm_create_errhandler)
        if hasattr(self, "on_comm_get_errhandler"):
            self.cbacks.on_comm_get_errhandler = CALLBACK(self.__on_comm_get_errhandler)
        if hasattr(self, "on_comm_set_errhandler"):
            self.cbacks.on_comm_set_errhandler = CALLBACK(self.__on_comm_set_errhandler)
        if hasattr(self, "on_file_create_errhandler"):
            self.cbacks.on_file_create_errhandler = CALLBACK(self.__on_file_create_errhandler)
        if hasattr(self, "on_file_get_errhandler"):
            self.cbacks.on_file_get_errhandler = CALLBACK(self.__on_file_get_errhandler)
        if hasattr(self, "on_file_set_errhandler"):
            self.cbacks.on_file_set_errhandler = CALLBACK(self.__on_file_set_errhandler)
        if hasattr(self, "on_finalized"):
            self.cbacks.on_finalized = CALLBACK(self.__on_finalized)
        if hasattr(self, "on_free_mem"):
            self.cbacks.on_free_mem = CALLBACK(self.__on_free_mem)
        if hasattr(self, "on_get_address"):
            self.cbacks.on_get_address = CALLBACK(self.__on_get_address)
        if hasattr(self, "on_info_create"):
            self.cbacks.on_info_create = CALLBACK(self.__on_info_create)
        if hasattr(self, "on_info_delete"):
            self.cbacks.on_info_delete = CALLBACK(self.__on_info_delete)
        if hasattr(self, "on_info_dup"):
            self.cbacks.on_info_dup = CALLBACK(self.__on_info_dup)
        if hasattr(self, "on_info_free"):
            self.cbacks.on_info_free = CALLBACK(self.__on_info_free)
        if hasattr(self, "on_info_get"):
            self.cbacks.on_info_get = CALLBACK(self.__on_info_get)
        if hasattr(self, "on_info_get_nkeys"):
            self.cbacks.on_info_get_nkeys = CALLBACK(self.__on_info_get_nkeys)
        if hasattr(self, "on_info_get_nthkey"):
            self.cbacks.on_info_get_nthkey = CALLBACK(self.__on_info_get_nthkey)
        if hasattr(self, "on_info_get_valuelen"):
            self.cbacks.on_info_get_valuelen = CALLBACK(self.__on_info_get_valuelen)
        if hasattr(self, "on_info_set"):
            self.cbacks.on_info_set = CALLBACK(self.__on_info_set)
        if hasattr(self, "on_pack_external"):
            self.cbacks.on_pack_external = CALLBACK(self.__on_pack_external)
        if hasattr(self, "on_pack_external_size"):
            self.cbacks.on_pack_external_size = CALLBACK(self.__on_pack_external_size)
        if hasattr(self, "on_request_get_status"):
            self.cbacks.on_request_get_status = CALLBACK(self.__on_request_get_status)
        if hasattr(self, "on_type_create_darray"):
            self.cbacks.on_type_create_darray = CALLBACK(self.__on_type_create_darray)
        if hasattr(self, "on_type_create_hindexed"):
            self.cbacks.on_type_create_hindexed = CALLBACK(self.__on_type_create_hindexed)
        if hasattr(self, "on_type_create_hvector"):
            self.cbacks.on_type_create_hvector = CALLBACK(self.__on_type_create_hvector)
        if hasattr(self, "on_type_create_indexed_block"):
            self.cbacks.on_type_create_indexed_block = CALLBACK(self.__on_type_create_indexed_block)
        if hasattr(self, "on_type_create_resized"):
            self.cbacks.on_type_create_resized = CALLBACK(self.__on_type_create_resized)
        if hasattr(self, "on_type_create_struct"):
            self.cbacks.on_type_create_struct = CALLBACK(self.__on_type_create_struct)
        if hasattr(self, "on_type_create_subarray"):
            self.cbacks.on_type_create_subarray = CALLBACK(self.__on_type_create_subarray)
        if hasattr(self, "on_type_get_extent"):
            self.cbacks.on_type_get_extent = CALLBACK(self.__on_type_get_extent)
        if hasattr(self, "on_type_get_true_extent"):
            self.cbacks.on_type_get_true_extent = CALLBACK(self.__on_type_get_true_extent)
        if hasattr(self, "on_unpack_external"):
            self.cbacks.on_unpack_external = CALLBACK(self.__on_unpack_external)
        if hasattr(self, "on_win_create_errhandler"):
            self.cbacks.on_win_create_errhandler = CALLBACK(self.__on_win_create_errhandler)
        if hasattr(self, "on_win_get_errhandler"):
            self.cbacks.on_win_get_errhandler = CALLBACK(self.__on_win_get_errhandler)
        if hasattr(self, "on_win_set_errhandler"):
            self.cbacks.on_win_set_errhandler = CALLBACK(self.__on_win_set_errhandler)
        if hasattr(self, "on_file_open"):
            self.cbacks.on_file_open = CALLBACK(self.__on_file_open)
        if hasattr(self, "on_file_close"):
            self.cbacks.on_file_close = CALLBACK(self.__on_file_close)
        if hasattr(self, "on_file_delete"):
            self.cbacks.on_file_delete = CALLBACK(self.__on_file_delete)
        if hasattr(self, "on_file_set_size"):
            self.cbacks.on_file_set_size = CALLBACK(self.__on_file_set_size)
        if hasattr(self, "on_file_preallocate"):
            self.cbacks.on_file_preallocate = CALLBACK(self.__on_file_preallocate)
        if hasattr(self, "on_file_get_size"):
            self.cbacks.on_file_get_size = CALLBACK(self.__on_file_get_size)
        if hasattr(self, "on_file_get_group"):
            self.cbacks.on_file_get_group = CALLBACK(self.__on_file_get_group)
        if hasattr(self, "on_file_get_amode"):
            self.cbacks.on_file_get_amode = CALLBACK(self.__on_file_get_amode)
        if hasattr(self, "on_file_set_info"):
            self.cbacks.on_file_set_info = CALLBACK(self.__on_file_set_info)
        if hasattr(self, "on_file_get_info"):
            self.cbacks.on_file_get_info = CALLBACK(self.__on_file_get_info)
        if hasattr(self, "on_file_set_view"):
            self.cbacks.on_file_set_view = CALLBACK(self.__on_file_set_view)
        if hasattr(self, "on_file_get_view"):
            self.cbacks.on_file_get_view = CALLBACK(self.__on_file_get_view)
        if hasattr(self, "on_file_read_at"):
            self.cbacks.on_file_read_at = CALLBACK(self.__on_file_read_at)
        if hasattr(self, "on_file_read_at_all"):
            self.cbacks.on_file_read_at_all = CALLBACK(self.__on_file_read_at_all)
        if hasattr(self, "on_file_write_at"):
            self.cbacks.on_file_write_at = CALLBACK(self.__on_file_write_at)
        if hasattr(self, "on_file_write_at_all"):
            self.cbacks.on_file_write_at_all = CALLBACK(self.__on_file_write_at_all)
        if hasattr(self, "on_file_iread_at"):
            self.cbacks.on_file_iread_at = CALLBACK(self.__on_file_iread_at)
        if hasattr(self, "on_file_iwrite_at"):
            self.cbacks.on_file_iwrite_at = CALLBACK(self.__on_file_iwrite_at)
        if hasattr(self, "on_file_read"):
            self.cbacks.on_file_read = CALLBACK(self.__on_file_read)
        if hasattr(self, "on_file_read_all"):
            self.cbacks.on_file_read_all = CALLBACK(self.__on_file_read_all)
        if hasattr(self, "on_file_write"):
            self.cbacks.on_file_write = CALLBACK(self.__on_file_write)
        if hasattr(self, "on_file_write_all"):
            self.cbacks.on_file_write_all = CALLBACK(self.__on_file_write_all)
        if hasattr(self, "on_file_iread"):
            self.cbacks.on_file_iread = CALLBACK(self.__on_file_iread)
        if hasattr(self, "on_file_iwrite"):
            self.cbacks.on_file_iwrite = CALLBACK(self.__on_file_iwrite)
        if hasattr(self, "on_file_seek"):
            self.cbacks.on_file_seek = CALLBACK(self.__on_file_seek)
        if hasattr(self, "on_file_get_position"):
            self.cbacks.on_file_get_position = CALLBACK(self.__on_file_get_position)
        if hasattr(self, "on_file_get_byte_offset"):
            self.cbacks.on_file_get_byte_offset = CALLBACK(self.__on_file_get_byte_offset)
        if hasattr(self, "on_file_read_shared"):
            self.cbacks.on_file_read_shared = CALLBACK(self.__on_file_read_shared)
        if hasattr(self, "on_file_write_shared"):
            self.cbacks.on_file_write_shared = CALLBACK(self.__on_file_write_shared)
        if hasattr(self, "on_file_iread_shared"):
            self.cbacks.on_file_iread_shared = CALLBACK(self.__on_file_iread_shared)
        if hasattr(self, "on_file_iwrite_shared"):
            self.cbacks.on_file_iwrite_shared = CALLBACK(self.__on_file_iwrite_shared)
        if hasattr(self, "on_file_read_ordered"):
            self.cbacks.on_file_read_ordered = CALLBACK(self.__on_file_read_ordered)
        if hasattr(self, "on_file_write_ordered"):
            self.cbacks.on_file_write_ordered = CALLBACK(self.__on_file_write_ordered)
        if hasattr(self, "on_file_seek_shared"):
            self.cbacks.on_file_seek_shared = CALLBACK(self.__on_file_seek_shared)
        if hasattr(self, "on_file_get_position_shared"):
            self.cbacks.on_file_get_position_shared = CALLBACK(self.__on_file_get_position_shared)
        if hasattr(self, "on_file_read_at_all_begin"):
            self.cbacks.on_file_read_at_all_begin = CALLBACK(self.__on_file_read_at_all_begin)
        if hasattr(self, "on_file_read_at_all_end"):
            self.cbacks.on_file_read_at_all_end = CALLBACK(self.__on_file_read_at_all_end)
        if hasattr(self, "on_file_write_at_all_begin"):
            self.cbacks.on_file_write_at_all_begin = CALLBACK(self.__on_file_write_at_all_begin)
        if hasattr(self, "on_file_write_at_all_end"):
            self.cbacks.on_file_write_at_all_end = CALLBACK(self.__on_file_write_at_all_end)
        if hasattr(self, "on_file_read_all_begin"):
            self.cbacks.on_file_read_all_begin = CALLBACK(self.__on_file_read_all_begin)
        if hasattr(self, "on_file_read_all_end"):
            self.cbacks.on_file_read_all_end = CALLBACK(self.__on_file_read_all_end)
        if hasattr(self, "on_file_write_all_begin"):
            self.cbacks.on_file_write_all_begin = CALLBACK(self.__on_file_write_all_begin)
        if hasattr(self, "on_file_write_all_end"):
            self.cbacks.on_file_write_all_end = CALLBACK(self.__on_file_write_all_end)
        if hasattr(self, "on_file_read_ordered_begin"):
            self.cbacks.on_file_read_ordered_begin = CALLBACK(self.__on_file_read_ordered_begin)
        if hasattr(self, "on_file_read_ordered_end"):
            self.cbacks.on_file_read_ordered_end = CALLBACK(self.__on_file_read_ordered_end)
        if hasattr(self, "on_file_write_ordered_begin"):
            self.cbacks.on_file_write_ordered_begin = CALLBACK(self.__on_file_write_ordered_begin)
        if hasattr(self, "on_file_write_ordered_end"):
            self.cbacks.on_file_write_ordered_end = CALLBACK(self.__on_file_write_ordered_end)
        if hasattr(self, "on_file_get_type_extent"):
            self.cbacks.on_file_get_type_extent = CALLBACK(self.__on_file_get_type_extent)
        if hasattr(self, "on_register_datarep"):
            self.cbacks.on_register_datarep = CALLBACK(self.__on_register_datarep)
        if hasattr(self, "on_file_set_atomicity"):
            self.cbacks.on_file_set_atomicity = CALLBACK(self.__on_file_set_atomicity)
        if hasattr(self, "on_file_get_atomicity"):
            self.cbacks.on_file_get_atomicity = CALLBACK(self.__on_file_get_atomicity)
        if hasattr(self, "on_file_sync"):
            self.cbacks.on_file_sync = CALLBACK(self.__on_file_sync)
        if hasattr(self, "on_iotest"):
            self.cbacks.on_iotest = CALLBACK(self.__on_iotest)
        if hasattr(self, "on_iowait"):
            self.cbacks.on_iowait = CALLBACK(self.__on_iowait)
        if hasattr(self, "on_iotestall"):
            self.cbacks.on_iotestall = CALLBACK(self.__on_iotestall)
        if hasattr(self, "on_iowaitall"):
            self.cbacks.on_iowaitall = CALLBACK(self.__on_iowaitall)
        if hasattr(self, "on_iotestany"):
            self.cbacks.on_iotestany = CALLBACK(self.__on_iotestany)
        if hasattr(self, "on_iowaitany"):
            self.cbacks.on_iowaitany = CALLBACK(self.__on_iowaitany)
        if hasattr(self, "on_iowaitsome"):
            self.cbacks.on_iowaitsome = CALLBACK(self.__on_iowaitsome)
        if hasattr(self, "on_iotestsome"):
            self.cbacks.on_iotestsome = CALLBACK(self.__on_iotestsome)
        if hasattr(self, "on_function_enter"):
            self.cbacks.on_function_enter = CALLBACK(self.__on_function_enter)
        if hasattr(self, "on_function_exit"):
            self.cbacks.on_function_exit = CALLBACK(self.__on_function_exit)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc_details):
        self.close()

    def open(self):
        if self._profile:
            return

        # the weird conversions are for interfacing with c-strings
        file_name_buf = create_string_buffer(bytes(str(self.file_name), "utf-8"));

        # calling undumpi_read_datatype_sizes apparently moves the filepointer
        # to the end of the file, skipping everything - we therefore open the
        # file once to read the sizes, then reopen it again for real processing
        profile = undumpi_open(file_name_buf)
        sizes = DumpiSizeof()
        undumpi_read_datatype_sizes(profile, byref(sizes))
        self._type_sizes = [sizes.size[i] for i in range(sizes.count)]
        libc.free(sizes.size)
        undumpi_close(profile)

        # now open the file for real
        self._profile = undumpi_open(file_name_buf)

    def close(self):
        if self._profile:
            undumpi_close(self._profile)

    @property
    def type_sizes(self):
        if not self._profile:
            raise ValueError("Can't read data sizes without open dumpi trace.")
        return self._type_sizes

    def print_sizes(self):
        if not self._profile:
            raise ValueError("Can't read data sizes without open dumpi trace.")
        print("DataType Sizes:")
        for i, type_size in enumerate(self.type_sizes):
            if i < 28:
                print(f"  {DataType(i).name} has size {type_size}")
            else: # anything >= 28 is a user-defined type
                print(f"  user-defined-datatype has size {type_size}")
        print()

    def print_header(self):
        if not self._profile:
            raise ValueError("Can't read header without open dumpi trace.")
        header = undumpi_read_header(self._profile).contents
        v = header.version
        print("Header:")
        print(f"  version: {v[0]}.{v[1]}.{v[2]}")
        time_struct = time.gmtime(header.starttime)
        print(f"  starttime: {time.asctime(time_struct)}")
        print(f"  hostname: {header.hostname.decode('utf-8')}")
        print(f"  username: {header.username.decode('utf-8')}")
        meshdim = header.meshdim
        print(f"  meshdim: {meshdim}")
        print("  meshsize: [", end="")
        for i in range(meshdim):
            print("{header.meshsize[i]}", end="")
            if i < meshdim-1:
                print(", ", end="")
        print("]")
        print("  meshcrd: [", end="")
        for i in range(meshdim):
            print("{header.meshcrd[i]}", end="")
            if i < meshdim-1:
                print(", ", end="")
        print("]")
        print()

    def print_footer(self):
        if not self._profile:
            raise ValueError("Can't read footer without open dumpi trace.")
        footer = undumpi_read_footer(self._profile).contents
        calls = [(i, c) for i, c in enumerate(footer.call_count) if c > 0]
        print("Function Call Count:")
        for call in calls:
            print(f"  {DumpiCallbacks._fields_[call[0]][0]}: {call[1]}")
        print()

    def read_stream(self):
        if not self._profile:
            raise ValueError("Can't read stream without open dumpi trace.")
        undumpi_read_stream(self._profile, byref(self.cbacks), None)

    def __on_send(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiSend))
        self.on_send(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_recv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRecv))
        self.on_recv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_get_count(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGetCount))
        self.on_get_count(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_bsend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiBSend))
        self.on_bsend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_ssend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiSSend))
        self.on_ssend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_rsend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRSend))
        self.on_rsend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_buffer_attach(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiBufferAttach))
        self.on_buffer_attach(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_buffer_detach(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiBufferDetach))
        self.on_buffer_detach(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_isend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiISend))
        self.on_isend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_ibsend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIbSend))
        self.on_ibsend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_issend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIsSend))
        self.on_issend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_irsend(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIrSend))
        self.on_irsend(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_irecv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIRecv))
        self.on_irecv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_wait(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWait))
        self.on_wait(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_test(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTest))
        self.on_test(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_request_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRequestFree))
        self.on_request_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_waitany(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWaitAny))
        self.on_waitany(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_testany(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTestAny))
        self.on_testany(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_waitall(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWaitAll))
        self.on_waitall(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_testall(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTestAll))
        self.on_testall(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_waitsome(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWaitSome))
        self.on_waitsome(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_testsome(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTestSome))
        self.on_testsome(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iprobe(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIprobe))
        self.on_iprobe(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_probe(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiProbe))
        self.on_probe(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cancel(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCancel))
        self.on_cancel(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_test_cancelled(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTestCancelled))
        self.on_test_cancelled(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_send_init(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiSendInit))
        self.on_send_init(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_bsend_init(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiBsendInit))
        self.on_bsend_init(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_ssend_init(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiSsendInit))
        self.on_ssend_init(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_rsend_init(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRsendInit))
        self.on_rsend_init(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_recv_init(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRecvInit))
        self.on_recv_init(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_start(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiStart))
        self.on_start(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_startall(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiStartall))
        self.on_startall(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_sendrecv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiSendrecv))
        self.on_sendrecv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_sendrecv_replace(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiSendrecvReplace))
        self.on_sendrecv_replace(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_contiguous(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeContiguous))
        self.on_type_contiguous(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_vector(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeVector))
        self.on_type_vector(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_hvector(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeHvector))
        self.on_type_hvector(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_indexed(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeIndexed))
        self.on_type_indexed(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_hindexed(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeHindexed))
        self.on_type_hindexed(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_struct(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeStruct))
        self.on_type_struct(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_address(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAddress))
        self.on_address(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_extent(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeExtent))
        self.on_type_extent(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeSize))
        self.on_type_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_lb(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeLb))
        self.on_type_lb(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_ub(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeUb))
        self.on_type_ub(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_commit(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCommit))
        self.on_type_commit(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeFree))
        self.on_type_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_get_elements(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGetElements))
        self.on_get_elements(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_pack(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiPack))
        self.on_pack(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_unpack(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiUnpack))
        self.on_unpack(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_pack_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiPackSize))
        self.on_pack_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_barrier(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiBarrier))
        self.on_barrier(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_bcast(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiBcast))
        self.on_bcast(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_gather(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGather))
        self.on_gather(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_gatherv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGatherv))
        self.on_gatherv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_scatter(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiScatter))
        self.on_scatter(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_scatterv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiScatterv))
        self.on_scatterv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_allgather(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAllgather))
        self.on_allgather(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_allgatherv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAllgatherv))
        self.on_allgatherv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_alltoall(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAlltoall))
        self.on_alltoall(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_alltoallv(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAlltoallv))
        self.on_alltoallv(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_reduce(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiReduce))
        self.on_reduce(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_op_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiOpCreate))
        self.on_op_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_op_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiOpFree))
        self.on_op_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_allreduce(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAllreduce))
        self.on_allreduce(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_reduce_scatter(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiReduceScatter))
        self.on_reduce_scatter(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_scan(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiScan))
        self.on_scan(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupSize))
        self.on_group_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_rank(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupRank))
        self.on_group_rank(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_translate_ranks(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupTranslateRanks))
        self.on_group_translate_ranks(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_compare(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupCompare))
        self.on_group_compare(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_group(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommGroup))
        self.on_comm_group(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_union(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupUnion))
        self.on_group_union(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_intersection(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupIntersection))
        self.on_group_intersection(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_difference(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupDifference))
        self.on_group_difference(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_incl(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupIncl))
        self.on_group_incl(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_excl(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupExcl))
        self.on_group_excl(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_range_incl(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupRangeIncl))
        self.on_group_range_incl(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_range_excl(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupRangeExcl))
        self.on_group_range_excl(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_group_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGroupFree))
        self.on_group_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSize))
        self.on_comm_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_rank(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommRank))
        self.on_comm_rank(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_compare(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommCompare))
        self.on_comm_compare(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_dup(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommDup))
        self.on_comm_dup(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommCreate))
        self.on_comm_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_split(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSplit))
        self.on_comm_split(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommFree))
        self.on_comm_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_test_inter(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommTestInter))
        self.on_comm_test_inter(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_remote_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommRemoteSize))
        self.on_comm_remote_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_remote_group(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommRemoteGroup))
        self.on_comm_remote_group(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_intercomm_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIntercommCreate))
        self.on_intercomm_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_intercomm_merge(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIntercommMerge))
        self.on_intercomm_merge(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_keyval_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiKeyvalCreate))
        self.on_keyval_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_keyval_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiKeyvalFree))
        self.on_keyval_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_attr_put(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAttrPut))
        self.on_attr_put(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_attr_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAttrGet))
        self.on_attr_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_attr_delete(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAttrDelete))
        self.on_attr_delete(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_topo_test(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTopoTest))
        self.on_topo_test(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartCreate))
        self.on_cart_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_dims_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiDimsCreate))
        self.on_dims_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_graph_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGraphCreate))
        self.on_graph_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_graphdims_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGraphdimsGet))
        self.on_graphdims_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_graph_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGraphGet))
        self.on_graph_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cartdim_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartdimGet))
        self.on_cartdim_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartGet))
        self.on_cart_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_rank(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartRank))
        self.on_cart_rank(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_coords(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartCoords))
        self.on_cart_coords(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_graph_neighbors_count(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGraphNeighborsCount))
        self.on_graph_neighbors_count(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_graph_neighbors(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGraphNeighbors))
        self.on_graph_neighbors(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_shift(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartShift))
        self.on_cart_shift(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_sub(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartSub))
        self.on_cart_sub(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_cart_map(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCartMap))
        self.on_cart_map(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_graph_map(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGraphMap))
        self.on_graph_map(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_get_processor_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGetProcessorName))
        self.on_get_processor_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_get_version(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGetVersion))
        self.on_get_version(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_errhandler_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiErrhandlerCreate))
        self.on_errhandler_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_errhandler_set(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiErrhandlerSet))
        self.on_errhandler_set(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_errhandler_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiErrhandlerGet))
        self.on_errhandler_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_errhandler_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiErrhandlerFree))
        self.on_errhandler_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_error_string(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiErrorString))
        self.on_error_string(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_error_class(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiErrorClass))
        self.on_error_class(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_wtime(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWtime))
        self.on_wtime(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_wtick(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWtick))
        self.on_wtick(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_init(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInit))
        self.on_init(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_finalize(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFinalize))
        self.on_finalize(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_initialized(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInitialized))
        self.on_initialized(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_abort(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAbort))
        self.on_abort(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_close_port(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiClosePort))
        self.on_close_port(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_accept(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommAccept))
        self.on_comm_accept(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_connect(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommConnect))
        self.on_comm_connect(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_disconnect(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommDisconnect))
        self.on_comm_disconnect(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_get_parent(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommGetParent))
        self.on_comm_get_parent(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_join(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommJoin))
        self.on_comm_join(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_spawn(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSpawn))
        self.on_comm_spawn(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_spawn_multiple(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSpawnMultiple))
        self.on_comm_spawn_multiple(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_lookup_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiLookupName))
        self.on_lookup_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_open_port(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiOpenPort))
        self.on_open_port(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_publish_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiPublishName))
        self.on_publish_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_unpublish_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiUnpublishName))
        self.on_unpublish_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_accumulate(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAccumulate))
        self.on_accumulate(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGet))
        self.on_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_put(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiPut))
        self.on_put(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_complete(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinComplete))
        self.on_win_complete(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinCreate))
        self.on_win_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_fence(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinFence))
        self.on_win_fence(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinFree))
        self.on_win_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_get_group(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinGetGroup))
        self.on_win_get_group(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_lock(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinLock))
        self.on_win_lock(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_post(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinPost))
        self.on_win_post(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_start(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinStart))
        self.on_win_start(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_test(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinTest))
        self.on_win_test(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_unlock(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinUnlock))
        self.on_win_unlock(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_wait(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinWait))
        self.on_win_wait(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_alltoallw(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAlltoallw))
        self.on_alltoallw(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_exscan(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiExscan))
        self.on_exscan(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_add_error_class(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAddErrorClass))
        self.on_add_error_class(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_add_error_code(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAddErrorCode))
        self.on_add_error_code(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_add_error_string(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAddErrorString))
        self.on_add_error_string(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_call_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommCallErrhandler))
        self.on_comm_call_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_create_keyval(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommCreateKeyval))
        self.on_comm_create_keyval(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_delete_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommDeleteAttr))
        self.on_comm_delete_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_free_keyval(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommFreeKeyval))
        self.on_comm_free_keyval(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_get_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommGetAttr))
        self.on_comm_get_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_get_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommGetName))
        self.on_comm_get_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_set_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSetAttr))
        self.on_comm_set_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_set_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSetName))
        self.on_comm_set_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_call_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileCallErrhandler))
        self.on_file_call_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_grequest_complete(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGrequestComplete))
        self.on_grequest_complete(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_grequest_start(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGrequestStart))
        self.on_grequest_start(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_init_thread(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInitThread))
        self.on_init_thread(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_is_thread_main(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIsThreadMain))
        self.on_is_thread_main(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_query_thread(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiQueryThread))
        self.on_query_thread(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_status_set_cancelled(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiStatusSetCancelled))
        self.on_status_set_cancelled(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_status_set_elements(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiStatusSetElements))
        self.on_status_set_elements(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_keyval(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateKeyval))
        self.on_type_create_keyval(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_delete_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeDeleteAttr))
        self.on_type_delete_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_dup(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeDup))
        self.on_type_dup(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_free_keyval(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeFreeKeyval))
        self.on_type_free_keyval(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_get_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeGetAttr))
        self.on_type_get_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_get_contents(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeGetContents))
        self.on_type_get_contents(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_get_envelope(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeGetEnvelope))
        self.on_type_get_envelope(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_get_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeGetName))
        self.on_type_get_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_set_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeSetAttr))
        self.on_type_set_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_set_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeSetName))
        self.on_type_set_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_match_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeMatchSize))
        self.on_type_match_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_call_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinCallErrhandler))
        self.on_win_call_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_create_keyval(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinCreateKeyval))
        self.on_win_create_keyval(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_delete_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinDeleteAttr))
        self.on_win_delete_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_free_keyval(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinFreeKeyval))
        self.on_win_free_keyval(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_get_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinGetAttr))
        self.on_win_get_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_get_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinGetName))
        self.on_win_get_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_set_attr(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinSetAttr))
        self.on_win_set_attr(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_set_name(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinSetName))
        self.on_win_set_name(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_alloc_mem(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiAllocMem))
        self.on_alloc_mem(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_create_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommCreateErrhandler))
        self.on_comm_create_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_get_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommGetErrhandler))
        self.on_comm_get_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_comm_set_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiCommSetErrhandler))
        self.on_comm_set_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_create_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileCreateErrhandler))
        self.on_file_create_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetErrhandler))
        self.on_file_get_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_set_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSetErrhandler))
        self.on_file_set_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_finalized(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFinalized))
        self.on_finalized(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_free_mem(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFreeMem))
        self.on_free_mem(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_get_address(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiGetAddress))
        self.on_get_address(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_create(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoCreate))
        self.on_info_create(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_delete(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoDelete))
        self.on_info_delete(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_dup(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoDup))
        self.on_info_dup(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_free(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoFree))
        self.on_info_free(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_get(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoGet))
        self.on_info_get(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_get_nkeys(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoGetNkeys))
        self.on_info_get_nkeys(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_get_nthkey(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoGetNthkey))
        self.on_info_get_nthkey(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_get_valuelen(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoGetValuelen))
        self.on_info_get_valuelen(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_info_set(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiInfoSet))
        self.on_info_set(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_pack_external(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiPackExternal))
        self.on_pack_external(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_pack_external_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiPackExternalSize))
        self.on_pack_external_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_request_get_status(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRequestGetStatus))
        self.on_request_get_status(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_darray(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateDarray))
        self.on_type_create_darray(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_hindexed(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateHindexed))
        self.on_type_create_hindexed(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_hvector(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateHvector))
        self.on_type_create_hvector(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_indexed_block(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateIndexedBlock))
        self.on_type_create_indexed_block(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_resized(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateResized))
        self.on_type_create_resized(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_struct(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateStruct))
        self.on_type_create_struct(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_create_subarray(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeCreateSubarray))
        self.on_type_create_subarray(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_get_extent(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeGetExtent))
        self.on_type_get_extent(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_type_get_true_extent(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiTypeGetTrueExtent))
        self.on_type_get_true_extent(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_unpack_external(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiUnpackExternal))
        self.on_unpack_external(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_create_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinCreateErrhandler))
        self.on_win_create_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_get_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinGetErrhandler))
        self.on_win_get_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_win_set_errhandler(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiWinSetErrhandler))
        self.on_win_set_errhandler(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_open(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileOpen))
        self.on_file_open(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_close(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileClose))
        self.on_file_close(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_delete(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileDelete))
        self.on_file_delete(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_set_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSetSize))
        self.on_file_set_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_preallocate(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFilePreallocate))
        self.on_file_preallocate(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_size(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetSize))
        self.on_file_get_size(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_group(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetGroup))
        self.on_file_get_group(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_amode(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetAmode))
        self.on_file_get_amode(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_set_info(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSetInfo))
        self.on_file_set_info(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_info(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetInfo))
        self.on_file_get_info(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_set_view(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSetView))
        self.on_file_set_view(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_view(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetView))
        self.on_file_get_view(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_at(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAt))
        self.on_file_read_at(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_at_all(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAtAll))
        self.on_file_read_at_all(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_at(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAt))
        self.on_file_write_at(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_at_all(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAtAll))
        self.on_file_write_at_all(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_iread_at(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileIreadAt))
        self.on_file_iread_at(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_iwrite_at(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileIwriteAt))
        self.on_file_iwrite_at(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileRead))
        self.on_file_read(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_all(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAll))
        self.on_file_read_all(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWrite))
        self.on_file_write(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_all(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAll))
        self.on_file_write_all(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_iread(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileIread))
        self.on_file_iread(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_iwrite(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileIwrite))
        self.on_file_iwrite(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_seek(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSeek))
        self.on_file_seek(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_position(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetPosition))
        self.on_file_get_position(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_byte_offset(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetByteOffset))
        self.on_file_get_byte_offset(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_shared(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadShared))
        self.on_file_read_shared(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_shared(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteShared))
        self.on_file_write_shared(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_iread_shared(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileIreadShared))
        self.on_file_iread_shared(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_iwrite_shared(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileIwriteShared))
        self.on_file_iwrite_shared(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_ordered(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadOrdered))
        self.on_file_read_ordered(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_ordered(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteOrdered))
        self.on_file_write_ordered(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_seek_shared(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSeekShared))
        self.on_file_seek_shared(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_position_shared(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetPositionShared))
        self.on_file_get_position_shared(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_at_all_begin(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAtAllBegin))
        self.on_file_read_at_all_begin(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_at_all_end(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAtAllEnd))
        self.on_file_read_at_all_end(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_at_all_begin(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAtAllBegin))
        self.on_file_write_at_all_begin(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_at_all_end(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAtAllEnd))
        self.on_file_write_at_all_end(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_all_begin(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAllBegin))
        self.on_file_read_all_begin(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_all_end(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadAllEnd))
        self.on_file_read_all_end(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_all_begin(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAllBegin))
        self.on_file_write_all_begin(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_all_end(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteAllEnd))
        self.on_file_write_all_end(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_ordered_begin(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadOrderedBegin))
        self.on_file_read_ordered_begin(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_read_ordered_end(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileReadOrderedEnd))
        self.on_file_read_ordered_end(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_ordered_begin(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteOrderedBegin))
        self.on_file_write_ordered_begin(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_write_ordered_end(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileWriteOrderedEnd))
        self.on_file_write_ordered_end(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_type_extent(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetTypeExtent))
        self.on_file_get_type_extent(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_register_datarep(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiRegisterDatarep))
        self.on_register_datarep(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_set_atomicity(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSetAtomicity))
        self.on_file_set_atomicity(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_get_atomicity(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileGetAtomicity))
        self.on_file_get_atomicity(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_file_sync(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFileSync))
        self.on_file_sync(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iotest(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIotest))
        self.on_iotest(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iowait(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIowait))
        self.on_iowait(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iotestall(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIotestall))
        self.on_iotestall(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iowaitall(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIowaitall))
        self.on_iowaitall(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iotestany(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIotestany))
        self.on_iotestany(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iowaitany(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIowaitany))
        self.on_iowaitany(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iowaitsome(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIowaitsome))
        self.on_iowaitsome(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_iotestsome(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiIotestsome))
        self.on_iotestsome(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_function_enter(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFuncCall))
        self.on_function_enter(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1

    def __on_function_exit(self, data, thread, cpu_time, wall_time, perf_info, userdata):
        dp = cast(data, POINTER(DumpiFuncCall))
        self.on_function_exit(dp.contents, thread, cpu_time, wall_time, perf_info)
        return 1
