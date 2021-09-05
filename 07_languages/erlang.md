

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

set_enum_value(EnumName) ->
  Value = case EnumName of
    red -> "red";
    blue -> "blue";
    green -> "green"
  end,
  Value.

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
  execute(?PROD2, dict:from_list(Data)),
  io:fwrite([set_enum_value(red), "\n"]).
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

# Practice
## Functions
```erlang
-module(main).
-export([start/0]).

same(A, A) ->
  true;
same(A, [Head | Tail]) ->
  IsHeadSame = same(A, Head),
  if Tail =/= [] -> same(A, Tail) and IsHeadSame
   ; true -> IsHeadSame
  end;
same(_, _) ->
  false.

same([Head | Tail]) ->
  same(Head, Tail);
same(X) ->
  if is_tuple(X) -> same(tuple_to_list(X))
   ; true -> throw(error("cannot handle this type."))
  end.

execute() ->
  Pairs = [{"a", [97]}, {8#17, 16#F}, {<<"a">>, 97}],
  [
    [same(A, B) || {A, B} <- Pairs],
    same([8#17, 16#F, 15]),
    same({8#17, 16#F, 15}),
    same([<<"a">>, 97, "a"]),
    same([<<"a">>, <<97>>]),
    same([<<"ab">>, <<97, 98>>, <<"a", "b">>]),
    same(["ab", [97, 98]])
    %% same(1234) %% cannot handle type
  ].

%% main
start() ->
  Fn = fun(I, X) -> io:fwrite(io_lib:format("~p: ~p\n", [I, X])) end,
  Result = execute(),
  Indices = lists:seq(1, length(Result)),
  [Fn(I, X) || {I, X} <- lists:zip(Indices, Result)].
```
Output
```
-module(main).
-export([start/0]).

same(A, A) ->
  true;
same(A, [Head | Tail]) ->
  IsHeadSame = same(A, Head),
  if Tail =/= [] -> same(A, Tail) and IsHeadSame
   ; true -> IsHeadSame
  end;
same(_, _) ->
  false.

same([Head | Tail]) ->
  same(Head, Tail);
same(X) ->
  if is_tuple(X) -> same(tuple_to_list(X))
   ; true -> throw(error("cannot handle this type."))
  end.

execute() ->
  Pairs = [{"a", [97]}, {8#17, 16#F}, {<<"a">>, 97}],
  [
    [same(A, B) || {A, B} <- Pairs],
    same([8#17, 16#F, 15]),
    same({8#17, 16#F, 15}),
    same([<<"a">>, 97, "a"]),
    same([<<"a">>, <<97>>]),
    same([<<"ab">>, <<97, 98>>, <<"a", "b">>]),
    same(["ab", [97, 98]])
    %% same(1234) %% cannot handle type
  ].

%% main
start() ->
  Fn = fun(I, X) -> io:fwrite(io_lib:format("~p: ~p\n", [I, X])) end,
  Result = execute(),
  Indices = lists:seq(1, length(Result)),
  [Fn(I, X) || {I, X} <- lists:zip(Indices, Result)].
```
## Lists
```erlang
-module(main).
-export([start/0]).

combine(A, B) -> 
  case {A rem 2, B rem 2} of
    {0, 1} -> A;
    {1, 0} -> B;
    _ -> A + B
  end.

execute() ->
  List = [1, 2, 3, 4, 5],
  FnDouble = fun(X) -> 2*X end,
  FnIsEven = fun(X) -> X rem 2 =:= 0 end,
  FnDivideIfEven = fun(X) -> 
      if 
        X rem 2 =:= 0 -> {true, X div 2};
        true -> false
      end
    end,
  FnCombine = fun(A, B) -> combine(A, B) end,
  FnSideEffect = fun(_) -> io:fwrite("side effect\n") end,
  [
    lists:map(FnDouble, List),
    lists:filter(FnIsEven, List),
    lists:filtermap(FnDivideIfEven, List),
    lists:foldl(fun(X, Sum) -> X + Sum end, 0, List),
    lists:foldr(fun(X, Sum) -> X + Sum end, 1, List),
    lists:zipwith(FnCombine, [1, 2, 3, 4], [2, 3, 5, 6]),
    lists:foreach(FnSideEffect, List)
  ].
  
%% main
start() ->
  Fn = fun(I, X) -> io:fwrite(io_lib:format("~p: ~p\n", [I, X])) end,
  Result = execute(),
  Indices = lists:seq(1, length(Result)),
  [Fn(I, X) || {I, X} <- lists:zip(Indices, Result)].
```
Output
```
> run-project
side effect
side effect
side effect
side effect
side effect
1: [2,4,6,8,10]
2: [2,4]
3: [1,2]
4: 15
5: 16
6: [2,2,8,10]
7: ok
```
