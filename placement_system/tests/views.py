from django.shortcuts import render, redirect
from .models import Question, Topic, Result, Company
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from users.models import StudentProfile
import json
from .models import Company, CompanyTest

@login_required
def start_test(request, topic_id):

    # Check if student profile exists
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return render(request, "not_approved.html")

    # Check approval status
    if not profile.approved:
        return render(request, "not_approved.html")

    topic = Topic.objects.get(id=topic_id)
    questions = Question.objects.filter(topic=topic)

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_answer:
                score += 1

        Result.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total_questions=total
        )

        return render(request, "result.html", {
            "score": score,
            "total": total,
            "topic": topic
        })

    return render(request, "start_test.html", {
        "topic": topic,
        "questions": questions
    })


@login_required
def dashboard(request):
    results = Result.objects.filter(user=request.user)

    total_tests = results.count()

    if total_tests > 0:
        average_score = results.aggregate(Avg('score'))['score__avg']
    else:
        average_score = 0

    weak_topics = []
    topic_labels = []
    topic_scores = []

    for result in results:
        percentage = (result.score / result.total_questions) * 100

        topic_labels.append(result.topic.name)
        topic_scores.append(round(percentage, 2))

        if percentage < 40:
            weak_topics.append(result.topic.name)

    readiness_score = average_score * 10 if average_score else 0

    # ✅ Company-wise Analysis (MUST be inside function)
    companies = Company.objects.all()
    company_analysis = []

    for company in companies:
        required = company.required_topics.all()
        total_required = required.count()

        if total_required == 0:
            continue

        score_sum = 0
        counted = 0

        for topic in required:
            result = results.filter(topic=topic).first()
            if result:
                percentage = (result.score / result.total_questions) * 100
                score_sum += percentage
                counted += 1

        if counted > 0:
            readiness = round(score_sum / counted, 2)
        else:
            readiness = 0

        company_analysis.append({
            "company": company.name,
            "readiness": readiness
        })

    return render(request, "dashboard.html", {
        "results": results,
        "average_score": average_score,
        "weak_topics": weak_topics,
        "readiness_score": readiness_score,
        "topic_labels": json.dumps(topic_labels),
        "topic_scores": json.dumps(topic_scores),
        "company_analysis": company_analysis,
    })


@login_required
def topic_list(request):
    topics = Topic.objects.all()
    return render(request, "topics.html", {"topics": topics})


@login_required
def company_test_list(request):
    companies = Company.objects.all()
    return render(request, "company_test_list.html", {"companies": companies})


@login_required
def company_start_test(request, company_id):
    company = Company.objects.get(id=company_id)
    questions = CompanyTest.objects.filter(company=company)
    print("Company:", company)
    print("Question count:", questions.count())

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_answer:
                score += 1

        return render(request, "company_result.html", {
            "company": company,
            "score": score,
            "total": total
        })

    return render(request, "company_start_test.html", {
        "company": company,
        "questions": questions
    })