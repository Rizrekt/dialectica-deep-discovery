import sys
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import dynamic_credential_entry, DynamicCredentialError
try:
    e = dynamic_credential_entry("custom.google-gemini", "access_token")
    s = str(e.get("surrogate", ""))
    print("GEMINI_SURROGATE_OK", s.startswith("hsurr:"), "placement:", e.get("placement"))
except DynamicCredentialError as ex:
    print("GEMINI_SURROGATE_FAIL", ex)
