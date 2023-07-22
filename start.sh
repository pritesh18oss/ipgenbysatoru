echo "Cloning main Repository"
git clone https://github.com/pritesh18oss/ipgenbysatoru /ipgenbysatoru
cd /ipgenbysatoru
echo "installing requirements"
pip install requirements.txt
echo "bot starting"
python bot.py
