

### switch modules dynamically
Reference:
- How: https://stackoverflow.com/questions/34579048/how-to-call-a-module-dynamically-in-erlang
- Reference_manual: https://erlang.org/doc/reference_manual/modules.html#module_info-0-and-module_info-1-functions
- Man: http://erlang.org/doc/man/io_lib.html#print-1
- Online erlang compiler: https://repl.it/languages/erlang?v2=1
```
-module(main).
-export([start/0]).

-define(PROD1, "1").
-define(PROD2, "2").

choose_module(?PROD1) -> array;
choose_module(?PROD2) -> binary.

execute(Type) ->
  Mod = choose_module(Type),
  ModName = io_lib:print(Mod:module_info(module)),
  io:fwrite(["Product", Type, " uses ", ModName, "\n"]).

start() -> 
  execute(?PROD1),
  execute(?PROD2).
```
