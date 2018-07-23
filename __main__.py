#!/bin/env python3


# Python based music sequencer
# Copyright (C) 2018 dzil123

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import music
import numpy as np

from music.note import Chromatic as Note
from music.tuning import EqualTempermentChromatic as Tuning
from music.sequence import Sequence
from music.instrument import SinWave as Instrument

BPM = 120
LENGTH_NOTE = 1/4 # quarter note
NOTE_DURATION = (60 * LENGTH_NOTE) / BPM

NOTES = ("C4", "D4", "E4", "F4")

SAMPLING_RATE = 44100
# BIT_DEPTH = None # will set when implement wave conversion

note_list = Sequence(Tuning)

for index, note in enumerate(NOTES):
	note_object = Note(note)
	time = NOTE_DURATION * index
	duration = NOTE_DURATION
	
	note_list.add(note_object, time, duration)

note_list_render = note_list.render()

# TMP WORKAROUND BC Instrument.render isnt implemented

#array = np.zeros(SAMPLING_RATE * len(NOTES) * NOTE_DURATION, dtype=np.float64)

instrument = Instrument(SAMPLING_RATE)

array = np.empty(0, dtype=np.float64)

for note in note_list_render:
	array = np.concatenate( (array, instrument.render_note(note)) ) # arrays to concat must be in tuple

# TODO render to ints and write to wave

