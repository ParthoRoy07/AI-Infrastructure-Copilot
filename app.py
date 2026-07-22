from flask import Flask, render_template, request, redirect, url_for
from agents.log_agent import analyze_log
from agents.helpdesk_agents import run_helpdesk_pipeline
from database.db import (
    insert_incident,
    insert_ticket,
    get_all_incidents,
    get_all_tickets,
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Accept pasted log text
        log_text = (
            request.form.get("log_text")
            or request.form.get("log_content")
            or request.form.get("log")
            or ""
        )
        # Call analyze_log()
        analysis_result = analyze_log(log_text)
        insert_incident(
    log_text,
    analysis_result.get("severity"),
    analysis_result.get("root_cause"),
    analysis_result.get("resolution")
)
        # Show result on helpdesk.html
        return render_template(
            "helpdesk.html",
            analysis_result=analysis_result,
            issue=analysis_result.get("issue"),
            severity=analysis_result.get("severity"),
            root_cause=analysis_result.get("root_cause"),
            resolution=analysis_result.get("resolution")
        )
    return render_template("upload.html")

@app.route("/helpdesk", methods=["GET", "POST"])
def helpdesk():
    if request.method == "POST":
        # Accept user issue
        issue = (
            request.form.get("issue")
            or request.form.get("user_issue")
            or ""
        )
        # Call run_helpdesk_pipeline()
        ticket = run_helpdesk_pipeline(issue)
        insert_ticket(
    ticket.get("issue"),
    ticket.get("priority"),
    ticket.get("resolution"),
    ticket.get("status")
)
        # Display generated ticket
        return render_template(
            "helpdesk.html",
            ticket=ticket,
            ticket_id=ticket.get("ticket_id"),
            issue=ticket.get("issue"),
            priority=ticket.get("priority"),
            status=ticket.get("status"),
            resolution=ticket.get("resolution")
        )
    return render_template("helpdesk.html")

if __name__ == "__main__":
    app.run(debug=True)
