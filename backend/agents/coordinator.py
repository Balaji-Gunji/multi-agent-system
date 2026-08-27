from .research_agent import run as research
from .planner_agent import run as plan
from .execution_agent import run as execute


def build_summary(task, research_result, plan_result, execution_result):
    lines = [
        f"Task: {task}",
        "",
        "Research → Planning → Execution completed.",
        ""
    ]

    for item in plan_result.get("plan", []):
        if "day" in item:
            lines.append(f"{item['day']}: " + " • ".join(item["items"]))
        else:
            lines.append("• " + item.get("step", ""))

    current = execution_result.get("current", {})
    if current:
        lines += [
            "",
            "Weather",
            f"Current temperature: {current.get('temperature_2m', 'N/A')}°C",
            f"Wind speed: {current.get('wind_speed_10m', 'N/A')} km/h"
        ]

    for day in execution_result.get("forecast", []):
        lines.append(
            f"{day['date']}: {day['min']}–{day['max']}°C | "
            f"Rain probability: {day['rain']}%"
        )

    return "\n".join(lines)


def run_workflow(task):
    research_result = research(task)
    plan_result = plan(task, research_result)
    execution_result = execute(task, plan_result)

    return {
        "task": task,
        "summary": build_summary(
            task, research_result, plan_result, execution_result
        ),
        "agents": [
            research_result,
            plan_result,
            execution_result
        ]
    }
