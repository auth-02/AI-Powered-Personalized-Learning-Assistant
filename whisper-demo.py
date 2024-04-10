import whisperx


def transcribe_audio(audio_file, device="cpu", batch_size=2, compute_type="int8"):
    
    options = {
    
    "max_new_tokens": None,
    "clip_timestamps": None,
    "hallucination_silence_threshold": None,
    }
    
    audio = whisperx.load_audio(audio_file)
    # model = whisperx.load_model("base", device, compute_type=compute_type)
    model = whisperx.load_model("base", device, compute_type=compute_type,asr_options=options)

    result = model.transcribe(audio, batch_size=batch_size)
    return result



audio_file = "temp_video.mp4"
transcription_result = transcribe_audio(audio_file)
print(transcription_result["segments"])