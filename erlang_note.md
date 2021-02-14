

### switch modules dynamically
Reference:
- How: https://stackoverflow.com/questions/34579048/how-to-call-a-module-dynamically-in-erlang
- Reference_manual: https://erlang.org/doc/reference_manual/modules.html#module_info-0-and-module_info-1-functions
- Man: http://erlang.org/doc/man/io_lib.html#print-1
- Online erlang compiler: https://repl.it/languages/erlang?v2=1
```erlang
-module(main).
-export([start/0]).

-define(PROD1, "1").
-define(PROD2, "2").

choose_module(?PROD1) -> array;
choose_module(?PROD2) -> dict.

execute(Type, Data) ->
  Mod = choose_module(Type),
  ModName = io_lib:print(Mod:module_info(module)),
  DataSize = io_lib:print(Mod:size(Data)),
  DataContent = io_lib:format("~p", [Data]),
  io:fwrite(["Product", Type, " uses ", ModName, "\n"]),
  io:fwrite(["Data size=", DataSize, "\n"]),
  io:fwrite(["Data=", DataContent, "\n"]).

start() -> 
  Data = [{"123", "456"}],
  execute(?PROD1, array:from_list(Data)),
  execute(?PROD2, dict:from_list(Data)).
```
Output:
```
 run-project
Product1 uses array
Data size=1
Data={array,1,10,undefined,
       {{"123","456"},
        undefined,undefined,undefined,undefined,undefined,undefined,undefined,
        undefined,undefined}}
Product2 uses dict
Data size=1
Data={dict,1,16,16,8,80,48,
      {[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]},
      {{[],[],[],[],[],[["123",52,53,54]],[],[],[],[],[],[],[],[],[],[]}}}
```
