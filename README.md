# Facegen Repo (Scattered Ideas)

This repository contains the code and instructions for setting up and running the Facegen project.

## Overview

- The elevenlabs script will give you a dose of what generative speech sounds like (you can choose to use the API and get billed for further usage)
- The whisperlargev3 script uses the openai whisper v3 model weights to perform cutting-edge speech-to-text conversion
- landmarks.py creates a facemesh based on your camera in real-time

## Setup and Installation

To get started, clone the repository and set up a virtual environment:

```bash
git clone https://github.com/Infatoshi/facegen
cd facegen
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
