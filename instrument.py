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


import abc
import music
import numpy as np
#import math # apparently np.pi

from . import sequence

class Instrument(object):
	def __init__(self, sampling_rate=44100): # TODO: maybe sampling rate in render_note
		self.sampling_rate = np.uint32(sampling_rate) # for all sampling rates in https://en.wikipedia.org/wiki/Sampling_(signal_processing) , all can fit in uint32
	
	def render(self, sequence_render):
		if not isinstance(sequence_render, sequence.Sequence):
			raise TypeError("'sequence_render' must be an instance of sequence.Sequence")
		
		raise NotImplementedError()
	
	def render_note(self, note_render):
		num_samples = np.ceil(self.sampling_rate * note_render["duration"], dtype=np.float64) # multiply sampling rate by duration to get total number of samples, rounding up # even though it's float64, it is an int but it can't be uint64
		array = np.arange(num_samples, dtype=np.float64) # array from 0 to num_samples int
		array /= self.sampling_rate # each value is now a float of time elapsed from start of note
		
		return self._render_note(note_render, array)
	
	@abc.abstractmethod
	def _render_note(self, note_render, array):
		raise NotImplementedError()

class SinWave(Instrument):
	def _render_note(self, note_render, array):
		raise NotImplementedError()
		return np.sin(2 * np.pi * self.sampling_rate * note_render["note"] * array) # idk
