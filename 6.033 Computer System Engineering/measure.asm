/*
procedure MEASURE(func)
    start <- GET_TIME(SECONDS)
    func()
    end <- GET_TIME(SECONDS)
    return end - start


processure GET_TIME(units)
    time <- CLOCK
    time <- CONVERTS_TO_UNITS(time, units)
    return time
*/

STORE R1, SP
ADD 4, SP
STORE R2, SP
ADD 4, SP
MOV SECONDS, R1
STORE R1, SP
ADD 4, SP
MOV 148, R1