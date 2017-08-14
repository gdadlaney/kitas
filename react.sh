curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs npm
npm config set proxy http://192.168.15.254:3128
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
nvm install v6.11.0
npm install -g create-react-native-app
create-react-native-app AwesomeProject
cd AwesomeProject 
sudo sysctl -w fs.inotify.max_user_watches=10000
npm start