import socket

try:
    socket.gethostbyname('api.gemini-ai.com')
    print("DNS resolution successful.")
except socket.gaierror as e:
    print(f"DNS resolution failed: {e}")
