# ~/.local/bin/projectalice-sk validate --paths ~/ProjectAlice/skills/PspMediaVolume

import re
import json
import os

from core.commons import constants
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.util.Decorators import MqttHandler


from skills.PspMediaVolume.library.Topics import(	_MULTIROOM_VOLUME,
																									_MULTIROOM_ENTRY_VOLUME,
																									_MULTIROOM_GESTURE_SENSOR_VOLUME_UP,
																									_MULTIROOM_GESTURE_SENSOR_VOLUME_DOWN
																								)

from skills.PspMediaVolume.library.CheckSnapcast import(CheckSnapcast)

class PspMediaVolume(AliceSkill):
	"""
	Author: poulsp
	Description:	Manage volume in the synchronous multiroom audio.
	"""

	#-----------------------------------------------
	def __init__(self):
		super().__init__()

		CheckSnapcast.installSnapserver()

		self._volumeStepsUpDown = None
		self._volume_station_default  = "0" # ???
		self._beQuiet                 = 1
		self._volumeCurrent           = ""
		self._isMuted                 = False
		self._volume 									= self._beQuiet
		self._activeSoundApp					= ""


		#-----------------------------------------------
	@property
	def beQuiet(self):
		return self._beQuiet


	#-----------------------------------------------
	@property
	def isMuted(self):
		return self._isMuted


	#-----------------------------------------------
	@isMuted.setter
	def isMuted(self, boolValue):
		self._isMuted = boolValue


	#-----------------------------------------------
	@property
	def volume(self):
		return self._volume


	#-----------------------------------------------
	@volume.setter
	def volume(self, value):
		self._volume = value


	#-----------------------------------------------
	def onStart(self):
		super().onStart()
		#TODO read volumeStepsUpDown from config
		self._volumeStepsUpDown = 10
		self._volumeCurrent	    = "40"
		self._volumeTemp		  	= self._volumeCurrent
		self._volume 						= self._volumeCurrent
		self._activeSoundApp					= ""


	#-----------------------------------------------
	def onHotwordToggleOff(self, siteId: str, session: DialogSession):
		#self.logDebug(f"###################### onHotwordToggleOff session: {session}")
		# session are None, when it comes from My temporary DND skill PspDnd.
		if session == None:
			return
		if not self.isMuted:
			self._onHotwordVolume = self._volume
			self.publish(_MULTIROOM_VOLUME,  json.dumps({'playSite': 'everywhere', 'volume': self.beQuiet, 'info': 'onHotwordToggleOff'}))


	#-----------------------------------------------
	def onHotwordToggleOn(self, siteId: str, session: DialogSession):
		#self.logDebug(f"###################### onHotwordToggleOn")

		if not self.isMuted:
			self.publish(_MULTIROOM_VOLUME,  json.dumps({'playSite': 'everywhere', 'volume': self._volume, 'info': 'onHotwordToggleOn'}))


	#-----------------------------------------------
	def _setMediaVolume(self, percent = '40'):
		percent = int(percent)
		if percent == 0:
			percent = 1
		else:
			if percent >= 94:
				percent = 94
			elif percent <= 0:
				percent = 1

		self._volume = str(percent)


	#-----------------------------------------------
	@MqttHandler(_MULTIROOM_GESTURE_SENSOR_VOLUME_UP)
	def gestureSensorVolumeUp(self, session: DialogSession):
		percent = int(self._volume) + self._volumeStepsUpDown
		self._setMediaVolume(str(percent))
		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@MqttHandler(_MULTIROOM_GESTURE_SENSOR_VOLUME_DOWN)
	def gestureSensorVolumeDown(self, session: DialogSession):
		percent = int(self._volume) - self._volumeStepsUpDown
		self._setMediaVolume(str(percent))
		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@IntentHandler('volumeUp')
	def volumeUp(self, session: DialogSession):
		percent	= '0' if 'Percent' not in session.slots else session.slotValue('Percent')

		percent = int(percent)
		if percent == 0:
			percent = int(self._volume) + self._volumeStepsUpDown
		else:
			percent = int(self._volume) + int(session.slotValue('Percent'))

		self._volume = str(percent)
		self._setMediaVolume(self._volume)

		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@IntentHandler('volumeDown')
	def volumeDown(self, session: DialogSession):
		percent	= '0' if 'Percent' not in session.slots else session.slotValue('Percent')

		percent = int(percent)
		if percent == 0:
			percent = int(self._volume) - self._volumeStepsUpDown
		else:
			percent = int(self._volume) - int(session.slotValue('Percent'))

		self._volume = str(percent)
		self._setMediaVolume(self._volume)

		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@IntentHandler('setVolume')
	def setVolume(self, session: DialogSession):
		percent	= '0' if 'Percent' not in session.slots else session.slotValue('Percent')

		self._setMediaVolume(percent)
		self.endDialog(session.sessionId, self.randomTalk('setVolume', [self._volume]))


	#-----------------------------------------------
	@IntentHandler('getVolume')
	def getVolume(self, session: DialogSession):
		self.endDialog(session.sessionId, self.randomTalk('getVolume', [self._volume]))


	#-----------------------------------------------
	@IntentHandler('volumeMute')
	def volumeMute(self, session: DialogSession):
		self.isMuted = True
		self._onHotwordVolume = self._volume
		self.publish(_MULTIROOM_VOLUME,  json.dumps({'playSite': 'everywhere', 'volume': self.beQuiet, 'muted': True}))

		self.endDialog(session.sessionId, self.randomTalk('volumeMute'))


	#-----------------------------------------------
	@IntentHandler('volumeUnmute')
	def volumeUnmute(self, session: DialogSession):
		self.isMuted = False
		self._onHotwordVolume = self._volume
		self.publish(_MULTIROOM_VOLUME,  json.dumps({'playSite': 'everywhere', 'volume': self._volume, 'muted': False}))

		self.endDialog(session.sessionId, self.randomTalk('volumeUnmute'))


	#-----------------------------------------------
	@MqttHandler(_MULTIROOM_ENTRY_VOLUME)
	def setStationEntryVolume(self, session: DialogSession, **_kwargs):
		try:
			self._activeSoundApp = session.payload['activeSoundApp']
		except Exception as e:
			print(f"################# except Exception as e: {e}")


		# Volume is passed to players via onHotwordToggleOn/Off
		self._volume = session.payload['stationVolume']

		#'sendFrom': 'PspBluetoothStreamer'
		# if self._activeSoundApp == 'PspBluetoothStreamer' in list(session.payload.values()):
		# 	self.publish(_MULTIROOM_VOLUME,  json.dumps({'playSite': 'everywhere', 'volume': self._volume}))
		self.publish(_MULTIROOM_VOLUME,  json.dumps({'playSite': 'everywhere', 'volume': self._volume}))


	#-----------------------------------------------
	def onSkillDeleted(self, skill: str):
		CheckSnapcast.removeSnapserver()
		super()
