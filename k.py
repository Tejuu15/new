from flask import Flask, render_template_string, request


app = Flask(__name__)


def caesar_cipher(text, shift, mode="encrypt"):
        result = ""

        if mode == "decrypt":
                shift = -shift

        for char in text:
                if char.isalpha():
                        base = ord("A") if char.isupper() else ord("a")
                        new_char = chr((ord(char) - base + shift) % 26 + base)
                        result += new_char
                else:
                        result += char

        return result


PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Caesar Cipher App</title>
    <style>
        :root {
            color-scheme: light;
            --bg1: #f6efe7;
            --bg2: #dce8f7;
            --card: rgba(255, 255, 255, 0.82);
            --text: #1f2937;
            --muted: #6b7280;
            --accent: #0f766e;
            --accent-dark: #115e59;
            --border: rgba(31, 41, 55, 0.12);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Georgia, "Times New Roman", serif;
            color: var(--text);
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.15), transparent 30%),
                radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.15), transparent 28%),
                linear-gradient(135deg, var(--bg1), var(--bg2));
            display: grid;
            place-items: center;
            padding: 24px;
        }

        .card {
            width: min(720px, 100%);
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: 0 24px 70px rgba(15, 23, 42, 0.16);
            backdrop-filter: blur(14px);
            padding: 32px;
        }

        h1 {
            margin: 0 0 8px;
            font-size: clamp(2rem, 4vw, 3rem);
            letter-spacing: -0.03em;
        }

        p {
            margin: 0 0 24px;
            color: var(--muted);
            line-height: 1.5;
        }

        form {
            display: grid;
            gap: 16px;
        }

        label {
            display: block;
            font-weight: 700;
            margin-bottom: 8px;
        }

        textarea,
        input,
        select {
            width: 100%;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 14px 16px;
            font: inherit;
            background: rgba(255, 255, 255, 0.9);
            color: var(--text);
        }

        textarea {
            min-height: 140px;
            resize: vertical;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .actions {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        button {
            border: 0;
            border-radius: 999px;
            padding: 12px 18px;
            font: inherit;
            font-weight: 700;
            cursor: pointer;
        }

        .primary {
            background: var(--accent);
            color: white;
        }

        .secondary {
            background: transparent;
            color: var(--accent-dark);
            border: 1px solid rgba(15, 118, 110, 0.35);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
        }

        .result {
            margin-top: 24px;
            padding: 18px;
            border-radius: 18px;
            background: rgba(15, 118, 110, 0.08);
            border: 1px solid rgba(15, 118, 110, 0.16);
        }

        .result h2 {
            margin: 0 0 8px;
            font-size: 1.1rem;
        }

        .result pre {
            margin: 0;
            white-space: pre-wrap;
            word-break: break-word;
            font: inherit;
        }

        @media (max-width: 640px) {
            .card {
                padding: 22px;
            }

            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <main class="card">
        <h1>Caesar Cipher App</h1>
        <p>Type a message, choose a shift, and encrypt or decrypt it in the browser.</p>

        <form method="post">
            <div>
                <label for="text">Text</label>
                <textarea id="text" name="text" placeholder="Enter text here...">{{ text }}</textarea>
            </div>

            <div class="grid">
                <div>
                    <label for="shift">Shift value</label>
                    <input id="shift" name="shift" type="number" value="{{ shift }}" required>
                </div>

                <div>
                    <label for="mode">Mode</label>
                    <select id="mode" name="mode">
                        <option value="encrypt" {% if mode == "encrypt" %}selected{% endif %}>Encrypt</option>
                        <option value="decrypt" {% if mode == "decrypt" %}selected{% endif %}>Decrypt</option>
                    </select>
                </div>
            </div>

            <div class="actions">
                <button class="primary" type="submit">Run cipher</button>
                <a class="secondary" href="/">Reset</a>
            </div>
        </form>

        {% if output is not none %}
        <section class="result">
            <h2>Result</h2>
            <pre>{{ output }}</pre>
        </section>
        {% endif %}
    </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
        text = ""
        shift = 3
        mode = "encrypt"
        output = None

        if request.method == "POST":
                text = request.form.get("text", "")
                mode = request.form.get("mode", "encrypt")
                try:
                        shift = int(request.form.get("shift", 3))
                except ValueError:
                        shift = 3
                output = caesar_cipher(text, shift, mode)

        return render_template_string(
                PAGE,
                text=text,
                shift=shift,
                mode=mode,
                output=output,
        )


if __name__ == "__main__":
        app.run(debug=True)