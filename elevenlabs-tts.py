from elevenlabs import voices, generate, play

voices = voices()
for voice in voices:
  print(voice)
  audio = generate(text="Hello there!", voice=voice)
  play(audio)
