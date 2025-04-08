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
=======
#!/bin/bash

# === Configuration ===
TOOL_NAME="¨PenAut"
TOOL_FILE="PenAut_pack"  # Dossier contenant le code source
INSTALL_LIB_PATH="/usr/local/lib/$TOOL_NAME"
BIN_PATH="/usr/local/bin/$TOOL_NAME"
REQUIREMENTS_FILE="requirements.txt"

# === Vérification des privilèges root ===
if [ "$EUID" -ne 0 ]; then
    echo "🔐 Ce script nécessite des privilèges administrateur (sudo)."
    echo "➡️  Veuillez entrer votre mot de passe sudo pour continuer..."
    exec sudo bash "$0" "$@"
fi

echo "🚀 Début de l'installation de l'outil $TOOL_NAME..."

# === Vérification de pip3 ===
if ! command -v pip3 &> /dev/null; then
    echo "⚠️ pip3 n'est pas installé. Installation en cours..."
    apt update && apt install -y python3-pip
fi

# === Vérification du fichier requirements.txt ===
if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo "❌ ERREUR : Le fichier $REQUIREMENTS_FILE est introuvable."
    exit 1
fi

# === Installation des dépendances ===
echo "📦 Installation des modules Python requis..."
pip3 install -r "$REQUIREMENTS_FILE"
echo "✅ Dépendances installées avec succès."

# === Création du dossier d'installation ===
echo "📁 Création du dossier $INSTALL_LIB_PATH..."
mkdir -p "$INSTALL_LIB_PATH"

# === Copie des fichiers source ===
echo "📤 Copie des fichiers de $TOOL_FILE vers $INSTALL_LIB_PATH..."
rsync -a --exclude='*.pyc' "$TOOL_FILE/" "$INSTALL_LIB_PATH/"

# === Vérification du fichier main.py ===
MAIN_FILE="$INSTALL_LIB_PATH/main.py"
if [[ ! -f "$MAIN_FILE" ]]; then
    echo "❌ ERREUR : Le fichier main.py est introuvable dans $INSTALL_LIB_PATH."
    exit 1
fi

# === Permissions ===
chmod +x "$MAIN_FILE"
chmod -R a+rX "$INSTALL_LIB_PATH"

# === Lien symbolique global ===
echo "🔗 Création du lien symbolique dans $BIN_PATH..."
rm -f "$BIN_PATH"
echo -e "#!/bin/bash\npython3 \"$MAIN_FILE\" \"\$@\"" > "$BIN_PATH"
chmod +x "$BIN_PATH"

# === Fin ===
echo "✅ Installation de $TOOL_NAME terminée avec succès !"
echo "🟢 Vous pouvez maintenant utiliser votre outil avec la commande : $TOOL_NAME"

