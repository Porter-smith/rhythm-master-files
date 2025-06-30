#!/usr/bin/env python3
"""
MIDI Song Database Generator
Reads MIDI files and generates a JSON structure similar to the TypeScript song database
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import re

def extract_song_info_from_filename(filename: str) -> Dict[str, Any]:
    """Extract song information from filename"""
    # Remove .mid/.midi extension
    name = filename.replace('.mid', '').replace('.midi', '')
    
    # Default values
    title = name
    artist = "Unknown"
    difficulties = ["easy"]
    overall_difficulty = 5  # Hardcoded to 5
    
    # Try to extract artist and title from common patterns
    if ' - ' in name:
        parts = name.split(' - ', 1)
        artist = parts[0].strip()
        title = parts[1].strip()
    elif ' -' in name:
        parts = name.split(' -', 1)
        artist = parts[0].strip()
        title = parts[1].strip()
    
    # Special cases for known songs
    if 'twinkle' in name.lower():
        title = "Twinkle Twinkle Little Star"
        artist = "Traditional"
    elif 'beethoven' in name.lower() or 'moonlight' in name.lower():
        artist = "Beethoven"
        title = "Moonlight Sonata"
    elif 'debussy' in name.lower() or 'clair' in name.lower():
        artist = "Debussy"
        title = "Clair de Lune"
    elif 'metallica' in name.lower():
        artist = "Metallica"
        if 'master' in name.lower():
            title = "Master of Puppets"
        elif 'nothing' in name.lower():
            title = "Nothing Else Matters"
    elif 'michael jackson' in name.lower() or 'billie jean' in name.lower():
        artist = "Michael Jackson"
        title = "Billie Jean"
    elif 'nirvana' in name.lower() or 'smells' in name.lower():
        artist = "Nirvana"
        title = "Smells Like Teen Spirit"
    elif 'owl city' in name.lower() or 'fireflies' in name.lower():
        artist = "Owl City"
        title = "Fireflies"
    elif 'pokemon' in name.lower():
        artist = "Pokemon"
        title = "Wild Pokemon Battle"
    elif 'smash' in name.lower() and 'mouth' in name.lower():
        artist = "Smash Mouth"
        title = "All Star"
    elif 'final countdown' in name.lower():
        artist = "Europe"
        title = "The Final Countdown"
    elif 'toto' in name.lower() or 'africa' in name.lower():
        artist = "Toto"
        title = "Africa"
    elif 'wii' in name.lower() and 'theme' in name.lower():
        artist = "Nintendo"
        title = "Wii Theme"
    elif 'mii channel' in name.lower():
        artist = "Nintendo"
        title = "Mii Channel"
    elif 'super smash' in name.lower():
        artist = "Nintendo"
        title = "Super Smash Bros Brawl - Main Theme"
    elif 'mountain king' in name.lower():
        artist = "Grieg"
        title = "In the Hall of the Mountain King"
    elif 'titanic' in name.lower() or 'heart' in name.lower():
        artist = "Celine Dion"
        title = "My Heart Will Go On"
    elif 'backstreet' in name.lower():
        artist = "Backstreet Boys"
        title = "I Want It That Way"
    elif 'dooms-gate' in name.lower():
        artist = "Doom"
        title = "Doom's Gate"
    elif 'spearsofjustice' in name.lower():
        artist = "Undertale"
        title = "Spear of Justice"
    elif 'test-drive' in name.lower():
        artist = "Test"
        title = "Test Drive"
    elif 'desert' in name.lower() or 'canyon' in name.lower():
        artist = "Traditional"
        title = "Desert Canyon"
    elif 'beach' in name.lower() and 'town' in name.lower():
        artist = "Traditional"
        if 'violin' in name.lower():
            title = "Beach Town Violin"
        elif 'flute' in name.lower():
            title = "Beach Town Flute"
    
    return {
        "title": title,
        "artist": artist,
        "difficulties": difficulties,
        "overall_difficulty": overall_difficulty
    }

def generate_midi_songs_json():
    """Generate JSON structure for MIDI songs"""
    midi_dir = Path("midi")
    songs = []
    
    if not midi_dir.exists():
        print(f"MIDI directory {midi_dir} not found!")
        return
    
    # Get all MIDI files
    midi_files = list(midi_dir.glob("*.mid")) + list(midi_dir.glob("*.midi"))
    
    for midi_file in midi_files:
        filename = midi_file.name
        
        # Extract basic info from filename
        song_info = extract_song_info_from_filename(filename)
        
        # Generate song ID
        song_id = filename.replace('.mid', '').replace('.midi', '').lower()
        song_id = re.sub(r'[^a-z0-9]', '-', song_id)
        song_id = re.sub(r'-+', '-', song_id).strip('-')
        
        # Create song object
        song = {
            "id": f"{song_id}-midi",
            "title": song_info["title"],
            "artist": song_info["artist"],
            "duration": "0:30",  # Default duration
            "difficulties": song_info["difficulties"],
            "bpm": 120,  # Default BPM
            "format": "midi",
            "overallDifficulty": song_info["overall_difficulty"],
            "soundFont": "https://porter-smith.github.io/rhythm-master-files/soundfonts/gzdoom.sf2",
            "midiFiles": {
                "easy": f"https://porter-smith.github.io/rhythm-master-files/midi/{filename}"
            },
            "audioFiles": {
                "easy": f"/audio/{song_id}-easy.mp3"
            },
            "notes": {
                "easy": []
            }
        }
        
        # Add soundfont for certain songs
        if any(keyword in filename.lower() for keyword in ['doom', 'spearsofjustice', 'beach', 'desert']):
            song["soundFont"] = "https://porter-smith.github.io/rhythm-master-files/soundfonts/gzdoom.sf2"
        
        songs.append(song)
    
    return songs

def main():
    """Main function to generate the JSON structure"""
    print("Analyzing MIDI files...")
    
    try:
        midi_songs = generate_midi_songs_json()
        
        if not midi_songs:
            print("No MIDI songs found!")
            return
        
        # Create the full structure
        output = {
            "midiSongs": midi_songs,
            "allSongs": midi_songs  # For now, just MIDI songs
        }
        
        # Save to JSON file
        with open("midi_songs_database.json", "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"Generated database with {len(midi_songs)} MIDI songs")
        print("Saved to: midi_songs_database.json")
        
        # Also print a TypeScript-like structure
        print("\n" + "="*50)
        print("TypeScript-like structure:")
        print("="*50)
        
        print("export const midiSongs: MidiSong[] = [")
        for i, song in enumerate(midi_songs):
            print(f"  {{")
            print(f"    id: '{song['id']}',")
            print(f"    title: '{song['title']}',")
            print(f"    artist: '{song['artist']}',")
            print(f"    duration: '{song['duration']}',")
            print(f"    difficulties: {json.dumps(song['difficulties'])},")
            print(f"    bpm: {song['bpm']},")
            print(f"    format: 'midi',")
            print(f"    overallDifficulty: {song['overallDifficulty']},")
            if 'soundFont' in song:
                print(f"    soundFont: '{song['soundFont']}',")
            print(f"    midiFiles: {{")
            print(f"      easy: '{song['midiFiles']['easy']}'")
            print(f"    }},")
            print(f"    notes: {{")
            print(f"      easy: []")
            print(f"    }}")
            if i < len(midi_songs) - 1:
                print(f"  }},")
            else:
                print(f"  }}")
        print("];")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
