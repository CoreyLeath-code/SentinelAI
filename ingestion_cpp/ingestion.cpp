#include <vector>
#include <algorithm>

std::vector<float> process(std::vector<float> input) {
    std::transform(input.begin(), input.end(), input.begin(),
        [](float x) { return x * 1.1f; });
    return input;
}
