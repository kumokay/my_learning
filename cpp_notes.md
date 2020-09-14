# CPP Designs

## Traits and policies
- A trait is a class or class template that characterizes a type, possibly a template parameter.
- A policy is a class or class template that defines an interface as a service to other classes.
```cpp
// https://coliru.stacked-crooked.com/a/206cf001971ed6ed
#include <iostream>
#include <string>

class Mage;
class Priest;
class Paladin;

template <typename TClass>
struct ClassTraits;

template <>
struct ClassTraits<Mage> {
  static constexpr int kMaxHp = 50;
  static constexpr int kDefense = 5;
  static constexpr int kDamage = 40;
};

template <>
struct ClassTraits<Priest> {
  static constexpr int kMaxHp = 70;
  static constexpr int kDefense = 0;
  static constexpr int kDamage = 10;
};

template <>
struct ClassTraits<Paladin> {
  static constexpr int kMaxHp = 80;
  static constexpr int kDefense = 10;
  static constexpr int kDamage = 20;
};

struct AttackPolicy {
  template <typename T, typename U>
  static void action(T& attacker, U& victim, int points) {
    victim.takeDamage(points);
  }
};

struct HealPolicy {
  template <typename T, typename U>
  static void action(T& healer, U& player, int points) {
    player.restoreHp(points);
  }
};

struct AttackAndSelfHealPolicy {
  template <typename T, typename U>
  static void action(T& attacker, U& victim, int points) {
    int damage = victim.takeDamage(points);
    attacker.restoreHp(damage * 0.3);
  }
};

template<typename TTraits, typename TPolicy>
class Player {
 public:
  explicit Player(std::string name)
  : name_(std::move(name)), 
    hp_(TTraits::kMaxHp) {}
  
  bool isAlive() const {
    if (hp_ > 0) {
      std::cout << name_ << " has " << hp_ << " hp!" << std::endl;
      return true;
    }
    std::cout << name_ << " is dead!" << std::endl;
    return false;
  }
  
  int takeDamage(int points) {
    auto diff = std::max(0, points - TTraits::kDefense);
    hp_ -= diff;
    std::cout << name_ << " took " << diff << " damage!" << std::endl;
    isAlive();
    return diff;
  }
  
  void restoreHp(int points) {
    auto diff = std::min(TTraits::kMaxHp - hp_, points);
    std::cout << name_ << " restored " << diff << " hp!" << std::endl;
    hp_ += diff;
  }
  
  template <typename TPlayer>
  void action(TPlayer& player) {
    if (!isAlive() || !player.isAlive()) {
      std::cerr << name_ << " cannot do anything to " << player.name() << std::endl;
      return;
    }
    TPolicy::action(*this, player, TTraits::kDamage);
  }
  
  const std::string& name() {
    return name_;
  }

 private:
  std::string name_;
  int hp_;
  int mp_;
};

class Mage : public Player<ClassTraits<Mage>, AttackPolicy> {
  using Player::Player;
};
class Paladin : public Player<ClassTraits<Paladin>, AttackAndSelfHealPolicy> {
  using Player::Player;
};
class Priest : public Player<ClassTraits<Priest>, HealPolicy> {
  using Player::Player;
};

int main()
{
  std::cout << "======setup" << std::endl;
  Mage mage("mage");
  Paladin paladin("paladin");
  Priest priest("priest");
  {
    std::cout << "======1" << std::endl;
    mage.action(paladin);
  }
  {
    std::cout << "======2" << std::endl;
    paladin.action(mage);
  }
  {
    std::cout << "======3" << std::endl;
    priest.action(mage);
  }
  {
    std::cout << "======4" << std::endl;
    mage.action(paladin);
  }
  {
    std::cout << "======5" << std::endl;
    paladin.action(mage);
  }
  {
    std::cout << "======6" << std::endl;
    priest.action(mage);
  }
  {
    std::cout << "======7" << std::endl;
    mage.action(paladin);
  }
  std::cout << "======teardown" << std::endl;
}
```

# CPP Features

## Reference declaration
- https://en.cppreference.com/w/cpp/language/reference
- Lvalue references can be used to alias an existing object (optionally with different cv-qualification)
- Rvalue references can be used to extend the lifetimes of temporary objects (note, lvalue references to const can extend the lifetimes of temporary objects too, but they are not modifiable through them)
```cpp
// https://coliru.stacked-crooked.com/a/9a2661443883ac9e
#include <iostream>
#include <string>
#include <vector>

struct Data {
  ~Data() {
    std::cout << "destroy data:" << value << std::endl;
  }
  Data(std::string s) : value(std::move(s)) {
    std::cout << "create data:" << value << std::endl;
  }
  Data(const Data& src) : value(src.value) { 
    std::cout << "copy data:" << value << std::endl;
  }
  Data(Data&& src) : value(std::move(src.value)) {
    std::cout << "move data:" << value << std::endl;
  }
  
  Data operator+(const Data& rhs)
  {
    return Data(value + rhs.value);
  }
  
  bool operator==(const Data& rhs) {
    return this->value == rhs.value;
  }

  friend std::ostream& operator<<(std::ostream& os, const Data& data) {
    os << data.value;
    return os;
  }

  std::string value;
};

Data& getRef() {
  static Data d{"static var"};
  return d;
}

Data& getDanglingRef() {
  Data d{"Dangling ref"};
  return d;
}

int main()
{
  std::cout << "======setup" << std::endl;
  Data d1{"111"}, d2{"222"};
  {
    std::cout << "======1" << std::endl;
    auto dv = d1 + d2;
  }
  {
    std::cout << "======2" << std::endl;
    const auto& dr = d1 + d2;
    // cannot bind non-const lvalue reference of type 'Data&' to an rvalue of type 'Data'
    // auto& dr2 = d1 + d2; 
  }
  {
    std::cout << "======3" << std::endl;
    auto&& dr = d1 + d2;
    dr.value += "modified";
    std::cout << dr.value << std::endl; 
  }
  {
    std::cout << "======4" << std::endl;
    auto& dr = getRef();
    std::cout << dr.value << std::endl; 
  }
  {
    std::cout << "======5" << std::endl;
    auto& dr = getDanglingRef();
    // Segmentation fault bc reads from a dangling reference
    // std::cout << dr.value; 
  }
  std::cout << "======teardown" << std::endl;
}
```

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
## Smart pointers
- share_ptr: https://en.cppreference.com/w/cpp/memory/shared_ptr
- unique_ptr: https://en.cppreference.com/w/cpp/memory/unique_ptr
```cpp
// https://coliru.stacked-crooked.com/a/30340b4613871824
#include <iostream>
#include <string>
#include <memory>

struct Data {
  ~Data() {
    std::cout << "destroy data:" << value << std::endl;
  }
  Data(std::string s) : value(std::move(s)) {
    std::cout << "create data:" << value << std::endl;
  }
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
  std::cout << "======setup" << std::endl;
  auto pu = std::make_unique<Data>("unique");
  auto ps = std::make_shared<Data>("shared");
  {
    std::cout << "======1" << std::endl;
    auto& prl = pu;
    std::cout << *prl << std::endl;
    // cannot copy unique ptr
    // auto pv = pu;
    auto&& prr = pu;
    std::cout << *prr << std::endl;
    auto pv = std::move(pu);
    std::cout << *pv << std::endl;
  }
  {
    std::cout << "======2" << std::endl;
    auto& prl = ps;
    std::cout << *prl << std::endl;
    auto&& prr = ps;
    std::cout << *prr << std::endl;
    auto pv1 = ps;
    std::cout << *pv1 << std::endl;
    auto pv2 = pv1;
    std::cout << *pv2 << std::endl;
  }
  std::cout << "======teardown" << std::endl;
}
```
