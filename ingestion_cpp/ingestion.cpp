#include <cassert>
#include <vector>

extern double calculate_psi(const std::vector<double>&, const std::vector<double>&);

int main() {
    std::vector<double> baseline = {0.25,0.25,0.25,0.25};
    std::vector<double> current  = {0.25,0.25,0.25,0.25};

    double psi = calculate_psi(baseline, current);
    assert(psi < 0.01);

    return 0;
}
