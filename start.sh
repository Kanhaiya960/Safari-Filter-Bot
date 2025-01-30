if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Kanhaiya960/Safari-Filter-Bot-new.git /Safari-Filter-Bot-new
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Safari-Filter-Bot-new
fi
cd /Safari-Filter-Bot-new
pip3 install -U -r requirements.txt
echo "Starting DQ-The-File-Donor...."
python3 bot.py
