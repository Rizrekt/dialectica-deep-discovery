import sys
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import dynamic_credential_entry
e = dynamic_credential_entry("custom.google-gemini", "access_token")
open("/tmp/gemini_surr.txt", "w").write(str(e["surrogate"]))
print("surrogate staged")
