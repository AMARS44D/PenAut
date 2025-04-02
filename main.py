import os, sys

# Vérification des droits root
if os.geteuid() != 0:
    print("❌ Ce script doit être exécuté en root (utilisez sudo).")
    sys.exit(1)

