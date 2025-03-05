# # # import numpy as np
# # # from scipy.io import wavfile
# # # import io
# # # import base64

# # # # Define musical parameters
# # # SAMPLE_RATE = 44100
# # # NOTE_DURATION = 0.5  # seconds
# # # FREQUENCIES = {
# # #     'a': 440.0,    # A4
# # #     'b': 493.88,   # B4
# # #     'c': 523.25,   # C5
# # #     'd': 587.33,   # D5
# # #     'e': 659.25,   # E5
# # #     'f': 698.46,   # F5
# # #     'g': 783.99,   # G5
# # #     'h':349.23,
# # #     'i':392.00,
# # #     'k':723.99,
# # #     'l':698.46,
# # #     'm':493.88,
# # #     'n':587.33,
# # #     'o':523.25,
# # #     'p':493.88,
# # #     'r':723.99,
# # #     'q':440.00,
# # #     's':493.88,
# # #     't':329.63,
# # #     'u':587.33,
# # #     'v':723.99,
# # #     'w':493.88,
# # #     'x':723.99,
# # #     'y':493.88,
# # #     'z':698.46


# # # }
 
# # # def generate_tone(frequency, duration):
# # #     t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
# # #     # Generate sine wave
# # #     tone = np.sin(2 * np.pi * frequency * t)
# # #     # Apply envelope to avoid clicks
# # #     envelope = np.exp(-t * 3)
# # #     return tone * envelope

# # # def generate_melody(username):
# # #     try:
# # #         # Convert username to lowercase and filter valid characters
# # #         username = username.lower()
# # #         melody = np.array([])
       
# # #         for char in username:
# # #             if char in FREQUENCIES:
# # #                 # Generate tone for each valid character
# # #                 tone = generate_tone(FREQUENCIES[char], NOTE_DURATION)
# # #                 melody = np.append(melody, tone)
# # #             else:
# # #                 # Use a rest (silence) for invalid characters
# # #                 silence = np.zeros(int(SAMPLE_RATE * NOTE_DURATION))
# # #                 melody = np.append(melody, silence)
       
# # #         # Normalize the melody
# # #         if len(melody) > 0:
# # #             melody = melody / np.max(np.abs(melody))
       
# # #         # Convert to 16-bit PCM
# # #         melody_int = np.int16(melody * 32767)
       
# # #         # Save to bytes buffer
# # #         buffer = io.BytesIO()
# # #         wavfile.write(buffer, SAMPLE_RATE, melody_int)
# # #         buffer.seek(0)
       
# # #         # Convert to base64 for sending to client
# # #         melody_base64 = base64.b64encode(buffer.read()).decode('utf-8')
       
# # #         return melody_base64
       
# # #     except Exception as e:
# # #         raise Exception(f"Failed to generate melody: {str(e)}")


 





# import numpy as np
# from scipy.io import wavfile
# import io
# import base64

# # Define musical parameters
# SAMPLE_RATE = 44100
# NOTE_DURATION = 0.5  # Increased duration for a smoother sound

# # Frequencies for notes (lower octaves for calming effect)
# frequencies = {
#     'C3': 130.81,
#     'D3': 146.83,
#     'E3': 164.81,
#     'F3': 174.61,
#     'G3': 196.00,
#     'A3': 220.00,
#     'B3': 246.94,
#     'C4': 261.63,
#     'D4': 293.66,
#     'E4': 329.63,
#     'F4': 349.23,
#     'G4': 392.00,
#     'A4': 440.00,
#     'B4': 493.88
# }

# # Map letters to notes (two letters per note)
# letter_to_note = {
#     'a': 'C3', 'b': 'C3',  # C3
#     'c': 'D3', 'd': 'D3',  # D3
#     'e': 'E3', 'f': 'E3',  # E3
#     'g': 'F3', 'h': 'F3',  # F3
#     'i': 'G3', 'j': 'G3',  # G3
#     'k': 'A3', 'l': 'A3',  # A3
#     'm': 'B3', 'n': 'B3',  # B3
#     'o': 'C4', 'p': 'C4',  # C4
#     'q': 'E4', 'r': 'D4',  # E4 and D4
#     's': 'F4', 't': 'E4',  # F4 and E4
#     'u': 'G4', 'v': 'G4',  # G4
#     'w': 'A4', 'x': 'C3',  # A4 and C3
#     'y': 'C4', 'z': 'F4'   # C4 and F4
# }

# # Function to generate a sine wave for a given frequency and duration
# def generate_sine_wave(frequency, duration):
#     t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
#     wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude of 0.5
#     return wave

# # Function to create a chord by combining multiple notes
# def generate_chord(notes, duration):
#     chord_wave = np.zeros(int(SAMPLE_RATE * duration))
#     for note in notes:
#         if note in frequencies:  # Check if the note exists in the frequencies dictionary
#             chord_wave += generate_sine_wave(frequencies[note], duration)
#     # Normalize the chord wave to prevent clipping
#     chord_wave /= np.max(np.abs(chord_wave))  # Normalize to prevent clipping
#     return chord_wave

# def generate_melody(username):
#     try:
#         # Convert username to lowercase and filter valid characters
#         username = username.lower()
#         melody = np.array([])

#         for char in username:
#             if char in letter_to_note:
#                 note = letter_to_note[char]
#                 # Create a chord with the root, third, and fifth
#                 if note == 'C3':
#                     chord = generate_chord(['C3', 'E3', 'G3'], NOTE_DURATION)  # C major chord
#                 elif note == 'D3':
#                     chord = generate_chord(['D3', 'F3', 'A3'], NOTE_DURATION)  # D minor chord
#                 elif note == 'E3':
#                     chord = generate_chord(['E3', 'G3', 'B3'], NOTE_DURATION)  # E minor chord
#                 elif note == 'F3':
#                     chord = generate_chord(['F3', 'A3', 'C4'], NOTE_DURATION)  # F major chord
#                 elif note == 'G3':
#                     chord = generate_chord(['G3', 'B3', 'D4'], NOTE_DURATION)  # G major chord
#                 elif note == 'A3':
#                     chord = generate_chord(['A3', 'C4', 'E4'], NOTE_DURATION)  # A minor chord
#                 elif note == 'B3':
#                     chord = generate_chord(['B3', 'D4', 'F4'], NOTE_DURATION)  # B diminished chord
#                 else:
#                     chord = generate_sine_wave(frequencies[note], NOTE_DURATION)  # Single note if no chord

#                 melody = np.append(melody, chord)

#         # Normalize the melody
#         if len(melody) > 0:
#             melody = melody / np.max(np.abs(melody))

#         # Convert to 16-bit PCM
#         melody_int = np.int16(melody * 32767)

#         # Save to bytes buffer
#         buffer = io.BytesIO()
#         wavfile.write(buffer, SAMPLE_RATE, melody_int)
#         buffer.seek(0)

#         # Convert to base64 for sending to client
#         melody_base64 = base64.b64encode(buffer.read()).decode('utf-8')

#         return melody_base64

#     except Exception as e:
#         raise Exception(f"Failed to generate melody: {str(e)}")

# # Example usage
# # username = "calm"
# # melody_base64 = generate_melody(username)
# # print(melody_base64)  # This will print the base64 encoded calming melody



import numpy as np
from scipy.io import wavfile
import io
import base64

# Define musical parameters
SAMPLE_RATE = 44100
NOTE_DURATION = 0.46  # Duration for a lively sound

# Frequencies for notes (middle octaves for a pleasant effect)
frequencies = {
    'C3': 130.81,
    'D3': 146.83,
    'E3': 164.81,
    'F3': 174.61,
    'G3': 196.00,
    'A3': 220.00,
    'B3': 246.94,
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,
    'D5': 587.33,
    'E5': 659.25,
    'F5': 698.46,
    'G5': 783.99,
    'A5': 880.00,
    'A6':470.00,
    'B5': 987.77
}

# Map letters to notes (middle octaves for a pleasant effect)
letter_to_note = {
    'a': 'C4', 'b': 'C4',  # C4
    'c': 'D4', 'd': 'D4',  # D4
    'e': 'G3', 'f': 'B3',  # E4
    'g': 'F4', 'h': 'C4',  # F4
    'i': 'C4', 'j': 'G4',  # G4
    'k': 'A3', 'l': 'A4',  # A4
    'm': 'B3', 'n': 'D3',  # B4
    'o': 'A3', 'p': 'C5',  # C5
    'q': 'E3', 'r': 'D3',  # E5 and D5
    's': 'F3', 't': 'E3',  # F5 and E5
    'u': 'G3', 'v': 'G5',  # G5
    'w': 'A5', 'x': 'C4',  # A5 and C4
    'y': 'C5', 'z': 'F5'   # C5 and F5
}

# Function to generate a sine wave for a given frequency and duration
def generate_sine_wave(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude of 0.5
    return wave

# Function to create a chord by combining multiple notes
def generate_chord(notes, duration):
    chord_wave = np.zeros(int(SAMPLE_RATE * duration))
    for note in notes:
        if note in frequencies:  # Check if the note exists in the frequencies dictionary
            chord_wave += generate_sine_wave(frequencies[note], duration)
    # Normalize the chord wave to prevent clipping
    chord_wave /= np.max(np.abs(chord_wave))  # Normalize to prevent clipping
    return chord_wave

def generate_melody(username):
    try:
        # Convert username to lowercase and filter valid characters
        username = username.lower()
        melody = np.array([])

        # Define a cheerful chord progression
        chord_progression = ['C4', 'F4', 'G4', 'C4']  # I-IV-V-I progression

        for char in username:
            if char in letter_to_note:
                note = letter_to_note[char]
                # Create a chord based on the cheerful progression
                if note in chord_progression:
                    if note == 'C4':
                        chord = generate_chord(['C4', 'E4', 'G4'], NOTE_DURATION)  # C major chord
                    elif note == 'F4':
                        chord = generate_chord(['F4', 'A4', 'C5'], NOTE_DURATION)  # F major chord
                    elif note == 'G4':
                        chord = generate_chord(['G4', 'B4', 'D5'], NOTE_DURATION)  # G major chord
                else:
                    chord = generate_sine_wave(frequencies[note], NOTE_DURATION)  # Single note if no chord

                melody = np.append(melody, chord)

        # Normalize the melody
        if len(melody) > 0:
            melody = melody / np.max(np.abs(melody))

        # Convert to 16-bit PCM
        melody_int = np.int16(melody * 32767)

        # Save to bytes buffer
        buffer = io.BytesIO()
        wavfile.write(buffer, SAMPLE_RATE, melody_int)
        buffer.seek(0)

        # Convert to base64 for sending to client
        melody_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return melody_base64

    except Exception as e:
        raise Exception(f"Failed to generate melody: {str(e)}")

# Example usage
# username = "happy"
# melody_base64 = generate_melody(username)
# print(melody_base64)  # This will print the base64 encoded cheerful melody