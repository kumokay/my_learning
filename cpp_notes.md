# Just some cpp notes

## unordered_set
### emplace vs try_emplace
- emplace
  - Inserts a new element into the container constructed in-place with the given args if there is no element with the key in the container.
  - The element **may be constructed** even if there already is an element with the key in the container
- [try_emplace](https://en.cppreference.com/w/cpp/container/unordered_map/try_emplace)
  - If a key equivalent to k already exists in the container, does nothing. Otherwise, behaves like emplace except that the element is constructed as value_type
  - It will not move from rvalue arguments if the insertion does not happen
```cpp
// https://coliru.stacked-crooked.com/view?id=d154e50b95b3a4b5
#include <iostream>
#include <string>
 
#include <unordered_map>
#include <vector>

struct Data{
  Data(std::string&& s) : data(std::move(s)) {
      std::cout << "Data:" << data << std::endl;
  }  
  std::string data;
};

int main()
{
    using namespace std::literals;
    std::unordered_map<std::string, Data> m;
 
    std::vector<std::string> values{
        "aaa", 
        "bbb", 
        "ccc", 
        "Won't be construct", 
        "Constructed but won't be inserted"};

    m.try_emplace("a", std::move(values[0]));
    m.try_emplace("b", std::move(values[1]));
    m.try_emplace("c", std::move(values[2]));
    m.try_emplace("c", std::move(values[3]));
    m.emplace("c", std::move(values[4]));
 
    for (const auto& [k, v] : m) {
        std::cout << k << " => " << v.data << '\n';
    }
    for (auto& s : values) {
        std::cout << "s:" << s << std::endl;
    }
}
```
