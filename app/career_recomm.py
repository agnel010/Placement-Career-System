def recommend_career(course: str, skills_input: str, interest: str) -> list[dict]:
    skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]

    skill_groups = {
        "programming": ["python", "java", "c++", "javascript", "c#", "go", "dsa"],
        "web":         ["html", "css", "javascript", "react", "node", "django", "next.js"],
        "data":        ["sql", "excel", "power bi", "tableau", "pandas", "statistics"],
        "ai_ml":       ["machine learning", "ai", "ml", "deep learning", "tensorflow"],
        "cloud":       ["aws", "azure", "gcp", "devops", "docker", "kubernetes"],
        "marketing":   ["seo", "digital marketing", "content", "social media", "google ads"],
        "design":      ["figma", "ui", "ux", "adobe", "graphic design"],
        "finance":     ["finance", "accounting", "financial modeling", "excel advanced"],
        "management":  ["project management", "agile", "business analysis", "leadership"]
    }

    course_boost = {
        "BTech":  ["programming", "web", "ai_ml", "cloud", "data"],
        "BCA":    ["programming", "web", "data", "ai_ml"],
        "MCA":    ["programming", "ai_ml", "cloud", "data"],
        "MBA":    ["management", "finance", "marketing"],
        "BCom":   ["finance", "management", "marketing"],
        "BSc":    ["data", "ai_ml", "programming"]
    }

    interest_map = {
        "Technology":       ["Software Engineer", "Full-Stack Developer"],
        "Data & Analytics": ["Data Analyst", "Data Scientist"],
        "Management":       ["Business Analyst", "Product Manager"],
        "Finance":          ["Financial Analyst"],
        "Marketing":        ["Digital Marketer"],
        "Design":           ["UI/UX Designer"],
        "Research":         ["Research Analyst", "Data Scientist"]
    }

    recs = {}

    # Skill matches
    for group, keywords in skill_groups.items():
        matches = sum(1 for k in keywords if k in skills)
        if matches > 0:
            score = matches / len(keywords) * 60
            if group == "programming":
                title = "Software Engineer"
            elif group == "web":
                title = "Full-Stack / Web Developer"
            elif group == "data":
                title = "Data Analyst"
            elif group == "ai_ml":
                title = "AI / ML Engineer"
            elif group == "cloud":
                title = "Cloud / DevOps Engineer"
            elif group == "marketing":
                title = "Digital Marketer"
            elif group == "design":
                title = "UI/UX Designer"
            elif group == "finance":
                title = "Financial Analyst"
            elif group == "management":
                title = "Business Analyst"
            else:
                continue

            recs[title] = recs.get(title, {"score": 0, "reasons": []})
            recs[title]["score"] += score
            recs[title]["reasons"].append(f"{group.replace('_', ' ').title()} skills ({matches} match)")

    # Interest boost
    for role in interest_map.get(interest, []):
        recs[role] = recs.get(role, {"score": 0, "reasons": []})
        recs[role]["score"] += 70
        recs[role]["reasons"].append(f"Aligns with your interest: {interest}")

    # Course boost
    for group in course_boost.get(course, []):
        for title, data in list(recs.items()):
            if any(g in title.lower() for g in ["engineer", "developer", "analyst", "scientist"]):
                data["score"] += 25
                data["reasons"].append(f"Strong fit for {course} graduates")

    # Format output
    result = []
    for title, data in recs.items():
        result.append({
            "title": title,
            "confidence": min(round(data["score"]), 100),
            "reasons": ", ".join(set(data["reasons"]))
        })

    result.sort(key=lambda x: x["confidence"], reverse=True)

    if not result:
        result = [{
            "title": "Explore High-Demand Fields",
            "confidence": 50,
            "reasons": "Add more specific skills or consider certifications in Data Analytics, Cloud, AI, Digital Marketing"
        }]

    return result[:6]