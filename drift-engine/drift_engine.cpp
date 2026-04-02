// drift-engine/drift_engine.cpp
// Reads JSON from stdin: {"expected": [...], "actual": [...]}
// Writes JSON to stdout: {"psi": <float>, "ks_stat": <float>, "drift_detected": <bool>}
#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <sstream>
#include <string>

// ---------------------------------------------------------------------------
// Statistics helpers
// ---------------------------------------------------------------------------

double calculate_psi(const std::vector<double>& expected,
                     const std::vector<double>& actual) {
    double psi = 0.0;
    for (size_t i = 0; i < expected.size() && i < actual.size(); ++i) {
        if (expected[i] <= 0.0 || actual[i] <= 0.0)
            continue;
        psi += (actual[i] - expected[i]) * std::log(actual[i] / expected[i]);
    }
    return psi;
}

// Kolmogorov-Smirnov statistic (max absolute difference of CDFs)
double calculate_ks(const std::vector<double>& expected,
                    const std::vector<double>& actual) {
    double exp_sum = std::accumulate(expected.begin(), expected.end(), 0.0);
    double act_sum = std::accumulate(actual.begin(), actual.end(), 0.0);
    double ks = 0.0;
    double cdf_exp = 0.0;
    double cdf_act = 0.0;
    for (size_t i = 0; i < expected.size() && i < actual.size(); ++i) {
        cdf_exp += (exp_sum > 0.0 ? expected[i] / exp_sum : 0.0);
        cdf_act += (act_sum > 0.0 ? actual[i] / act_sum : 0.0);
        double diff = std::fabs(cdf_exp - cdf_act);
        if (diff > ks)
            ks = diff;
    }
    return ks;
}

// ---------------------------------------------------------------------------
// Minimal JSON helpers (no external deps)
// ---------------------------------------------------------------------------

// Parse a JSON array of doubles: [1.0, 2.0, ...]
std::vector<double> parse_array(const std::string& json, const std::string& key) {
    std::vector<double> result;
    std::string search = "\"" + key + "\"";
    size_t pos = json.find(search);
    if (pos == std::string::npos)
        return result;
    pos = json.find('[', pos);
    if (pos == std::string::npos)
        return result;
    size_t end = json.find(']', pos);
    if (end == std::string::npos)
        return result;
    std::string arr = json.substr(pos + 1, end - pos - 1);
    std::stringstream ss(arr);
    std::string token;
    while (std::getline(ss, token, ',')) {
        try {
            result.push_back(std::stod(token));
        } catch (...) {}
    }
    return result;
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

int main() {
    std::string line, input;
    while (std::getline(std::cin, line))
        input += line;

    std::vector<double> expected = parse_array(input, "expected");
    std::vector<double> actual   = parse_array(input, "actual");

    if (expected.empty() || actual.empty()) {
        std::cout << "{\"error\": \"invalid input\"}" << std::endl;
        return 1;
    }

    double psi    = calculate_psi(expected, actual);
    double ks     = calculate_ks(expected, actual);
    bool   drift  = psi > 0.2 || ks > 0.1;

    std::cout << "{"
              << "\"psi\": "    << psi    << ", "
              << "\"ks_stat\": " << ks    << ", "
              << "\"drift_detected\": " << (drift ? "true" : "false")
              << "}" << std::endl;
    return 0;
}
