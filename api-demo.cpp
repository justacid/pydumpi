#include <iostream>
#include <dumpi/libundumpi/libundumpi.h>

int message_count = 0;

int mpi_isend(const dumpi_isend *prm, uint16_t thread, const dumpi_time *cpu, 
              const dumpi_time *wall, const dumpi_perfinfo *perf, void *uarg) 
{
    message_count++;
    return 1;
}

int main(int argc, char** argv)
{
    if (argc != 2) {
        return 1;
    }

    libundumpi_callbacks cback;
    libundumpi_clear_callbacks(&cback);
    cback.on_isend = mpi_isend;

    auto profile = undumpi_open(argv[1]);
    undumpi_read_stream(profile, &cback, nullptr);
    undumpi_close(profile);

    std::cout << "ISend was called " << message_count << " times." << std::endl;

    return 0;
}
