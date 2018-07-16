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


from . import tuning, note

class Sequence(object):
	def __init__(self, tuning_manager):
		if not isinstance(tuning_manager, tuning.Frequency):
			raise TypeError("'tuning_manager' must be a valid music.tuning.Frequency")
		
		self.tuning = tuning_manager
		self._list = list()
	
	def add(self, new_note, time, duration):
		hertz = self.tuning.get_frequency(new_note) # don't catch TypeError "note param must be accepted type"
		
		note_dict = {"note": hertz, "time": time, "duration": duration}
		
		self._list.append(note_dict)
	
	def render():
		return sorted(self._list)
