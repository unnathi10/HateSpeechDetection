# Detection of Hate Speech Detection in Videos Using Machine Learning
[Master's Project]

### Objective:
To detect hate speech in videos based on the spoken content of the videos using machine learning.

### Approach:
* Extract audio from video using FFmpeg API
* Convert audio to text transcript using Google Cloud Speech-to-Text API
* Extract features to get word counts, frequency of word counts, uni-grams and bi-grams
* Train Naive Bayes, Linear SVM, Random Forrest and RNN models
* Compute Accuracy, Precision score, Recall score, F1 score

### Dataset:
* YouTube videos are searched and downloaded using a YouTube crawler
* Videos are searched using the 'search by keyword' function provided by YouTube Data API 
* Searched videos are downloaded using Pytube library
* Each video is labeled as Normal or Hateful (Racist, Sexist)

### Language Used:
* Python

### Tools Used:
* YouTube Data API
* FFmpeg API
* Google Cloud Speech-to-Text API
* Google Storage Bucket
* Jupyter Notebook

Note: You can view .ipynb files using nbviewer - https://nbviewer.jupyter.org/
