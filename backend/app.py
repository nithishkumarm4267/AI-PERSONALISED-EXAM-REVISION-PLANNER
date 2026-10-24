import math
import os
import re

from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")


def get_ollama_client():
    # Ollama requires an api_key argument for OpenAI compatibility,
    # but ignores this placeholder for local requests.
    return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "provider": "Ollama local"})


@app.post("/api/topics")
def generate_topics():
    data = request.get_json(silent=True) or {}
    subject = str(data.get("subject", "")).strip()
    course_context = str(data.get("course_context", "")).strip()

    if not subject:
        return jsonify({"error": "Enter a subject name."}), 400

    try:
        client = get_ollama_client()
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You help students prepare for exams. Suggest exactly "
                        "7 concise, important study topics for the subject and "
                        "course context. Return one topic per line with no "
                        "numbering, bullets, introduction, or explanations. "
                        "If the exact syllabus is unknown, suggest general "
                        "topics and do not claim they match a specific college."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Subject: " + subject + "\nCourse context: "
                        + (course_context or "General undergraduate level")
                    ),
                },
            ],
            temperature=0.2,
            max_tokens=300,
        )

        content = response.choices[0].message.content or ""
        topics = []

        for line in content.splitlines():
            topic = re.sub(r"^\s*(?:[-*•]\s*|\d+[\).]\s*)", "", line)
            topic = topic.strip()
            if topic:
                topics.append(topic)

        topics = topics[:7]
        if not topics:
            return jsonify({"error": "The local model returned no topics."}), 502

        return jsonify({"topics": topics, "model": OLLAMA_MODEL})
    except Exception as exc:
        return jsonify({
            "error": (
                "Could not reach Ollama. Make sure Ollama is installed, "
                "running, and the qwen3:4b model has been downloaded."
            ),
            "details": str(exc),
        }), 502


@app.post("/api/plan")
def create_plan():
    data = request.get_json(silent=True) or {}

    student_name = str(data.get("student_name", "Student")).strip() or "Student"
    subject = str(data.get("subject", "")).strip()
    course_context = str(data.get("course_context", "")).strip()

    try:
        days_left = int(data.get("days_left", 0))
        hours_per_day = float(data.get("hours_per_day", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Enter valid days and study hours."}), 400

    raw_topics = data.get("topics", [])
    if not subject:
        return jsonify({"error": "Enter a subject name."}), 400
    if days_left < 1:
        return jsonify({"error": "Days until the exam must be at least 1."}), 400
    if hours_per_day <= 0:
        return jsonify({"error": "Study hours must be greater than 0."}), 400
    if not isinstance(raw_topics, list) or not raw_topics:
        return jsonify({"error": "Add at least one topic."}), 400

    topics = []
    for raw in raw_topics:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name", "")).strip()
        try:
            confidence = int(raw.get("confidence", 0))
        except (TypeError, ValueError):
            continue
        if name and 1 <= confidence <= 5:
            topics.append({"name": name, "confidence": confidence})

    if not topics:
        return jsonify({"error": "Each topic needs a confidence score from 1 to 5."}), 400

    topics.sort(key=lambda item: item["confidence"])
    topics_per_day = math.ceil(len(topics) / days_left)

    lines = [
        "Study timetable for " + student_name,
        "Subject: " + subject,
        "Course context: " + (course_context or "Not provided"),
        "Days until the exam: " + str(days_left),
        "",
    ]
    schedule = []

    for day in range(days_left):
        start = day * topics_per_day
        todays_topics = topics[start:start + topics_per_day]

        if todays_topics:
            average_confidence = sum(
                item["confidence"] for item in todays_topics
            ) / len(todays_topics)

            study_percentage = 0.5 + (5 - average_confidence) * 0.075
            topic_study_hours = hours_per_day * study_percentage
            revision_hours = hours_per_day - topic_study_hours
            total_weight = sum(
                6 - item["confidence"] for item in todays_topics
            )

            day_topics = []
            lines.append("Day " + str(day + 1) + ":")

            for item in todays_topics:
                weight = 6 - item["confidence"]
                allocated_hours = round(
                    topic_study_hours * weight / total_weight, 1
                )
                day_topics.append({
                    "name": item["name"],
                    "confidence": item["confidence"],
                    "study_hours": allocated_hours,
                })
                lines.append(
                    "  - " + item["name"]
                    + " (confidence: " + str(item["confidence"]) + "/5, "
                    + "study: " + format(allocated_hours, ".1f") + " hours)"
                )

            lines.append(
                "  Quick revision: "
                + format(revision_hours, ".1f") + " hours"
            )
            schedule.append({
                "day": day + 1,
                "topics": day_topics,
                "revision_hours": round(revision_hours, 1),
            })
        else:
            lines.append("Day " + str(day + 1) + ": Revision and practice")
            lines.append(
                "  Study time: " + format(hours_per_day, ".1f") + " hours"
            )
            schedule.append({
                "day": day + 1,
                "topics": [],
                "revision_hours": round(hours_per_day, 1),
            })

        lines.append("")

    safe_subject = re.sub(r"[^A-Za-z0-9_-]+", "_", subject).strip("_")
    filename = "study_plan_" + (safe_subject or "subject") + ".txt"

    return jsonify({
        "schedule": schedule,
        "plan_text": "\n".join(lines),
        "filename": filename,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
