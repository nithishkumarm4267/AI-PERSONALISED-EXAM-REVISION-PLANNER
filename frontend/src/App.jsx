import { useState } from "react";

const initialForm = {
  student_name: "",
  subject: "",
  course_context: "B.Tech AI & Data Science",
  days_left: 7,
  hours_per_day: 1,
};

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [topics, setTopics] = useState([]);
  const [manualText, setManualText] = useState("");
  const [manualMode, setManualMode] = useState(false);
  const [plan, setPlan] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  function updateForm(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function suggestTopics(event) {
    event.preventDefault();
    setError("");
    setPlan(null);
    setTopics([]);
    setManualMode(false);
    setBusy(true);

    try {
      const response = await fetch("/api/topics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject: form.subject,
          course_context: form.course_context,
        }),
      });
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Could not generate topics.");
      }

      setTopics(
        result.topics.map((name) => ({ name, confidence: 3 }))
      );
    } catch (err) {
      setError(err.message + " You can enter topics manually below.");
      setManualMode(true);
    } finally {
      setBusy(false);
    }
  }

  function useManualTopics() {
    const names = manualText
      .split(/\r?\n/)
      .map((name) => name.trim())
      .filter(Boolean);

    if (names.length === 0) {
      setError("Enter at least one topic, one topic per line.");
      return;
    }

    setTopics(names.map((name) => ({ name, confidence: 3 })));
    setError("");
    setManualMode(false);
  }

  function updateConfidence(index, value) {
    setTopics((current) =>
      current.map((topic, topicIndex) =>
        topicIndex === index
          ? { ...topic, confidence: Number(value) }
          : topic
      )
    );
  }

  async function createPlan() {
    setError("");
    setBusy(true);

    try {
      const response = await fetch("/api/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          days_left: Number(form.days_left),
          hours_per_day: Number(form.hours_per_day),
          topics,
        }),
      });
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Could not create the timetable.");
      }

      setPlan(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  function downloadPlan() {
    if (!plan) return;

    const file = new Blob([plan.plan_text], {
      type: "text/plain;charset=utf-8",
    });
    const url = URL.createObjectURL(file);
    const link = document.createElement("a");
    link.href = url;
    link.download = plan.filename;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="page-shell">
      <header className="topbar">
        <a className="brand" href="#">
          <span className="brand-mark">R</span>
          <span>Revision Planner</span>
        </a>
        <span className="local-badge">
          <span className="status-dot" />
          Local AI planner
        </span>
      </header>

      <section className="hero">
        <p className="eyebrow">STUDY SMARTER</p>
        <h1>Your exam plan,<br />built around you.</h1>
        <p className="hero-copy">
          Add your subject and exam details. The local AI suggests topics,
          then your confidence scores shape the revision timetable.
        </p>
      </section>

      <section className="planner-card">
        <div className="section-heading">
          <span className="step-number">01</span>
          <div>
            <h2>Exam details</h2>
            <p>Tell us what you are preparing for.</p>
          </div>
        </div>

        <form onSubmit={suggestTopics}>
          <div className="form-grid">
            <label>
              Your name
              <input
                name="student_name"
                value={form.student_name}
                onChange={updateForm}
                placeholder="e.g. Nithish"
              />
            </label>
            <label>
              Subject
              <input
                name="subject"
                value={form.subject}
                onChange={updateForm}
                placeholder="e.g. Data Structures"
                required
              />
            </label>
            <label className="wide-field">
              Course or syllabus context
              <input
                name="course_context"
                value={form.course_context}
                onChange={updateForm}
                placeholder="e.g. B.Tech AI & Data Science, Semester 3"
              />
            </label>
            <label>
              Days until exam
              <input
                name="days_left"
                type="number"
                min="1"
                value={form.days_left}
                onChange={updateForm}
                required
              />
            </label>
            <label>
              Study hours per day
              <input
                name="hours_per_day"
                type="number"
                min="0.1"
                step="0.1"
                value={form.hours_per_day}
                onChange={updateForm}
                required
              />
            </label>
          </div>

          <button className="primary-button" type="submit" disabled={busy}>
            {busy ? "Getting topics..." : "Suggest topics with local AI"}
            <span aria-hidden="true">→</span>
          </button>
        </form>

        {error && <div className="notice">{error}</div>}

        {manualMode && (
          <div className="manual-panel">
            <label>
              Enter topics, one per line
              <textarea
                rows="6"
                value={manualText}
                onChange={(event) => setManualText(event.target.value)}
                placeholder={"Arrays\nLinked lists\nStacks\nQueues"}
              />
            </label>
            <button
              className="secondary-button"
              type="button"
              onClick={useManualTopics}
            >
              Use these topics
            </button>
          </div>
        )}

        {topics.length > 0 && (
          <section className="topics-panel">
            <div className="section-heading compact-heading">
              <span className="step-number">02</span>
              <div>
                <h2>Review your topics</h2>
                <p>Set your confidence from 1 (low) to 5 (high).</p>
              </div>
            </div>

            <div className="topic-list">
              {topics.map((topic, index) => (
                <div className="topic-row" key={topic.name + index}>
                  <span className="topic-index">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span className="topic-name">{topic.name}</span>
                  <label className="confidence-control">
                    <span>Confidence</span>
                    <select
                      value={topic.confidence}
                      onChange={(event) =>
                        updateConfidence(index, event.target.value)
                      }
                    >
                      {[1, 2, 3, 4, 5].map((score) => (
                        <option key={score} value={score}>
                          {score} / 5
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              ))}
            </div>

            <button
              className="primary-button"
              type="button"
              onClick={createPlan}
              disabled={busy}
            >
              {busy ? "Building your timetable..." : "Create my timetable"}
              <span aria-hidden="true">→</span>
            </button>
          </section>
        )}
      </section>

      {plan && (
        <section className="plan-card">
          <div className="plan-heading">
            <div>
              <p className="eyebrow">YOUR PERSONAL PLAN</p>
              <h2>{form.subject} revision timetable</h2>
            </div>
            <button className="secondary-button" onClick={downloadPlan}>
              Download .txt
            </button>
          </div>

          <div className="schedule">
            {plan.schedule.map((day) => (
              <article className="day-card" key={day.day}>
                <div className="day-label">DAY {day.day}</div>
                {day.topics.length > 0 ? (
                  <>
                    {day.topics.map((topic) => (
                      <div className="scheduled-topic" key={topic.name}>
                        <span>{topic.name}</span>
                        <strong>{topic.study_hours.toFixed(1)} h</strong>
                      </div>
                    ))}
                    <div className="revision-line">
                      Quick revision <span>{day.revision_hours.toFixed(1)} h</span>
                    </div>
                  </>
                ) : (
                  <div className="revision-only">
                    Revision and practice
                    <span>{day.revision_hours.toFixed(1)} h</span>
                  </div>
                )}
              </article>
            ))}
          </div>
        </section>
      )}

      <footer>
        <span>AI Personalised Exam Revision Planner</span>
        <span>Check AI-suggested topics against your official syllabus.</span>
      </footer>
    </main>
  );
}
