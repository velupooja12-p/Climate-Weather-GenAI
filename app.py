import urllib.parse
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

WEATHER_WORDS = {
    "sunny": "bright sunny weather with a warm golden sun",
    "rainy": "gentle rainy weather with soft raindrops and puddles",
    "cloudy": "a calm cloudy sky with fluffy clouds",
    "stormy": "a dramatic but child-friendly stormy sky with rain clouds",
    "snowy": "a magical snowy day with soft snowflakes",
    "windy": "a breezy windy day with leaves moving in the air",
    "rainbow": "a colorful rainbow after rain with soft sunlight",
}

STYLES = {
    "cartoon": "cute colorful children's storybook cartoon illustration",
    "3d": "friendly polished 3D animated children's illustration",
    "watercolor": "soft children's watercolor illustration",
    "realistic": "bright realistic educational weather photograph",
}

AGE_SETTINGS = {
    "3-5": {
        "level": "preschool children aged 3 to 5",
        "image": (
            "very simple, cute and colorful children's illustration, "
            "large clear objects, friendly child characters, "
            "simple clean background, very few objects, "
            "familiar everyday objects, bright cheerful visuals"
        ),
        "learning": (
            "The child may not know how to use a mobile phone or laptop. "
            "The learning should mainly happen through seeing and listening. "
            "Use one simple idea at a time. "
            "Use familiar objects that a preschool child can recognize easily. "
            "The image should be understandable without reading."
        )
    },
    "6-8": {
        "level": "children aged 6 to 8",
        "image": (
            "simple colorful educational illustration, "
            "clear objects, friendly child characters, "
            "slightly more details and simple visual actions"
        ),
        "learning": (
            "Use simple words and clear visual details. "
            "Show the weather in an easy educational way."
        )
    },
    "9-12": {
        "level": "children aged 9 to 12",
        "image": (
            "detailed educational children's illustration, "
            "clear weather-related objects, "
            "useful environmental details and slightly more realistic details"
        ),
        "learning": (
            "Include more educational information and visual detail "
            "while keeping the scene child-friendly and easy to understand."
        )
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}

    age = (data.get("age") or "3-5").strip()
    weather = (data.get("weather") or "sunny").lower()
    location = (data.get("location") or "a happy park").strip()
    style = (data.get("style") or "cartoon").lower()
    extra = (data.get("extra") or "").strip()

    if age not in AGE_SETTINGS:
        age = "3-5"
    if weather not in WEATHER_WORDS:
        weather = "sunny"
    if style not in STYLES:
        style = "cartoon"

    age_info = AGE_SETTINGS[age]

    prompt = f"""
Create a child-friendly educational weather illustration.

Target age:
{age_info["level"]}

Weather:
{WEATHER_WORDS[weather]}

Scene:
{location}

Art style:
{STYLES[style]}

Age-appropriate visual design:
{age_info["image"]}

Learning approach:
{age_info["learning"]}

Extra details:
{extra if extra else "simple happy scene suitable for children"}

Clearly show the selected weather condition.

Make the image safe, friendly, colorful and educational.

Avoid scary or disturbing content.
Do not include violence.
Do not include complex scientific diagrams.
Do not add text, labels, logos or watermarks.
"""

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = (
            "https://image.pollinations.ai/prompt/"
            + encoded_prompt
            + "?width=1024&height=1024&nologo=true"
        )

        response = requests.get(image_url, timeout=60)

        if response.status_code != 200:
            return jsonify({
                "error": "Image generation service is not available right now."
            }), 500

        return jsonify({
            "success": True,
            "image_url": image_url,
            "prompt": prompt.strip(),
            "age": age,
            "weather": weather,
            "style": style
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
