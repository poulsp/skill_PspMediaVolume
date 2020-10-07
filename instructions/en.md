## PspMediaVolume

### What it does.
Manage volume in the synchronous multiroom audio.
This is the ground/base skill for the synchronous multiroom audio system.

### Want to test it out.
It is not in the ProjectAlice store for now.
But if you want to test it out then clone it as:
```
cd ProjectAlice/skills
git clone https://github.com/poulsp/skill_PspMediaVolume PspMediaVolume
```
### Test it out with the Alice docker image.
Alice docker image [docker-Alice-Linux-x86](https://github.com/poulsp/docker-Alice-Linux-x86.git)
You should remember to uncomment
ports:
#- "1704:1704"
in docker-compose.yml.
