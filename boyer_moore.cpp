// dependency pybind needs to be installed to build. Installation using pip or brew recommended
// also needs CMake or other library managers to be built
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <vector>
#include <cctype>  // for std::tolower

namespace py = pybind11;

std::vector<int> preprocessBadCharHeuristic(const std::string& pattern) {
    int NO_OF_CHARS = 256;
    std::vector<int> badChar(NO_OF_CHARS, -1);

    for (int i = 0; i < pattern.size(); ++i)
        badChar[(int) pattern[i]] = i;

    return badChar;
}

std::vector<int> searchBoyerMoore(const std::string& text, const std::string& pattern) {
    std::vector<int> badChar = preprocessBadCharHeuristic(pattern);
    int m = pattern.size();
    int n = text.size();

    std::vector<int> occurrences;

    int s = 0; // s counts shifting of the pattern
    int shiftcount = 0;
    while (s <= (n - m)) {
        int j = m - 1;

        while (j >= 0 && std::tolower(pattern[j]) == std::tolower(text[s + j]))
            j--;

        if (j < 0) {
            // Pattern occurs at shift = s
            occurrences.push_back(s);

            // Is end of pattern? 1 to exit loop, if not skip lenght of pattern
            s += (s + m < n) ? m - badChar[text[s + m]] : 1;
            shiftcount++;
        } else {
            s += std::max(1, j - badChar[text[s + j]]);
            shiftcount++;
        }
    }

    std::cout << "Shiftcount: " << shiftcount << std::endl;

    return occurrences;
}

PYBIND11_MODULE(libboyer_moore, m) {
    m.doc() = "Boyer-Moore algorithm with bad character heuristic";
    m.def("searchBoyerMoore", &searchBoyerMoore, "Search for all occurrences of a pattern in text using Boyer-Moore");
    m.def("preprocessBadCharHeuristic", &preprocessBadCharHeuristic, "Preprocess bad character heuristic");
}


