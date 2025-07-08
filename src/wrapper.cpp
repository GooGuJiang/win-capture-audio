#include "audio-capture-helper.hpp"
#include "mixer.hpp"
#include <memory>
#include <limits.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef void *WCA_Handle;

static WAVEFORMATEX make_format(unsigned int sample_rate, unsigned short channels)
{
	WAVEFORMATEX fmt{};
	fmt.wFormatTag = WAVE_FORMAT_IEEE_FLOAT;
	fmt.nChannels = channels;
	fmt.nSamplesPerSec = sample_rate;
	fmt.nBlockAlign = channels * sizeof(float);
	fmt.nAvgBytesPerSec = sample_rate * fmt.nBlockAlign;
	fmt.wBitsPerSample = CHAR_BIT * sizeof(float);
	fmt.cbSize = 0;
	return fmt;
}

struct CaptureInstance {
	Mixer mixer;
	std::unique_ptr<AudioCaptureHelper> helper;
	CaptureInstance(unsigned int pid, unsigned int rate, unsigned short ch)
		: mixer(make_format(rate, ch)),
		  helper(std::make_unique<AudioCaptureHelper>(&mixer, mixer.GetFormat(), pid))
	{
	}
};

__declspec(dllexport) WCA_Handle sca_create_capture(unsigned int pid, unsigned int sample_rate,
						    unsigned short channels)
{
	try {
		auto inst = new CaptureInstance(pid, sample_rate, channels);
		return inst;
	} catch (...) {
		return nullptr;
	}
}

__declspec(dllexport) unsigned int sca_read_audio_frames(WCA_Handle h, float *buffer,
							 unsigned int frames)
{
	if (!h || !buffer)
		return 0;
	auto inst = static_cast<CaptureInstance *>(h);
	return static_cast<unsigned int>(inst->mixer.Read(buffer, frames));
}

__declspec(dllexport) void sca_destroy_capture(WCA_Handle h)
{
	auto inst = static_cast<CaptureInstance *>(h);
	delete inst;
}

#ifdef __cplusplus
}
#endif
