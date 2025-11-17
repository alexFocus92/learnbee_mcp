"""Constants used throughout the Learnbee MCP application."""

# Maximum length for lesson content
LESSON_CONTENT_MAX_LENGTH = 50000

# Available tutor names for early childhood education
# Mix of Disney characters, video game characters, famous personalities, and original characters
# Format: (name, description)
TUTOR_NAMES = [
    ("Mickey Mouse", "Friendly Disney character who loves learning"),
    ("Elsa", "Magical queen who teaches with wonder and creativity"),
    ("Buzz Lightyear", "Space explorer teaching science and adventure"),
    ("Mario", "Heroic plumber making learning fun and exciting"),
    ("Sonic", "Fast hedgehog who makes learning super speedy"),
    ("Pikachu", "Electric Pokémon friend who sparks curiosity"),
    ("Einstein", "Brilliant scientist sharing knowledge simply"),
    ("Curious Explorer", "Adventurer discovering new things together"),
    ("Magic Teacher", "Wizard making learning magical and fun"),
    ("Adventure Buddy", "Friend ready for exciting learning journeys")
]

# Helper function to get tutor names only (for backward compatibility)
def get_tutor_names():
    """Get list of tutor names only."""
    return [name for name, _ in TUTOR_NAMES]

# Helper function to get tutor description
def get_tutor_description(tutor_name):
    """Get description for a tutor by name."""
    for name, description in TUTOR_NAMES:
        if name == tutor_name:
            return description
    return ""

# Available languages
LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Chinese",
    "Japanese",
    "Korean",
    "Arabic",
    "Russian",
    "Dutch",
    "Polish",
    "Turkish",
    "Hindi"
]

# Difficulty levels
DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]

# Age ranges for lessons
AGE_RANGES = ["3-6", "4-7", "5-8", "6-9", "7-10"]

