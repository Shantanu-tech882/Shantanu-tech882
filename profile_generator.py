from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps, ImageEnhance


PHOTO = Path("assets/profile.jpg")
OUTPUT = Path("assets/profile-animation.svg")

# ASCII settings
COLUMNS = 72
ROWS = 42

# Dark → bright
ASCII_CHARS = " .:-=+*#%@"


def image_to_ascii():
    image = Image.open(PHOTO).convert("RGB")

    # Focus slightly toward the upper part of the photo
    image = ImageOps.fit(
        image,
        (COLUMNS, ROWS),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.34),
    )

    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(1.45)

    pixels = image.load()
    lines = []

    for y in range(ROWS):
        line = ""

        for x in range(COLUMNS):
            brightness = pixels[x, y]
            index = int(brightness / 256 * len(ASCII_CHARS))

            if index >= len(ASCII_CHARS):
                index = len(ASCII_CHARS) - 1

            line += ASCII_CHARS[index]

        lines.append(line)

    return lines


def build_svg(ascii_lines):
    width = 1200
    height = 620

    svg = [
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}"
        height="{height}"
        viewBox="0 0 {width} {height}">

        <rect width="100%" height="100%" fill="#0d1117"/>

        <rect x="25" y="25"
              width="1150"
              height="570"
              rx="18"
              fill="#010409"
              stroke="#30363d"
              stroke-width="2"/>

        <!-- Terminal buttons -->
        <circle cx="55" cy="55" r="7" fill="#ff5f56"/>
        <circle cx="80" cy="55" r="7" fill="#ffbd2e"/>
        <circle cx="105" cy="55" r="7" fill="#27c93f"/>

        <!-- Terminal title -->
        <text x="135" y="61"
              fill="#8b949e"
              font-family="monospace"
              font-size="16">
            shantanu@github: ~/profile
        </text>

        <!-- Terminal prompt -->
        <text x="55" y="105"
              fill="#58a6ff"
              font-family="monospace"
              font-size="18">
            $ ./whoami
        </text>
        '''
    ]

    # ASCII portrait
    start_y = 135
    line_height = 10

    for i, line in enumerate(ascii_lines):
        safe_line = escape(line)

        delay = 0.7 + (i * 0.035)

        svg.append(
            f'''
            <text x="55"
                  y="{start_y + i * line_height}"
                  fill="#58a6ff"
                  font-family="monospace"
                  font-size="10"
                  xml:space="preserve"
                  opacity="0">
                {safe_line}
                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    begin="{delay:.2f}s"
                    dur="0.25s"
                    fill="freeze"/>
            </text>
            '''
        )

    # Information panel
    info_x = 720
    info_y = 155

    info_lines = [
        ("$ name", "#58a6ff"),
        ("Shantanu Shaw", "#f0f6fc"),
        ("", "#8b949e"),
        ("$ role", "#58a6ff"),
        ("Developer", "#f0f6fc"),
        ("", "#8b949e"),
        ("$ technologies", "#58a6ff"),
        ("Python • C++ • Java", "#8b949e"),
        ("React • Next.js", "#8b949e"),
        ("Node.js • Express", "#8b949e"),
        ("MongoDB • Supabase", "#8b949e"),
        ("AWS • Google Cloud", "#8b949e"),
        ("", "#8b949e"),
        ("$ status", "#58a6ff"),
        ("Building • Learning • Shipping", "#3fb950"),
        ("", "#8b949e"),
        ("$ echo \"Hello World!\"", "#58a6ff"),
        ("Welcome to my GitHub.", "#f0f6fc"),
    ]

    for i, (text, color) in enumerate(info_lines):
        y = info_y + i * 23
        delay = 1.2 + i * 0.12

        svg.append(
            f'''
            <text x="{info_x}"
                  y="{y}"
                  fill="{color}"
                  font-family="monospace"
                  font-size="18"
                  opacity="0">
                {escape(text)}
                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    begin="{delay:.2f}s"
                    dur="0.35s"
                    fill="freeze"/>
            </text>
            '''
        )

    # Blinking cursor
    svg.append(
        '''
        <rect x="55" y="555"
              width="10"
              height="18"
              fill="#58a6ff">
            <animate
                attributeName="opacity"
                values="1;0;1"
                dur="0.8s"
                repeatCount="indefinite"/>
        </rect>
        
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    if not PHOTO.exists():
        raise FileNotFoundError(
            f"Could not find {PHOTO}. "
            "Make sure your photo is stored as assets/profile.jpg."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    ascii_lines = image_to_ascii()
    svg = build_svg(ascii_lines)

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
