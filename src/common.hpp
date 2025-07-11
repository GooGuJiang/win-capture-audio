#pragma once

#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <stdio.h>
#include <stdint.h>

#ifndef BUILD_WRAPPER
#include <util/platform.h>
#include <obs.h>
#else
#include <stdarg.h>

enum { LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR };

inline static void blogva(int level, const char *format, va_list args)
{
	(void)level;
	vfprintf(stderr, format, args);
	fprintf(stderr, "\n");
}
#endif

#define do_log(level, format, ...) \
	do_log_source(level, "[win-capture-audio] (%s) " format, __func__, ##__VA_ARGS__)

inline static void do_log_source(int level, const char *format, ...)
{
	va_list args;
	va_start(args, format);

	blogva(level, format, args);

	va_end(args);
}

#define error(format, ...) do_log(LOG_ERROR, format, ##__VA_ARGS__)
#define warn(format, ...) do_log(LOG_WARNING, format, ##__VA_ARGS__)
#define info(format, ...) do_log(LOG_INFO, format, ##__VA_ARGS__)
#define debug(format, ...) do_log(LOG_DEBUG, format, ##__VA_ARGS__)