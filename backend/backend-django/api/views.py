import os
from rest_framework.views import APIView
from rest_framework.response import Response

import os
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    CNN,
    CRNN,
    SVMClassifier,
    KNNClassifier,
    RandomForestModel
)

from .utils.preprocess import (
    extract_feature_vector,
)


# -----------------------------------
# Helper to save uploaded file
# -----------------------------------
def save_uploaded_file(file):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    save_path = os.path.join(settings.MEDIA_ROOT, file.name)
    with open(save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return save_path


# -----------------------------------
# CNN
# -----------------------------------

class CNNAudioPredict(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        save_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(save_path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        cnn_model = CNN()
        # Load model only, don't retrain
        cnn_model.analyze()  # ensures model is loaded

        # Use predict_user_song for actual prediction
        label = cnn_model.predict_user_song(save_path)
        if not label:
            return Response({"error": "Prediction failed"}, status=500)

        # return Response({"label": label})
        cnn_model = CNN()
        accuracy, _ = cnn_model.analyze()  # get model accuracy
        label, confidence = cnn_model.predict_user_song(save_path)

        return Response({
            "model_name": "CNN",
            "predicted_label": label,
            "model_overall_accuracy": accuracy,
            "prediction_confidence": confidence,
            "file_id": os.path.basename(save_path)
        })


# -----------------------------------
# CRNN
# -----------------------------------
class CRNNAudioPredict(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        save_path = save_uploaded_file(file)

        crnn_model = CRNN()
        accuracy = crnn_model.analyze()
        label, confidence = crnn_model.predict_user_song(save_path)

        return Response({
            "model_name": "CRNN",
            "predicted_label": label,
            "model_overall_accuracy": accuracy,
            "prediction_confidence": confidence,
            "file_id": os.path.basename(save_path)
        })


# -----------------------------------
# SVM
# -----------------------------------
class SVMAudioPredict(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        save_path = save_uploaded_file(file)

        feat = extract_feature_vector(save_path)
        if feat is None:
            return Response({"error": "Audio processing failed"}, status=500)

        svm_model = SVMClassifier()
        accuracy = svm_model.analyze()
        label, confidence = svm_model.predict_user_song(feat)

        return Response({
            "model_name": "SVM",
            "predicted_label": label,
            "model_overall_accuracy": accuracy,
            "prediction_confidence": confidence,
            "file_id": os.path.basename(save_path)
        })


# -----------------------------------
# KNN
# -----------------------------------
class KNNAudioPredict(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        save_path = save_uploaded_file(file)

        feat = extract_feature_vector(save_path)
        if feat is None:
            return Response({"error": "Audio processing failed"}, status=500)

        knn_model = KNNClassifier()
        accuracy = knn_model.analyze()
        label, confidence = knn_model.predict_user_song(feat)

        return Response({
            "model_name": "KNN",
            "predicted_label": label,
            "model_overall_accuracy": accuracy,
            "prediction_confidence": confidence,
            "file_id": os.path.basename(save_path)
        })


# -----------------------------------
# RANDOM FOREST
# -----------------------------------
class RFAudioPredict(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        save_path = save_uploaded_file(file)

        feat = extract_feature_vector(save_path)
        if feat is None:
            return Response({"error": "Audio processing failed"}, status=500)

        rf_model = RandomForestModel()
        accuracy = rf_model.analyze()
        label, confidence = rf_model.predict_user_song(feat)

        return Response({
            "model_name": "RandomForest",
            "predicted_label": label,
            "model_overall_accuracy": accuracy,
            "prediction_confidence": confidence,
            "file_id": os.path.basename(save_path)
        })

@method_decorator(csrf_exempt, name="dispatch")
class FeedbackCorrectView(View):
    """
    User confirms prediction was correct.
    We do nothing but log/return success.
    """
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            file_id = data.get("file_id")

            if not file_id:
                return JsonResponse({"error": "file_id missing"}, status=400)

            return JsonResponse({
                "message": "Prediction confirmed as correct.",
                "file_id": file_id
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class FeedbackIncorrectView(View):
    """
    User confirms prediction was wrong → delete uploaded file from media/
    """
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            file_id = data.get("file_id")

            if not file_id:
                return JsonResponse({"error": "file_id missing"}, status=400)

            file_path = os.path.join(settings.MEDIA_ROOT, file_id)

            if os.path.exists(file_path):
                os.remove(file_path)
                deleted = True
            else:
                deleted = False

            return JsonResponse({
                "message": "Prediction marked incorrect. File deleted." if deleted else "File not found.",
                "file_deleted": deleted,
                "file_id": file_id
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
