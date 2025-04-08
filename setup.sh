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
