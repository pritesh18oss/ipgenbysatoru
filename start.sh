if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/pritesh18oss/ipgenbysatoru /ipgenbysatoru
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /ipgenbysatoru
fi
cd /ipgenbysatoru
pip install -U -r requirements.txt
echo "Starting Bot...."
python bot.py
