#!/bin/bash

# Nom de l'outil
TOOL_NAME="PenAut"
SCRIPT_NAME="main.py"
ALIAS_NAME="penaut"

# Vérifie si exécuté en root (sudo)
if [ "$EUID" -ne 0 ]; then
    echo "[!] Ce script nécessite des privilèges administrateur."
    echo "[>] Veuillez entrer votre mot de passe sudo pour continuer..."
    exec sudo bash "$0" "$@"
fi

echo "[✓] Privilèges root confirmés."

# Vérifie si pip3 est installé
if ! command -v pip3 &> /dev/null; then
    echo "[•] pip3 n'est pas installé. Installation en cours..."
    apt update && apt install -y python3-pip
fi

echo "[+] Installation des dépendances Python..."

# Installer les modules requis
pip3 install -r ./requirement.txt

echo "[✓] Modules Python installés."

# Rendre le script principal exécutable
chmod +x "$SCRIPT_NAME"

# Détection du shell de l'utilisateur courant
USER_SHELL_CONFIG="$HOME/.bashrc"
if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
    USER_SHELL_CONFIG="$HOME/.zshrc"
fi

# Ajouter un alias s'il n'existe pas
if ! grep -q "alias $ALIAS_NAME=" "$USER_SHELL_CONFIG"; then
    echo "alias $ALIAS_NAME='python3 $(pwd)/$SCRIPT_NAME'" >> "$USER_SHELL_CONFIG"
    echo "[✓] Alias ajouté dans $USER_SHELL_CONFIG"
    echo "[i] Recharge ton terminal ou exécute : source $USER_SHELL_CONFIG"
else
    echo "[i] Alias déjà présent dans $USER_SHELL_CONFIG"
fi

echo "[✔] Installation terminée ! Tu peux maintenant lancer ton outil avec : $ALIAS_NAME"
