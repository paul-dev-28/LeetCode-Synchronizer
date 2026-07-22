"""
Maps LeetCode language names to source file extensions.
"""

LANGUAGE_EXTENSION = {
    "C++": "cpp",
    "Java": "java",
    "Python": "py",
    "Python3": "py",
    "Python 3": "py",
    "Python2": "py",
    "Python 2": "py",
    "JavaScript": "js",
    "TypeScript": "ts",
    "Go": "go",
    "Rust": "rs",
    "Kotlin": "kt",
    "Swift": "swift",
    "PHP": "php",
    "Ruby": "rb",
    "Scala": "scala",
    "C": "c",
    "C#": "cs",
    "MySQL": "sql",
    "Oracle": "sql",
    "MS SQL Server": "sql",
    "PostgreSQL": "sql",
    "SQLite": "sql",
    "Pandas": "py",
    "Racket": "rkt",
    "Dart": "dart",
    "Bash": "sh",
    "Shell": "sh",
    "Elixir": "ex",
    "Erlang": "erl",
    "Julia": "jl",
}


def get_extension(language: str) -> str:
    """
    Returns the file extension corresponding to a LeetCode language.

    Raises:
        ValueError if the language is unsupported.
    """

    language = language.strip()

    if language not in LANGUAGE_EXTENSION:
        raise ValueError(f"Unsupported language: {language}")

    return LANGUAGE_EXTENSION[language]


def is_supported(language: str) -> bool:
    """
    Returns True if the language is supported.
    """

    return language.strip() in LANGUAGE_EXTENSION


def add_language(language: str, extension: str) -> None:
    """
    Allows adding new language mappings dynamically.
    """

    LANGUAGE_EXTENSION[language.strip()] = extension.strip()


def all_languages():
    """
    Returns a sorted list of supported languages.
    """

    return sorted(LANGUAGE_EXTENSION.keys())


if __name__ == "__main__":

    print("Supported Languages\n")

    for lang in all_languages():
        print(f"{lang:20} -> .{get_extension(lang)}")