// drift_engine.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

double calculate_mean(const std::vector<double>& data) {
    double sum = std::accumulate(data.begin(), data.end(), 0.0);
    return sum / data.size();
}

double calculate_variance(const std::vector<double>& data, double mean) {
    double variance = 0.0;
    for (double val : data) {
        variance += std::pow(val - mean, 2);
    }
    return variance / data.size();
}

// Population Stability Index (PSI)
double calculate_psi(const std::vector<double>& expected,
                     const std::vector<double>& actual) {

    double psi = 0.0;
    for (size_t i = 0; i < expected.size(); ++i) {
        if (expected[i] == 0 || actual[i] == 0)
            continue;

        psi += (actual[i] - expected[i]) *
               std::log(actual[i] / expected[i]);
    }
    return psi;
}

int main() {
    std::vector<double> baseline = {0.2, 0.3, 0.25, 0.25};
    std::vector<double> current  = {0.1, 0.35, 0.30, 0.25};

    double psi = calculate_psi(baseline, current);

    std::cout << "PSI Score: " << psi << std::endl;

    if (psi > 0.2)
        std::cout << "Drift Detected." << std::endl;
    else
        std::cout << "No Significant Drift." << std::endl;

    return 0;
}
