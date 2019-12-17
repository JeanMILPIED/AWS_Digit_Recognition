# AWS_Digit_Recognition
## set-up the AWS structure to train your digit recognition NN and apply  it through hand written digits in an API

### OBJECTIVE: PUTTING Live your Digit recognition POC
In a summary, what you will do in this project is :
- Create an instance
- Build a digit recognition model
- Store it on a webpage 
- Deploy it in a server
 
So you will set-up 3 different machines. They are described hereunder with a summary of the steps:
1. Machine1
a. Install Jupyter
b. Train model and save the model (NN) (option: play with it)
c. We will use Keras and Tensorflow
d. Once done it can be turned down
    
2. Machine2: Webserver in public
a. Deploy the web app
b. This is the FRONT END machine
c. we will use a basic Apache Server
    
3. Machine3: (in the public w/o public IP or properly within the private subnet)
a. BACK END machine
b. It stores the model and it does the prediction
c. Runs the application and send prediction to front end
d. Back end in python : FLASK (equivalent to NodeJS) . (note: Not recommended to use a python back end except for POC)

Note: why having 3 machines ? Because it keeps things clean with separated tasks in each machines.

We use the MNIST dataset of hand digits (50k train and 10k test)
http://yann.lecun.com/exdb/mnist/
The webapp will allow the user to draw a number with the mouse and the model will recognize it
All the data are in this git-hub
M5.xlarge to use for training the model

## details of instances set-up
### Machine1
- chose an UBUNTU server free tier instance 18.04 with a 
```Sudo apt-get install git```
```Git clone ("the clone adress of the full git_hub repository")```
- This will install all the environment
```Pip install -r ./AWS_Tutorials/MNIST/requirements.txt```
See all the command lines at 
https://github.com/leodsti/AWS_Tutorials/blob/master/MNIST/Command%20to%20makes%20things%20work.txt

Then you go on the notebook, chose the right kernel and launch the notebook

Notes of the notebook
- Keras is a framework that codes another framework which is tensorflow
- Keras makes your life easier in building NN
- It does not work with pytorch yet
- It tries to predict 10 classes
- Epoch 10 => we are changing the values 10 times

### Machine2
- Launch instance ubuntu 18.04 free Tier
- Install appache
```sudo apt install apache2```
- https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04
```sudo ufw allow 'Apache'```
- note:ctrl-C to get out of Apache
- Put the files (index.html, index.js, style.css on the machine and make run
  
```
Mkdir static
ssh -i "JM_Keypair.pem" ubuntu@3.226.235.17 
scp -i "JM_Keypair.pem" "index.js" ubuntu@3.226.235.17:/home/ubuntu/static/index.js 
scp -i "JM_Keypair.pem" "index.js" ubuntu@3.226.235.17:/home/ubuntu/static 
scp -i "JM_Keypair.pem" "index.js" ubuntu@3.226.235.17:/home/ubuntu/static/index.js 
scp -i "JM_Keypair.pem" "style.css" ubuntu@3.226.235.17:/home/ubuntu/static/style.css 
scp -i "JM_Keypair.pem" "index.html" ubuntu@3.226.235.17:/home/ubuntu/index.html
```
	
- Put the right files in the right folders
```
19  sudo mkdir /var/www/html/static
20  sudo cp -i /home/ubuntu/index.html /var/www/html
26  sudo cp -i /home/ubuntu/static/index.js /var/www/html/static
27  sudo cp -i /home/ubuntu/static/style.css /var/www/html/static ```
28  sudo systemctl reload apache2
``` 
	
Now if you connect at the public IP adress, you have : 
	   


### Machine3
- EC2 instance Ubuntu 18.04 with 20Go storage memory
- Connect and update
- To solve package incompatibilities, we install conda back and use a virtual environment
- We follow all the steps hereunder:
```	
1  sudo apt-get update
2  python3
3  wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
4  sudo bash Anaconda3-2019.03-Linux-x86_64.sh
5  exit
6  conda create -n my_flask_env python=3.6
7  conda activate my_flask_env
8  conda install -c anaconda flask
9  Conda install opencv
10  conda install opencv
11  conda install keras
12  history
13  conda deactivate
14  sudo apt-get install git
15  git clone https://github.com/leodsti/AWS_Tutorials.git
16  ls
17  history
18  conda activate my_flask_env
19  conda install -r ./AWS_Tutorials/MNIST/requirements.txt
20  pip3 install -r ./AWS_Tutorials/MNIST/requirements.txt
21  pip install -r ./AWS_Tutorials/MNIST/requirements.txt
22  cd
23  ls
24  cd AWS_Tutorials
25  ls
26  cd MNIST
27  python3 keras_flask.py
28  sudo vi keras_flask.py
47  history
```

And we modify the python script for keras_flask.py as follow (we use both PIL and keras.preprocessing packages)
you can find the python script in this github

```
def loadImage(filename):
	img_rows = img_cols = 28
	img = Image.open(filename).convert('L')
	img_1 = img.resize((28,28),Image.NEAREST)
	print(img_1.size)
	img_2 = image.img_to_array(img_1)
	print(img_2.size)
	#.reshape(img_1.size[1], img_1.size[0])
	img_2 = img_2 / 255
	# Reshape from (28,28) to (1,28,28,1) : 1 sample, 28x28 pixels, 1 channel (B/W)
	img_3 = np.expand_dims(img_2, axis=0)
	img_3 = np.expand_dims(img_3, axis=0)
	img_4 = np.reshape(img_3, (1,img_cols,img_rows,1))
	return np.array(img_4)
```

It works!

# you can then connect via the public IP adress of your API
	
	
