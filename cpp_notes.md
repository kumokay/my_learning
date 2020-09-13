# Just some cpp notes

## Structured binding declaration
- https://en.cppreference.com/w/cpp/language/structured_binding
```cpp
// https://coliru.stacked-crooked.com/a/3eb42da341156f95
#include <iostream>
#include <string>
#include <vector>

struct Data {
  Data(std::string s) : value(std::move(s)) {}
  Data(const Data& src) : value(src.value) { 
    std::cout << "copy data:" << value << std::endl;
  }
  Data(Data&& src) : value(std::move(src.value)) { 
    std::cout << "move data:" << value << std::endl;
  }
  
  friend std::ostream& operator<<(std::ostream& os, const Data& data) {
    os << data.value;
    return os;
  }

  std::string value;
};

int main()
{
  std::pair<Data, Data> p{Data("111"), Data("222")};
  {
    std::cout << "======" << std::endl;
    auto& [x,y] = p;
    std::cout << x << "," << y << std::endl;
    std::cout << "p=" << p.first << "," << p.second << std::endl;
  }
  {
    std::cout << "======" << std::endl;
    auto&& [x,y] = std::move(p);
    std::cout << x << "," << y << std::endl;
    std::cout << "p=" << p.first << "," << p.second << std::endl;
  }
  {
    std::cout << "======" << std::endl;
    auto [x,y] = std::move(p);
    std::cout << x << "," << y << std::endl;
    std::cout << "p=" << p.first << "," << p.second << std::endl;
  }
}
```


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
