from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class PspMediaVolume(AliceSkill):
	"""
	Author: poulsp
	Description: Manage volume in the synchronous multiroom audio.
	"""

	@IntentHandler('MyIntentName')
	def dummyIntent(self, session: DialogSession, **_kwargs):
		pass
