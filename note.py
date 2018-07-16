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

#from . import tuning

class NoteConvertionError(Exception):
	pass

class Note(abc.ABC):
	def __init__(self, raw_value): # Do not override
		try:
			value = int(raw_value) # TODO: make it so if Note(instanceofNote), return the param, dont make new Note, dont make error
		except ValueError:
			try:
				converted_value = self.convert(raw_value)
			except (NoteConvertionError):
				raise TypeError("value %s must be int or valid key" % repr(raw_value))
			else:
				return self.__init__(converted_value) # put in else clause to isolate exception
		
		if value not in self.table():
			raise ValueError("invalid value %s" % str(value))
		
		self.value = value
		self._name = None
	
	@classmethod
	def convert(cls, value): # Override me # example: "A3" -> int
		raise NoteConvertionError()
	
	@classmethod
	@abc.abstractmethod
	def table(cls): # Override me
		return [] # All acceptable note.value
	
	
	@classmethod
	def calculate_name(cls, value): # Override me
		return value
	
	@property
	def name(self): # Do not override, override calculate_name
		if self._name is None:
			self._name = self.calculate_name(self.value)
		
		return self._name
	
	def __repr__(self): # Do not override, override calculate_name
		return "%s(%r)" % (self.__class__.__name__, self.value)
	
	def __str__(self):
		return str(self.name)
	
	
	def __hash__(self):
		return hash(self.value)
	
	def __eq__(self, other):
		if not type(self) == type(other):
			return NotImplemented
		
		return self.value == other.value # Should never do attr error bs same class
	
	def __ne__(self, other):
		if not type(self) == type(other):
			return NotImplemented
		
		return not self.__eq__(other)

class Chromatic(Note):
	NOTE_CONVERT_TABLE = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, # the "#" and "b" are keyboard character, not little b
						  "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8, "AB": 8, "A":9, # All uppercase bc `value = str(value).strip().upper()`
						  "A#": 10, "BB": 10, "B": 11}
	
	NOTE_CONVERT_INVERSE_TABLE = {v: k for k, v in NOTE_CONVERT_TABLE.items()} # Todo: "EB" -> "Eb"
	
	@classmethod
	def convert(cls, value): # actually implement "A3" -> int, scientific pitch notation
		
		value = str(value).strip().upper()
		
		note_input = value[:2]
		simple_note_input = note_input[:1]
		octave_input = None
		
		note = None
		octave = None
		
		try:
			note = cls.NOTE_CONVERT_TABLE[note_input] # First try 2 char input, then if fail try 1 char input
		except KeyError:
			try:
				note = cls.NOTE_CONVERT_TABLE[simple_note_input]
			except KeyError:
				raise NoteConvertionError("Note not found")
			else:
				octave_input = value[1:]
		else:
			octave_input = value[2:]
		
		try:
			octave = int(octave_input)
		except ValueError:
			raise NoteConvertionError("Octave not found")
		
		return note + (octave + 1) * 12 # https://en.wikipedia.org/wiki/Scientific_pitch_notation
	
	@classmethod
	def table(cls):
		return range(128) # don't need list() bc int in range() works? # from 0 to 127 competable w/ MIDI
	
	@classmethod
	def calculate_name(cls, value):
		note = value % 12
		octave = value // 12 - 1
		
		return cls.NOTE_CONVERT_INVERSE_TABLE[note] + str(octave)
