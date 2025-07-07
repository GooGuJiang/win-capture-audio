#pragma once

#include <thread>
#ifdef BUILD_WRAPPER
#include <deque>
#else
#include <queue>
#include <vector>
#endif

#include <windows.h>
#include <wil/resource.h>

#include "common.hpp"
#ifndef BUILD_WRAPPER
#include <obs.h>
#endif

namespace MixerEvents {
enum MixerEvents {
	Shutdown = WM_USER,
	Tick,
};
}

#ifdef BUILD_WRAPPER

class Mixer {
private:
	WAVEFORMATEX format;
	wil::critical_section buffer_section;
	std::deque<float> buffer;

public:
	Mixer(WAVEFORMATEX format);
	~Mixer();

	void SubmitPacket(UINT64 timestamp, float *data, UINT32 num_frames);
	size_t Read(float *data, size_t frames);
	WORD Channels() const { return format.nChannels; }
	WAVEFORMATEX GetFormat() const { return format; }
};

#else

class Mixer {
private:
	static const UINT64 ms_in_ts = 10000;

	static const UINT64 cutoff_start = 120 * ms_in_ts;
	static const UINT64 cutoff_end = 40 * ms_in_ts;

	static const DWORD tick_interval = 10;

	obs_source_t *source;

	std::thread worker_thread;
	DWORD worker_tid;
	wil::unique_event worker_ready{wil::EventOptions::ManualReset};

	HANDLE timer;

	WAVEFORMATEX format;

	wil::critical_section input_section;
	std::queue<std::tuple<UINT64, std::vector<float>>> input_queue;

	UINT64 mix_timestamp;
	std::vector<float> mix;

	template<typename T> static T RoundToNearest(T x, T m);

	UINT64 GetCurrentTimestamp();
	std::size_t DurationToFrames(UINT64 duration);
	UINT64 FramesToDuration(std::size_t frames);

	std::size_t TimestampToMixOffset(UINT64 timestamp);
	std::tuple<std::size_t, std::size_t> CalculateCutoff(UINT64 timestamp);

	void ProcessInput(UINT64 input_timestamp, std::vector<float> &input_buffer);
	void ProcessInput();

	void Tick();
	void Run();

public:
	void SubmitPacket(UINT64 timestamp, float *data, UINT32 num_frames);

	Mixer(obs_source_t *source, WAVEFORMATEX format);
	~Mixer();
};

#endif
