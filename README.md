# HAL 9000 (2001: A Space Odyssey)

> Good afternoon, gentlemen. I am a HAL 9000 computer.
I became operational at the H.A.L. plant in Urbana, Illinois on the
12th of January 1992.
 
## Table of Contents

* [Inspiration](#inspiration)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Running the Program](#running-the-program)
* [Demo Video](#demo-video)
* [Photo Gallery](#photo-gallery)

## Inspiration

[![HAL 9000 Playing Chess](https://img.youtube.com/vi/2SCsz8kYu5s/0.jpg)](https://youtu.be/2SCsz8kYu5s)

## Prerequisites

- You have a working Linux environment with a microphone, speakers, and monitor.
  - For our demo, we host the project on a Beagle-YAI
- You have cloned this repository and are in the root
- You have installed Python

## Setup

1. Run the following commands in the terminal
```
sudo apt install Stockfish
sudo apt install alsa-utils  
sudo apt install python3-pyaudio alsa-utils  
sudo apt install portaudio19-dev python3-all-dev  
sudo apt-get install flac
```
2. Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
3. Install Python dependencies  
`pip install -r requirements.txt`

## Running the Program
1. `python hal.py`  
2. In the output console, there will be an IP and port. Navigate to that link in your web browser to access the chess GUI.

## Demo Video

[![HAL 9000 Demo](https://img.youtube.com/vi/CTExVcBcNeg/0.jpg)](https://youtu.be/CTExVcBcNeg)

## Photo Gallery

<p>
  <img src="https://i.imgur.com/0dO9HDE.jpeg" width="500">
  <br>
  <b>Outer Shell</b>
</p>

<p>
  <img src="https://i.imgur.com/bVwEBZw.jpeg" width="500">
  <br>
  <b>Hosted on Beagle-YAI</b>
</p>

<p>
  <img src="https://i.imgur.com/8fs024E.jpeg" width="500">
  <br>
  <b>Inside setup with Beagle and cables</b>
</p>

<p>
  <img src="https://i.imgur.com/qq93yoP.jpeg" width="500">
  <br>
  <b>Full setup with HAL and GUI</b>
</p>