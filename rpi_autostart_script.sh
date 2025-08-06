#!/bin/bash

# Script simple pour lancer fullv2.py au démarrage du Raspberry Pi

# Créer le script de lancement
cat << 'EOF' > /home/pi/start_fullv2.sh
#!/bin/bash
cd /home/pi
source oled-env/bin/activate
python fullv2.py
EOF

# Rendre le script exécutable
chmod +x /home/pi/start_fullv2.sh

# Ajouter au fichier rc.local pour qu'il se lance au démarrage
sudo cp /etc/rc.local /etc/rc.local.backup
sudo sed -i '/^exit 0/i /home/pi/start_fullv2.sh &' /etc/rc.local

echo "config terminée !"
