import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    abort,
)

from dotenv import load_dotenv
from psycopg import OperationalError

from db import db_cursor
from ollama_client import (
    analyze_incident,
    ask_assistant,
    ollama_health,
)


load_dotenv()


app = Flask(__name__)


ALLOWED_SEVERITIES = {
    "Low",
    "Medium",
    "High",
    "Critical",
}

ALLOWED_STATUSES = {
    "Open",
    "Investigating",
    "Resolved",
}

ALLOWED_CATEGORIES = {
    "Linux",
    "Docker",
    "Kubernetes",
    "AWS",
    "CI/CD",
    "Terraform",
    "Database",
    "Networking",
    "Application",
    "Other",
}


def get_incident_or_404(incident_id):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM incidents
            WHERE id = %s
            """,
            (incident_id,),
        )

        incident = cursor.fetchone()

    if not incident:
        abort(404)

    return incident


@app.route("/")
def dashboard():

    with db_cursor() as cursor:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE status = 'Open'
                ) AS open,
                COUNT(*) FILTER (
                    WHERE status = 'Investigating'
                ) AS investigating,
                COUNT(*) FILTER (
                    WHERE status = 'Resolved'
                ) AS resolved,
                COUNT(*) FILTER (
                    WHERE severity = 'Critical'
                    AND status != 'Resolved'
                ) AS critical
            FROM incidents
            """
        )

        stats = cursor.fetchone()

        cursor.execute(
            """
            SELECT *
            FROM incidents
            ORDER BY created_at DESC
            LIMIT 8
            """
        )

        recent = cursor.fetchall()

        # Get trend data for last 7 days
        cursor.execute(
            """
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM incidents
            WHERE created_at >= NOW() - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
            """
        )
        trend_data = cursor.fetchall()
        trend_labels = [
            row[0].strftime("%a") if row[0] else ""
            for row in trend_data
        ]
        trend_values = [row[1] for row in trend_data]

        # Get category distribution
        cursor.execute(
            """
            SELECT category, COUNT(*) as count
            FROM incidents
            GROUP BY category
            ORDER BY count DESC
            """
        )
        category_data = cursor.fetchall()
        category_labels = [row[0] for row in category_data]
        category_values = [row[1] for row in category_data]

    return render_template(
        "dashboard.html",
        stats=stats,
        incidents=recent,
        trend_labels=trend_labels,
        trend_values=trend_values,
        category_labels=category_labels,
        category_values=category_values,
    )


@app.route("/incidents")
def incidents():
    status = request.args.get(
        "status",
        "All"
    )

    severity = request.args.get(
        "severity",
        "All"
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = """
        SELECT *
        FROM incidents
        WHERE 1 = 1
    """

    params = []

    if status != "All":
        query += " AND status = %s"
        params.append(status)

    if severity != "All":
        query += " AND severity = %s"
        params.append(severity)

    if search:
        query += """
            AND (
                title ILIKE %s
                OR description ILIKE %s
                OR category ILIKE %s
            )
        """

        value = f"%{search}%"

        params.extend([
            value,
            value,
            value,
        ])

    query += " ORDER BY created_at DESC"

    with db_cursor() as cursor:
        cursor.execute(
            query,
            params,
        )

        incident_list = cursor.fetchall()

    return render_template(
        "incidents.html",
        incidents=incident_list,
        status_filter=status,
        severity_filter=severity,
        search=search,
    )


@app.route(
    "/incidents/create",
    methods=["POST"]
)
def create_incident():
    title = request.form.get(
        "title",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    category = request.form.get(
        "category",
        "Other"
    )

    severity = request.form.get(
        "severity",
        "Medium"
    )

    if not title or not description:
        return redirect(
            url_for("incidents")
        )

    if category not in ALLOWED_CATEGORIES:
        category = "Other"

    if severity not in ALLOWED_SEVERITIES:
        severity = "Medium"

    with db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO incidents (
                title,
                description,
                category,
                severity
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                title,
                description,
                category,
                severity,
            ),
        )

        incident = cursor.fetchone()

    return redirect(
        url_for(
            "incident_detail",
            incident_id=incident["id"],
        )
    )


@app.route("/incidents/<int:incident_id>")
def incident_detail(incident_id):
    incident = get_incident_or_404(
        incident_id
    )

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM ai_analyses
            WHERE incident_id = %s
            ORDER BY created_at DESC
            """,
            (incident_id,),
        )

        analyses = cursor.fetchall()

    return render_template(
        "incident.html",
        incident=incident,
        analyses=analyses,
    )


@app.route(
    "/incidents/<int:incident_id>/status",
    methods=["POST"]
)
def update_status(incident_id):
    get_incident_or_404(
        incident_id
    )

    status = request.form.get(
        "status"
    )

    if status not in ALLOWED_STATUSES:
        abort(400)

    with db_cursor() as cursor:

        if status == "Resolved":
            cursor.execute(
                """
                UPDATE incidents
                SET
                    status = %s,
                    updated_at = CURRENT_TIMESTAMP,
                    resolved_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    status,
                    incident_id,
                ),
            )

        else:
            cursor.execute(
                """
                UPDATE incidents
                SET
                    status = %s,
                    updated_at = CURRENT_TIMESTAMP,
                    resolved_at = NULL
                WHERE id = %s
                """,
                (
                    status,
                    incident_id,
                ),
            )

    return redirect(
        url_for(
            "incident_detail",
            incident_id=incident_id,
        )
    )


@app.route(
    "/incidents/<int:incident_id>/analyze",
    methods=["POST"]
)
def analyze(incident_id):
    incident = get_incident_or_404(
        incident_id
    )

    try:
        analysis = analyze_incident(
            incident
        )

    except Exception as error:
        return render_template(
            "incident.html",
            incident=incident,
            analyses=[],
            ai_error=str(error),
        ), 503

    with db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO ai_analyses (
                incident_id,
                analysis
            )
            VALUES (%s, %s)
            """,
            (
                incident_id,
                analysis,
            ),
        )

    return redirect(
        url_for(
            "incident_detail",
            incident_id=incident_id,
        )
    )


@app.route("/history")
def history():
    search = request.args.get(
        "search",
        ""
    ).strip()

    query = """
        SELECT *
        FROM incidents
        WHERE status = 'Resolved'
    """

    params = []

    if search:
        query += """
            AND (
                title ILIKE %s
                OR description ILIKE %s
                OR category ILIKE %s
            )
        """

        value = f"%{search}%"

        params.extend([
            value,
            value,
            value,
        ])

    query += """
        ORDER BY
            resolved_at DESC NULLS LAST,
            created_at DESC
    """

    with db_cursor() as cursor:
        cursor.execute(
            query,
            params,
        )

        resolved_incidents = cursor.fetchall()

    return render_template(
        "history.html",
        incidents=resolved_incidents,
        search=search,
    )


@app.route(
    "/assistant",
    methods=["GET", "POST"]
)
def assistant():
    error = None

    if request.method == "POST":

        message = request.form.get(
            "message",
            ""
        ).strip()

        if message:

            try:
                response = ask_assistant(
                    message
                )

                with db_cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO chat_history (
                            user_message,
                            ai_response
                        )
                        VALUES (%s, %s)
                        """,
                        (
                            message,
                            response,
                        ),
                    )

            except Exception as exc:
                error = str(exc)

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM chat_history
            ORDER BY created_at DESC
            LIMIT 30
            """
        )

        chats = cursor.fetchall()

    chats.reverse()

    return render_template(
        "assistant.html",
        chats=chats,
        error=error,
    )


@app.route(
    "/assistant/clear",
    methods=["POST"]
)
def clear_chat():
    with db_cursor() as cursor:
        cursor.execute(
            "DELETE FROM chat_history"
        )

    return redirect(
        url_for("assistant")
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "incident-manager",
    })


@app.route("/ready")
def readiness():
    database_ready = False

    try:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT 1"
            )

            cursor.fetchone()

        database_ready = True

    except OperationalError:
        database_ready = False

    ai_ready = ollama_health()

    ready = (
        database_ready
        and ai_ready
    )

    return jsonify({
        "status": (
            "ready"
            if ready
            else "not_ready"
        ),
        "database": database_ready,
        "ollama": ai_ready,
    }), 200 if ready else 503


@app.route("/metrics")
def metrics():
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE status = 'Open'
                ) AS open,
                COUNT(*) FILTER (
                    WHERE status = 'Investigating'
                ) AS investigating,
                COUNT(*) FILTER (
                    WHERE status = 'Resolved'
                ) AS resolved
            FROM incidents
            """
        )

        stats = cursor.fetchone()

    output = f"""# HELP incidents_total Total number of incidents
# TYPE incidents_total gauge
incidents_total {stats['total']}

# HELP incidents_open Number of open incidents
# TYPE incidents_open gauge
incidents_open {stats['open']}

# HELP incidents_investigating Number of investigating incidents
# TYPE incidents_investigating gauge
incidents_investigating {stats['investigating']}

# HELP incidents_resolved Number of resolved incidents
# TYPE incidents_resolved gauge
incidents_resolved {stats['resolved']}
"""

    return (
        output,
        200,
        {
            "Content-Type":
                "text/plain; version=0.0.4"
        },
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv(
            "FLASK_HOST",
            "0.0.0.0"  # nosec B104
        ),
        port=int(
            os.getenv(
                "FLASK_PORT",
                "5001"
            )
        ),
        debug=os.getenv(
            "FLASK_DEBUG",
            "false"
        ).lower() == "true",
    )
