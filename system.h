#ifndef SYSTEM_H
#define SYSTEM_H

#define assert(condition, message) \
    if (!(condition)) __assert2(__FILE__, __LINE__, #condition, message)

#define assertf(condition, message, ...) \
    if (!(condition)) __assert2(__FILE__, __LINE__, #condition, message, __VA_ARGS__)

int __assert2(char * filename, int line, char * assertion, char * message, ...);
void sysWaitDrawSync();

#endif