# User Behaviour Analytics
[![Build Status](https://travis-ci.com/kaiiyer/UBA.svg?branch=master)](https://travis-ci.com/kaiiyer/UBA)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9c9de4eb13f54cdda0c46b91c3616eb6)](https://app.codacy.com/manual/kaiiyer47/UBA?utm_source=github.com&utm_medium=referral&utm_content=kaiiyer/UBA&utm_campaign=Badge_Grade_Dashboard)

![Python](https://alibahaari.github.io/Badge/Python.png)  ![NPM](https://alibahaari.github.io/Badge/npm.png)		![HTML](https://alibahaari.github.io/Badge/HTML.png)		![CSS](https://alibahaari.github.io/Badge/JavaScript.png)   ![JS](https://alibahaari.github.io/Badge/CSS.png)

<a href="https://github.com/kaiiyer/UBA/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/kaiiyer/UBA"></a>
<a href="https://github.com/kaiiyer/UBA/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/kaiiyer/UBA"></a>
<a href="https://github.com/kaiiyer/UBA/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/kaiiyer/UBA"></a>
<a href="https://github.com/kaiiyer/UBA/graphs/contributors" alt="Contributors">
<img src="https://img.shields.io/github/contributors/kaiiyer/UBA" /></a>

## Get the updated code & documentation on XS code [here](https://cp.xscode.com/Tormorrow-SOC/OpenUB)
Our main development, and documentation branches are first pushed to our sponsorship repository, and then eventually pushed to our public free repository. To obtain the most updated code, and documentation for OpenUBA, subscribe to our XS Code repository.

```
https://cp.xscode.com/Tormorrow-SOC/OpenUB
```

## Goals
To Build a lightweight, SIEM Agnostic, UEBA Framework focused on providing:
- Model Management
- Community-driven Model Library
- Model Versioning
- Dashboard
- Rule Storage/Management
- Case Management
- Peer-oriented/community intel
- Lightweight, SIEM-agnostic infrastructure
- Flexible/open dataset support

## Components
- Model Client (optional)
- Model Server (Remote or Local)
- Transport Client
- User Inferface

## Installation

Fork this repository (Click the Fork button in the top right of this page, click your Profile Image)
Clone your fork down to your local machine
```
git clone https://github.com/your-username/UBA.git
```
1. Install pip3 if you don't have it already
```    
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
    python3 get-pip.py     
    sudo python3 get-pip.py
```
2. Install the python dependencies
```
pip3 install requirements.txt
```
3. Install HADOOP and JDK
4. Configure Spark environment by running spark_env.sh
```
bash spark_env.sh 
OR
./spark_env.sh
```
5. Run the make file
```
make
```
6. Point your browser to localhost:3000 to view the UI and localhost:5000 for viewing the Flask app running
