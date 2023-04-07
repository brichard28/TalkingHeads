from pathlib import Path
import subprocess, time, os

version = '2020.2.5'
appFile = Path('/Users/lpzjwp/code/psychopy/git/dist/PsychoPy.app')
dmgFilename = str(appFile).replace(".app", "_rw.dmg")

thisFolder = Path(__file__).parent
finalDistFolder = thisFolder.parent.parent/'dist'

with Path().home()/ 'keys/apple_ost_id' as p:
    IDENTITY = p.read_text().strip()
with Path().home()/ 'keys/apple_psychopy3_app_specific' as p:
    PWORD = p.read_text().strip()

ENTITLEMENTS = thisFolder / "entitlements.plist"
BUNDLE_ID = "org.opensciencetools.psychopy"
USERNAME = "admin@opensciencetools.org"

def dmgStapleInside():
    dmgFilename = str(appFile).replace(".app", "_rw.dmg")
    appName = appFile.name
    """Staple the notarization to the app inside the r/w dmg file"""
    # staple the file inside the dmg
    cmdStr = f"hdiutil attach '{dmgFilename}'"
    exitcode, output = subprocess.getstatusoutput(cmdStr)
    volName = output.split('\t')[-1]
    staple(f"'{volName}/{appName}'")
    cmdStr = f"hdiutil detach '{volName}' -quiet"
    print(f'cmdStr was: {cmdStr}')
    for n in range(5):  # if we do this too fast then it fails. Try 5 times
        time.sleep(5)
        exitcode, output = subprocess.getstatusoutput(cmdStr)
        print(f"Attempt {n}. output: '{output}''")
        if exitcode == 0:
            break  # succeeded so stop
    if exitcode != 0:
        print(f'*********Failed to detach {volName} (wrong name?) *************')
        exit(1)

def dmgCompress():
    dmgFilename = str(appFile).replace(".app", "_rw.dmg")
    dmgFinalFilename = finalDistFolder/(f"StandalonePsychoPy-{version}-macOS.dmg")
    # remove previous file if it's there
    if Path(dmgFinalFilename).exists():
        os.remove(dmgFinalFilename)

    cmdStr = f"hdiutil convert {dmgFilename} " \
                f"-format UDZO " \
                f"-o {dmgFinalFilename}"
    exitcode, output = subprocess.getstatusoutput(cmdStr)
    print(output)
    if exitcode != 0:
        print(f'****Failed to compress {dmgFilename} to {dmgFinalFilename} (is it not ejected?) ****')
        exit(1)
    return dmgFinalFilename

def staple(filepath):
    cmdStr = f'xcrun stapler staple {filepath}'
    print(cmdStr)
    exitcode, output = subprocess.getstatusoutput(cmdStr)
    print(f"exitcode={exitcode}: {output}")
    if exitcode != 0:
        print('*********Staple failed*************')
        exit(1)

if __name__ == "__main__":
    dmgStapleInside()
    dmgCompress()