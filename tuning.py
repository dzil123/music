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

from . import note

class Frequency(abc.ABC):
	ACCEPTED_TYPE = (note.Note)
	
	@classmethod
	def valid_types(cls):
		#try:
		#	return cls.ACCEPTED_TYPE + super().valid_types()
		#except AttributeError: # Parent doesn't have a valid_type(); super() fail
		return cls.ACCEPTED_TYPE
	
	@classmethod # Do not override
	def get_frequency(cls, note_instance):
		if not isinstance(note_instance, cls.valid_types()):
			raise TypeError("'note' parameter must be instance of %s" % str(cls.valid_types()))
		
		return cls._get_frequency(note_instance) # maybe try catch for KeyError
	
	@classmethod
	@abc.abstractmethod
	def _get_frequency(cls, note_instance):
		pass

class LookupTableFrequency(Frequency, abc.ABC):
	ACCEPTED_TYPE = (note.Note)
	
	@classmethod
	@abc.abstractmethod
	def table(cls): # Not all Frequency class will have this!
		return {} # Here is where a dictionary lookup table of Note.value: hertz is defined, probably hardcoded
	
	@classmethod
	def _get_frequency(cls, note_instance):
		
		return cls.table()[note_instance]

class DynamicallyGeneratedFrequency(Frequency, abc.ABC):
	GENERATED_DICT = {}
	
	@classmethod
	def _get_frequency(cls, note_instance):
		
		try:
			return cls.GENERATED_DICT[note_instance]
		except KeyError:
			calculated_freq = cls.calculate_frequency(note_instance)
			cls.GENERATED_DICT[note_instance] = calculated_freq
			return calculated_freq
	
	@classmethod
	@abc.abstractmethod
	def calculate_frequency(cls):
		pass

class Chromatic(DynamicallyGeneratedFrequency):
	ACCEPTED_TYPE = (note.Chromatic)

class EqualTempermentChromatic(Chromatic):
	REF_PITCH_NUM = 69 # midi note # A4
	REF_PITCH_HERTZ = 440.0 # reference_hertz
	
	@classmethod
	def calculate_frequency(cls, note_instance):
		
		#REF_PITCH_HERTZ * ( (2 ** (1/12)) ** (GIVEN_NUM - REF_PITCH_NUM) )
		# https://en.wikipedia.org/wiki/Equal_temperament#Calculating_absolute_frequencies
		
		return cls.REF_PITCH_HERTZ * (2 ** ((note_instance.value - cls.REF_PITCH_NUM) / 12) )
