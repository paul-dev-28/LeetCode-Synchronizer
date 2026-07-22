import json
import os
import pathlib
import shutil
import urllib.parse

from git import Repo

from language import get_extension


class GitHubSynchronizer:

    def __init__(self):

        self.repo = Repo(os.getcwd())

        url = urllib.parse.urlparse(
            self.repo.remote("origin").url
        )

        url = url._replace(
            netloc=f"{os.environ['GITHUB_TOKEN']}@{url.netloc}"
        )

        if not url.path.endswith(".git"):
            url = url._replace(
                path=url.path + ".git"
            )

        self.repo.remote("origin").set_url(
            url.geturl()
        )

        commit = list(self.repo.iter_commits())[0]

        self.repo.config_writer().set_value(
            "user",
            "name",
            commit.author.name,
        ).release()

        self.repo.config_writer().set_value(
            "user",
            "email",
            commit.author.email,
        ).release()

    def load_database(self):

        if not os.path.exists("submissions.json"):
            return []

        with open(
            "submissions.json",
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def save_database(self, database):

        database.sort(
            key=lambda x: x["id"]
        )

        with open(
            "submissions.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                database,
                f,
                indent=2,
                ensure_ascii=False,
            )
    def clean_problem_folder(
        self,
        folder,
    ):

        if os.path.exists(folder):

            shutil.rmtree(folder)

        pathlib.Path(folder).mkdir(
            parents=True,
            exist_ok=True,
        )

    def write_submission(
        self,
        submission,
    ):

        folder = (
            f"problems/"
            f"{submission.id:04d}-"
            f"{submission.title_slug}"
        )

        self.clean_problem_folder(folder)

        extension = get_extension(
            submission.language
        )

        source = (
            f"{folder}/"
            f"{submission.id:04d}-"
            f"{submission.title_slug}."
            f"{extension}"
        )

        with open(
            source,
            "w",
            encoding="utf-8",
        ) as f:

            f.write(
                submission.code.strip()
            )

        with open(
            f"{folder}/README.md",
            "w",
            encoding="utf-8",
        ) as f:

            f.write(
                f"<h2>{submission.id}. "
                f"{submission.title}</h2>\n\n"
            )

            f.write(
                submission.content.strip()
            )

    def update_database(self, submissions):

        database = []

        for submission in submissions:

            database.append(
                {
                    "id": submission.id,
                    "title": submission.title,
                    "title_slug": submission.title_slug,
                    "difficulty": submission.difficulty,
                    "skills": sorted(submission.skills),
                }
            )

        self.save_database(database)


    def generate_readme(self, submissions):

        lines = []

        lines.append("# LeetCode Submissions\n")

        lines.append(
            "> Automatically synchronized from LeetCode.\n"
        )

        lines.append(
            "| # | Title | Difficulty | Skills |"
        )

        lines.append(
            "|---|-------|------------|--------|"
        )

        for submission in sorted(
            submissions,
            key=lambda x: x.id,
        ):

            title = (
                f"[{submission.title}]"
                f"(https://leetcode.com/problems/"
                f"{submission.title_slug})"
            )

            skills = " ".join(
                f"`{skill}`"
                for skill in sorted(submission.skills)
            )

            lines.append(
                f"| {submission.id:04d} | "
                f"{title} | "
                f"{submission.difficulty} | "
                f"{skills} |"
            )

        with open(
            "README.md",
            "w",
            encoding="utf-8",
        ) as f:

            f.write("\n".join(lines))


    def synchronize(self, submissions):

        print(
            "\nWriting files...\n"
        )

        for submission in submissions:

            self.write_submission(
                submission
            )

        print(
            "Updating README..."
        )

        self.generate_readme(
            submissions
        )

        print(
            "Updating database..."
        )

        self.update_database(
            submissions
        )

        print(
            "Creating Git commit..."
        )

        self.repo.git.add(A=True)

        if self.repo.is_dirty():

            self.repo.index.commit(
                f"Synchronize {len(submissions)} LeetCode solutions"
            )

            print(
                "Pushing..."
            )

            self.repo.git.push(
                "origin"
            )

            print(
                "Synchronization complete."
            )

        else:

            print(
                "Repository already up to date."
            )