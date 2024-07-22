# Task-3: Integrated Speech Recognition and Intent Classification for Robot Control

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [Dataset](#dataset)
- [Tools and Technologies](#tools-and-technologies)
- [Results](#results)
- [Conclusion](#conclusion)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Speech-to-Text Conversion**: Utilizes the Wav2Vec2 model for transcribing speech, including Indian English accents.
- **Intent Classification**: Uses a BERT-based model trained on the CLINC150 dataset for classifying intents from transcribed text.
- **Distance Extraction**: Extracts distance measurements from spoken instructions.
- **Live Audio Recording**: Implements real-time audio recording for immediate processing.
- **Multi-Accent Support**: Specifically tuned for Indian English accents using the AI4Bharat dataset.

## Prerequisites
- Python 3.x
- PyAudio
- torchaudio
- transformers
- scikit-learn
- word2number
- scipy
- numpy

## Setup and Installation

### Clone the Repository
```bash
git clone https://github.com/vikramkumar402/Task-3-Speech-Intent-Classification.git
cd Task-3-Speech-Intent-Classification
```

### Installation
Install the required Python packages:

```bash
pip install pyaudio torchaudio transformers scikit-learn word2number scipy numpy
```

## Running the Project

1. **Start the Audio Recording Script**:
   ```bash
   python audio_recorder.py
   ```
   This script allows you to record audio samples for processing.

2. **Open the Google Colab Notebook**:
   Click the button below to open the project notebook in Google Colab:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1P24iMF6WaomwNw9tCxfrBAta4iLzngrO?usp=sharing)

3. **Run the Cells**:
   Execute the cells in order to set up the environment, train the model, and process audio.

4. **Upload and Process Audio**:
   Use the file upload feature in the notebook to process your recorded audio files.

## Dataset
This project utilizes two main datasets:

1. **CLINC150**: Used for training the intent classification model.
   - Contains a wide variety of intents for general language understanding.

2. **AI4Bharat-NPTEL2020-Indian-English-Speech-Dataset**: 
   - Used for fine-tuning and testing the speech recognition model on Indian English accents.
   - Specifically using the "Pure-Set" subset for diverse accent coverage.

## Tools and Technologies

| Area                  | Tool/Technology           | Description                                    |
| --------------------- | ------------------------- | ---------------------------------------------- |
| Speech Recognition    | Wav2Vec2                  | For accurate speech-to-text conversion         |
| Intent Classification | BERT                      | For classifying intents from transcribed text  |
| Audio Processing      | PyAudio, torchaudio       | For recording and processing audio             |
| Natural Language      | Transformers, word2number | For text processing and number extraction      |
| Machine Learning      | PyTorch, scikit-learn     | For model training and evaluation              |
| Data Handling         | NumPy, SciPy              | For numerical operations and data manipulation |

## Results

The intent classification model achieved the following performance on the test set:

- **Test Accuracy: 88.3636%**

This high accuracy demonstrates the model's strong capability in classifying intents from transcribed speech.

## Conclusion
This integrated system demonstrates the capability to process spoken instructions, particularly in Indian English accents, and extract meaningful intents and parameters for robot control. The combination of Wav2Vec2 for speech recognition and BERT for intent classification provides a robust pipeline for understanding and acting upon vocal commands.

## Contributing
Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Vikram Kumar - vikramk.ug22.cs@nitp.ac.in

LinkedIn: [linkedin.com/in/vikramkumar2510/](https://www.linkedin.com/in/vikramkumar2510/)

Project Link: [https://github.com/vikramkumar402/Task-3-Speech-Intent-Classification](https://github.com/vikramkumar402/Task-3-Speech-Intent-Classification)
