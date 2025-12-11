from django.urls import path
from .views import (
    CNNAudioPredict,
    CRNNAudioPredict,
    KNNAudioPredict,
    SVMAudioPredict,
    RFAudioPredict,
    FeedbackIncorrectView,
    FeedbackCorrectView,
)

urlpatterns = [
    path("predict/cnn/", CNNAudioPredict.as_view(), name="predict-cnn"),
    path("predict/crnn/", CRNNAudioPredict.as_view(), name="predict-crnn"),
    path("predict/knn/", KNNAudioPredict.as_view(), name="predict-knn"),
    path("predict/svm/", SVMAudioPredict.as_view(), name="predict-svn"),
    path("predict/rf/", RFAudioPredict.as_view(), name="predict-rf"),
    path("feedback/correct/", FeedbackCorrectView.as_view(), name="feedback-correct"),
    path("feedback/incorrect/", FeedbackIncorrectView.as_view(), name="feedback-incorrect"),

]
