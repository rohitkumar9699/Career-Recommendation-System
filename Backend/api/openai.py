import json
import os
from typing import List

from google import genai
from pydantic import BaseModel, Field

def generate_career_roadmap(recommendations: List[dict]) -> dict:
    # =========================================================
    # 1. Define the EXACT JSON structure you want
    # =========================================================

    class CareerRoadmap(BaseModel):
        career: str = Field(
            description="The original career name from the input."
        )

        score: float = Field(
            description="The original recommendation score from the input."
        )

        degree_course: List[str] = Field(
            description="Relevant degrees, diplomas, certifications, or courses."
        )

        what_you_do: str = Field(
            description="A simple explanation of what professionals in this career do."
        )

        skills: List[str] = Field(
            description="Important skills required for this career."
        )

        what_to_explore: List[str] = Field(
            description="Career-related areas, subjects, or opportunities to explore."
        )


    class CareerRoadmapResponse(BaseModel):
        recommendations: List[CareerRoadmap]


    # =========================================================
    # 2. Initialize Gemini
    # =========================================================

    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Set it in your environment before running the program."
        )

    client = genai.Client(api_key=api_key)


    # =========================================================
    # 3. Your existing ML model output
    # =========================================================

    # recommendations = [
    #     {
    #         "career": "Business Owner",
    #         "score": 86.0
    #     },
    #     {
    #         "career": "Accountant",
    #         "score": 9.0
    #     },
    #     {
    #         "career": "Real Estate Developer",
    #         "score": 2.0
    #     }
    # ]


    # =========================================================
    # 4. Prompt
    # =========================================================

    prompt = f"""
    You are a career guidance agent.

    Generate a career roadmap for EVERY career in the provided input.

    INPUT:
    {json.dumps(recommendations, indent=2)}

    For each career, provide:

    - career
    - score
    - degree_course
    - what_you_do
    - skills
    - what_to_explore

    Rules:
    1. Do not skip any career.
    2. Keep the original career names unchanged.
    3. Keep the original scores unchanged.
    4. Do not change the order of the recommendations.
    5. Use simple language suitable for students.
    6. Do not claim that a career is guaranteed for the student.
    7. Do not include Markdown or explanations outside the JSON.
    8. Generate relevant career information for each recommendation.
    """


    # =========================================================
    # 5. Generate structured JSON
    # =========================================================

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CareerRoadmapResponse,
        }
    )


    # =========================================================
    # 6. Validate the response
    # =========================================================

    try:
        result = CareerRoadmapResponse.model_validate_json(response.text)

    except Exception as error:
        print("Invalid response received from Gemini.")
        print(error)
        raise SystemExit(1)


    # =========================================================
    # 7. Verify that Gemini did not change your ML output
    # =========================================================

    if len(result.recommendations) != len(recommendations):
        raise ValueError("Gemini returned an incorrect number of recommendations.")


    for original, generated in zip(
        recommendations,
        result.recommendations
    ):
        if original["career"] != generated.career:
            raise ValueError(
                f"Career name changed: "
                f"{original['career']} -> {generated.career}"
            )

        if original["score"] != generated.score:
            raise ValueError(
                f"Score changed for {original['career']}: "
                f"{original['score']} -> {generated.score}"
            )


    # =========================================================
    # 8. Print final JSON
    # =========================================================

    # print("\nFINAL JSON:\n")

    data = result.model_dump()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return data