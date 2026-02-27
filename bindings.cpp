#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

std::vector<float> process(std::vector<float> input);

PYBIND11_MODULE(ingestion_cpp, m) {
    m.def("process", &process);
}
