from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import InterviewSession, Question, Answer
from .serializers import QuestionSerializer
from django.shortcuts import get_object_or_404


def generate_questions(role):
    if role.lower() == "python developer":
        return [
            "What is OOP in Python?",
            "Explain Django architecture.",
            "What is REST API?",
            "Difference between list and tuple?",
            "What is virtual environment?"
        ]
    else:
        return [
            "Tell me about yourself.",
            "What are your strengths?",
            "Why should we hire you?"
        ]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_interview(request):
    role = request.data.get("role")

    session = InterviewSession.objects.create(
        user=request.user,
        role=role
    )

    questions_list = generate_questions(role)

    created_questions = []

    for q in questions_list:
        question = Question.objects.create(
            session=session,
            text=q
        )
        created_questions.append(question)

    serializer = QuestionSerializer(created_questions, many=True)

    return Response(serializer.data)


def calculate_score(answer_text):
    keywords = ["python", "django", "api", "oop"]
    score = 0

    for word in keywords:
        if word in answer_text.lower():
            score += 25

    return score


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    question_id = request.data.get("question_id")
    answer_text = request.data.get("answer")

    question = get_object_or_404(Question, id=question_id)

    score = calculate_score(answer_text)

    answer = Answer.objects.create(
        question=question,
        text=answer_text,
        score=score
    )

    # Update total score in session
    session = question.session
    session.total_score += score
    session.save()

    return Response({
        "message": "Answer submitted",
        "score": score,
        "total_score": session.total_score
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def interview_history(request):
    sessions = InterviewSession.objects.filter(user=request.user).order_by("-created_at")

    data = []

    for session in sessions:
        data.append({
            "id": session.id,
            "role": session.role,
            "total_score": session.total_score,
            "created_at": session.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return Response(data)

from django.db.models import Avg, Max

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    sessions = InterviewSession.objects.filter(user=request.user)

    total_interviews = sessions.count()
    average_score = sessions.aggregate(avg=Avg("total_score"))["avg"] or 0
    highest_score = sessions.aggregate(max=Max("total_score"))["max"] or 0

    return Response({
        "total_interviews": total_interviews,
        "average_score": average_score,
        "highest_score": highest_score
    })

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User created successfully"})