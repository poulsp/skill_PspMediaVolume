import platform
import shlex
import subprocess

# HELP TO DEVELOPMENT.
# sudo apt-get purge snapserver -y
# sudo rm /dev/shm/snapfifo
# sudo joe /etc/snapserver.conf
# sudo systemctl status snapserver.service
# Test stream
# ffmpeg -v 0 -y -rtbufsize 15M -i http://stream.srg-ssr.ch/m/rsj/aacp_96 -f u16le -acodec pcm_s16le -ac 2 -ar 48000 /dev/shm/snapfifo


_RELEASE 	= '0.21.0'
_URL 			= 'https://github.com/badaix/snapcast/releases/download'
_WGET_URL = f"{_URL}/v{_RELEASE}/snapserver_{_RELEASE}"

_PLATFORM_SYSTEM   = platform.system()
_PLATFORM_MACHINE  = platform.machine()


class CheckSnapcast():


	#-----------------------------------------------
	@staticmethod
	def installSnapserver():
		try:
			_dpkgOutput = subprocess.check_output(
				"dpkg-query -l snapserver",
				stderr=subprocess.STDOUT,
				shell=True
			).decode('utf-8').replace('\n','')

		except subprocess.CalledProcessError as e:
			# Install snapserver
			sedCmd 	= shlex.split('sudo sed -i "s/\.*source = pipe:\/\/\/tmp\/snapfifo?name=default/source = pipe:\/\/\/dev\/shm\/snapfifo?name=default/" /etc/snapserver.conf')
			sedCmd2 = shlex.split('sudo sed -i "s/\.*stream = pipe:\/\/\/tmp\/snapfifo?name=default/stream = pipe:\/\/\/dev\/shm\/snapfifo?name=default/" /etc/snapserver.conf')

			if _PLATFORM_MACHINE == "x86_64":
				# print(f"####################################### _PLATFORM_MACHINE: {_PLATFORM_MACHINE } ")
				# Installed in the Docker image.
				pass
				# downloadUrl = f"{_WGET_URL}-1_amd64.deb"
				# snapServerDeb = f"snapserver_{_RELEASE}-1_amd64.deb"

				# print(f"####################################### downloadUrl {downloadUrl } ")
				# print(f"####################################### snapServerDeb {snapServerDeb} ")


				# subprocess.run(['wget', downloadUrl])
				# subprocess.run(['sudo', 'dpkg', '-i', snapServerDeb])
				# subprocess.run(['sudo', 'apt-get', '-f', 'install', '-y'])
				# subprocess.run(['rm', snapServerDeb])
				# subprocess.run(['sudo', 'systemctl', 'stop', 'snapserver'])
				# subprocess.run(sedCmd)
				# subprocess.run(sedCmd2)
				# subprocess.run(['sudo', 'rm', '/tmp/snapfifo'])
				# subprocess.run(['sudo', 'systemctl', 'restart', 'snapserver'])


			elif _PLATFORM_MACHINE == "armv7l" or _PLATFORM_MACHINE == "armv6l":
				# print(f"####################################### _PLATFORM_MACHINE: {_PLATFORM_MACHINE } ")
				downloadUrl = f"{_WGET_URL}-1_armhf.deb"
				snapServerDeb = f"snapserver_{_RELEASE}-1_armhf.deb"

				# print(f"####################################### downloadUrl {downloadUrl } ")
				# print(f"####################################### snapServerDeb {snapServerDeb} ")

				subprocess.run(['wget', downloadUrl])
				subprocess.run(['sudo', 'dpkg', '-i', snapServerDeb])
				subprocess.run(['sudo', 'apt-get', '-f', 'install', '-y'])
				subprocess.run(['rm', snapServerDeb])
				subprocess.run(['sudo', 'systemctl', 'stop', 'snapserver'])
				subprocess.run(sedCmd)
				subprocess.run(sedCmd2)
				subprocess.run(['sudo', 'rm', '/tmp/snapfifo'])
				subprocess.run(['sudo', 'systemctl', 'restart', 'snapserver'])


	#-----------------------------------------------
	@staticmethod
	def removeSnapserver():
		if _PLATFORM_MACHINE == "x86_64":
			print(f"####################################### _PLATFORM_MACHINE: {_PLATFORM_MACHINE } ")
			# Installed in the Docker image.
			pass

		elif _PLATFORM_MACHINE == "armv7l" or _PLATFORM_MACHINE == "armv6l":
			subprocess.run(['sudo', 'systemctl', 'stop', 'snapserver'])
			subprocess.run(['sudo', 'rm', '/dev/shm/snapfifo'])
			subprocess.run(['sudo', 'apt-get', 'purge', 'snapserver', '-y'])

