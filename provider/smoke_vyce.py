import sys
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import dynamic_credential_entry
e = dynamic_credential_entry("custom.vyce", "access_token")
open("/tmp/vyce_surr.txt", "w").write(str(e["surrogate"]))
print("surrogate staged")
