#include "mixer.hpp"
#include <algorithm>
#ifdef BUILD_WRAPPER

Mixer::Mixer(WAVEFORMATEX fmt) : format(fmt) {}

Mixer::~Mixer() {}

void Mixer::SubmitPacket(UINT64, float *data, UINT32 num_frames)
{
	auto lock = buffer_section.lock();
	buffer.insert(buffer.end(), data, data + num_frames * format.nChannels);
}

size_t Mixer::Read(float *out, size_t frames)
{
	auto lock = buffer_section.lock();
	size_t samples = frames * format.nChannels;
	size_t available = std::min(samples, buffer.size());
	for (size_t i = 0; i < available; ++i) {
		out[i] = buffer.front();
		buffer.pop_front();
	}
	return available / format.nChannels;
}

#endif

