#!/bin/bash

# Script simple pour lancer fullv2.py au démarrage du Raspberry Pi

echo "Configuration du démarrage automatique pour fullv2.py..."

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

echo "Configuration terminée !"
echo "Votre programme fullv2.py se lancera automatiquement au prochain redémarrage."
echo ""
echo "Pour tester maintenant: /home/pi/start_fullv2.sh"
echo "Pour redémarrer: sudo reboot"