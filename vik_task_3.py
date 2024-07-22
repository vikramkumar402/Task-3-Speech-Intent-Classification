# -*- coding: utf-8 -*-
"""vik-task-3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QDZ-8GcnpFIO5URkojgRzqjSOUoI3LnW
"""

# Cell 1: Install required libraries
!pip install transformers torchaudio jiwer datasets torch scikit-learn word2number

# Cell 2: Import necessary libraries
import os
import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, BertModel, BertTokenizer
from datasets import load_dataset
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import re
from tqdm.notebook import tqdm
from google.colab import drive
import tarfile
from IPython.display import Audio
from word2number import w2n

# Cell 3: Mount Google Drive and extract the Indian accent dataset
drive.mount('/content/drive')
tar_path = '/content/drive/My Drive/VIKRAM-DRDO/nptel-pure-set.tar.gz'
extraction_path = '/content/nptel-pure-set'
if not os.path.exists(extraction_path):
    os.makedirs(extraction_path)
with tarfile.open(tar_path, 'r:gz') as tar:
    tar.extractall(path=extraction_path)
print('Extraction completed.')

# Cell 4: Define the ASR (Automatic Speech Recognition) module
class ASRModule:
    def __init__(self, model_name="facebook/wav2vec2-large-960h-lv60-self"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)

    def transcribe(self, waveform, sample_rate):
        if waveform.ndim > 1:
            waveform = waveform.mean(dim=0)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
        inputs = self.processor(waveform, sampling_rate=16000, return_tensors="pt", padding=True)
        inputs = inputs.input_values.to(self.device)
        with torch.no_grad():
            logits = self.model(inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])
        return transcription

asr_module = ASRModule()

# Cell 5: Define the Intent Classifier model
class IntentClassifier(nn.Module):
    def __init__(self, num_intents):
        super(IntentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_intents)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits

# Cell 6: Define the Data Processor
class DataProcessor:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.le = LabelEncoder()

    def load_clinc150(self):
        dataset = load_dataset("clinc_oos", "plus")
        train_data = dataset['train']
        test_data = dataset['test']

        X_train = train_data['text']
        y_train = self.le.fit_transform(train_data['intent'])
        X_test = test_data['text']
        y_test = self.le.transform(test_data['intent'])

        return X_train, y_train, X_test, y_test, self.le.classes_

    def load_indian_accent_data(self, base_path):
        dataset = []
        wav_directory = os.path.join(base_path, 'nptel-pure', 'wav')
        txt_directory = os.path.join(base_path, 'nptel-pure', 'corrected_txt')
        for filename in os.listdir(wav_directory):
            if filename.lower().endswith('.wav'):
                audio_path = os.path.join(wav_directory, filename)
                transcript_path = os.path.join(txt_directory, filename.replace('.wav', '.txt'))
                try:
                    waveform, sample_rate = torchaudio.load(audio_path)
                    with open(transcript_path, 'r') as file:
                        transcript = file.read().strip()
                    if transcript:
                        dataset.append((waveform, sample_rate, transcript))
                except Exception as e:
                    print(f"Failed to load or process file {filename}: {e}")
        return dataset

    def prepare_intent_data(self, texts, labels):
        encodings = self.tokenizer(texts, truncation=True, padding=True, max_length=128, return_tensors="pt")
        dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'], torch.tensor(labels))
        return DataLoader(dataset, batch_size=16, shuffle=True)

data_processor = DataProcessor()

# Cell 7: Define utility functions
def extract_distances(instruction):
    pattern = r'(\w+|\d+)\s*(meter|metre|m|feet|ft)'
    matches = re.findall(pattern, instruction, re.IGNORECASE)
    distances = []
    for match in matches:
        try:
            number = w2n.word_to_num(match[0])
        except ValueError:
            try:
                number = float(match[0])
            except ValueError:
                continue
        distances.append(number)
    return distances

# Cell 8: Load and prepare CLINC150 data for intent classification
X_train, y_train, X_test, y_test, intents = data_processor.load_clinc150()
train_loader = data_processor.prepare_intent_data(X_train, y_train)
test_loader = data_processor.prepare_intent_data(X_test, y_test)

print(f"Number of intents: {len(intents)}")
print(f"Number of training samples: {len(X_train)}")
print(f"Number of test samples: {len(X_test)}")

# Cell 9: Initialize and train intent classifier
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
intent_classifier = IntentClassifier(len(intents)).to(device)
optimizer = torch.optim.AdamW(intent_classifier.parameters(), lr=2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

num_epochs = 5
for epoch in range(num_epochs):
    intent_classifier.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
        input_ids, attention_mask, labels = [b.to(device) for b in batch]
        optimizer.zero_grad()
        outputs = intent_classifier(input_ids, attention_mask)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch+1}/{num_epochs}, Average Loss: {avg_loss:.4f}")

print("Training completed")

# Cell 10: Evaluate the intent classifier
intent_classifier.eval()
correct = 0
total = 0
with torch.no_grad():
    for batch in tqdm(test_loader, desc="Evaluating"):
        input_ids, attention_mask, labels = [b.to(device) for b in batch]
        outputs = intent_classifier(input_ids, attention_mask)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.4f}%")

# Cell 11: Load Indian accent data
indian_accent_data = data_processor.load_indian_accent_data(extraction_path)
print(f"Loaded {len(indian_accent_data)} Indian accent audio samples")

# Cell 12: Function to process audio and classify intent
def process_instruction(audio_waveform, sample_rate):
    transcription = asr_module.transcribe(audio_waveform, sample_rate)
    encoding = data_processor.tokenizer(transcription, return_tensors='pt', padding=True, truncation=True, max_length=128)
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = intent_classifier(input_ids, attention_mask)

    _, pred = torch.max(outputs, dim=1)
    intent = intents[pred.item()]
    distances = extract_distances(transcription)

    return f"Transcription: {transcription}\nIntent: {intent}\nDistances: {distances}"

# Cell 13: Test with Indian accent data
for waveform, sample_rate, _ in indian_accent_data[:5]:
    result = process_instruction(waveform, sample_rate)
    print(result)
    print('-' * 50)

!pip install scipy numpy

# Cell 14: Main processing loop for user-uploaded audio
from google.colab import files
import scipy.io.wavfile as wavfile
import numpy as np

print("Audio File Processing")
print("Upload a WAV file with your spoken instruction.")

while True:
    uploaded = files.upload()
    if not uploaded:
        print("No file was uploaded.")
        break

    file_name = list(uploaded.keys())[0]
    sample_rate, audio = wavfile.read(file_name)
    audio = audio.astype(np.float32) / 32768.0

    print(f"Audio shape: {audio.shape}, Sample rate: {sample_rate}")
    display(Audio(audio, rate=sample_rate))

    result = process_instruction(torch.from_numpy(audio), sample_rate)
    print("\nResult:")
    print(result)
    print('-' * 50)

    choice = input("Do you want to process another audio file? (yes/no): ")
    if choice.lower() != 'yes':
        break

print("Processing completed.")