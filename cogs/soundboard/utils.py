"""
Audio normalization utilities.
"""

import os
from pydub import AudioSegment


def normalize_and_fetch(raw_folder, normalized_folder, target_dbfs):
    """Normalize all MP3 files and return list of normalized paths."""
    normalized_sounds = []
    for file in os.listdir(raw_folder):
        if file.lower().endswith(".mp3"):
            raw_path = os.path.join(raw_folder, file)
            normalized_path = os.path.join(normalized_folder, file)
            normalized_sounds.append(normalized_path)

            if os.path.exists(normalized_path):
                continue

            audio = AudioSegment.from_file(raw_path)
            normalized_audio = normalize(audio, target_dbfs)
            normalized_audio.export(normalized_path, format="mp3")

    return normalized_sounds


def normalize(audio, target_dbfs):
    """Normalize audio to target dBFS level."""
    gain_needed = target_dbfs - audio.dBFS
    normalized_audio = audio.apply_gain(gain_needed)

    return normalized_audio