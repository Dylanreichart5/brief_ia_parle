import pyaudio
import wave

chunk = 1024  # Taille de chaque échantillon audio
sample_format = pyaudio.paInt16  # Format d'échantillon audio
channels = 2  # Nombre de canaux audio (stéréo)
fs = 44100  # Fréquence d'échantillonnage (nombre d'échantillons par seconde)

# Initialisation de l'objet PyAudio
p = pyaudio.PyAudio()

# Ouverture du flux audio
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# Enregistrement audio
frames = []
print("Enregistrement en cours...")
while True:
    data = stream.read(chunk)
    frames.append(data)

    # Pour arrêter l'enregistrement, appuyez sur la touche 'q'
    if 'q' in input().lower():
        break

# Arrêt du flux audio
stream.stop_stream()
stream.close()

# Fermeture de l'objet PyAudio
p.terminate()

# Écriture des données audio en fichier .wav
wf = wave.open("enregistrement.wav", "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b"".join(frames))
wf.close()

print("Enregistrement terminé.")
