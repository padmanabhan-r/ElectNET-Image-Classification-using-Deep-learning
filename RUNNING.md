# Dependencies

### Scraping

You need to have Chrome Browser, Chromedriver and Selenium installed on your system to run the scraper.

1. Install the latest version of Chromedriver from the following link: https://sites.google.com/a/chromium.org/chromedriver/downloads
2. Install Chrome Browser using the following commands:
    sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
    sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    sudo apt-get -y update
    sudo apt-get -y install google-chrome-stable

3. Give the location of the chromedriver in the scrape_images.py.

### Loading Images on MongoDB

You need to have Mongodb installed on your system to store all the downloaded data from the scraper to MongoDB.

1. Install the latest version by following the instructions on this link: https://docs.mongodb.com/manual/installation/

### UI
To be able to view the UI Demo, you need Docker, NodeJS installed. 
1. To install Docker, follow the given link. https://docs.docker.com/install/
2. Follow the given link to install NodeJS. https://nodejs.org/en/download/ 

### Other packages
1. The other packages needed for the project can be installed by running the command: sh dependencies.sh
2. You need to use Python version 3.6 to use Clipper to deploy the machine learning model. 

# Execution

### 1. Scraping the images:
1. The location of the chrome-driver package needs to be specified in the scraping code if you need to download more than 100 images per category
2. Move into the api folder.
3. Execute: python3 ./scrape_images.py
4. The images are stored in the data folder inside api/.
5. For more information, execute: python3 ./scrape_images.py --help

### 2. Loading Images:
1. Start MongoDB.
2. Move into the api folder.
3. Execute: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.1 load_images.py

### 3. Training the model:
1. Start MongoDB.
2. Move into the api folder.
3. Execute: python3 ./model_training.py
4. Save the model file as model_best.pth in the static_files folder inside api/.

### 4. Deploying the model:
1. Start docker.
2. Move into the api folder.
3. Make sure the model file is saved in the static_files folder.
4. To start the clipper connection, run: python3 ./inference/clipper_connection.py
5. Once the clipper connection is established, deploy the model and create a REST endpoint by running: python3 ./inference/inference.py. This will take some time to execute.
6. After the model has been deployed, move onto the UI step.
7. If you want to stop the Clipper connection, execute: python3 ./inference/stop_clipper_connection.py

### 5. User Interface: 
1. Make sure that the clipper connection is available and the model has been deployed using Clipper before proceeding with the commands to view the user interface.
2. Move into the api/ folder.
    - Execute: export FLASK_APP=upload.py
    - Execute: python3 -m flask run
3. Move to the user/ folder.
    - Execute: npm install (This installs all the dependencies needed for the front-end.)
    - Execute: npm start

