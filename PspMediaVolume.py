from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class PspMediaVolume(AliceSkill):
	"""
	Author: poulsp
	Description: Manage volume in the synchronous multiroom audio. this is the ground/base skill for the synchronous multiroom audio system.  uses the excelent 'snapcast system' from "https://github.com/badaix/snapcast" by badaix.
	"""

	@IntentHandler('MyIntentName')
	def dummyIntent(self, session: DialogSession, **_kwargs):
		pass
