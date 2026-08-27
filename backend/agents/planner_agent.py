def run(task, research):
    titles = [x["title"] for x in research.get("results", [])]

    if "hyderabad" in task.lower() and any(
        word in task.lower() for word in ["trip", "tour", "travel"]
    ):
        places = [
            "Charminar",
            "Chowmahalla Palace",
            "Laad Bazaar",
            "Golconda Fort",
            "Qutb Shahi Tombs",
            "Salar Jung Museum",
            "Hussain Sagar",
            "Birla Mandir"
        ]

        return {
            "agent": "Planner Agent",
            "status": "completed",
            "goal": task,
            "plan": [
                {"day": "Day 1", "items": places[:3]},
                {"day": "Day 2", "items": places[3:6]},
                {"day": "Day 3", "items": places[6:]}
            ]
        }

    return {
        "agent": "Planner Agent",
        "status": "completed",
        "goal": task,
        "plan": [
            {"step": f"Review research result: {title}"}
            for title in titles[:5]
        ] or [{"step": "Review available research and create an actionable plan."}]
    }
