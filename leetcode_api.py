import copy
import os
import time
import requests

from dataclasses import dataclass

from queries import (
    QUESTION_DETAIL,
    SUBMISSION_LIST,
    SUBMISSION_DETAILS,
)


@dataclass
class Submission:

    id: int
    title: str
    title_slug: str

    difficulty: str

    skills: list

    timestamp: int

    language: str

    code: str

    content: str


class LeetCodeAPI:

    GRAPHQL_URL = "https://leetcode.com/graphql"

    ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"

    def __init__(self):

        self.session = requests.Session()

        self.session.cookies.set(
            "LEETCODE_SESSION",
            os.environ["LEETCODE_SESSION"],
            domain="leetcode.com",
        )

        self.session.cookies.set(
            "csrftoken",
            os.environ["LEETCODE_CSRF_TOKEN"],
            domain="leetcode.com",
        )

        self.headers = {
            "User-Agent":
            "Mozilla/5.0",
            "Connection":
            "keep-alive",
            "Content-Type":
            "application/json",
        }

    def graphql(self, payload):

        for attempt in range(3):

            try:

                title_slug = payload.get("variables", {}).get("titleSlug", "")

                headers = dict(self.headers)

                if title_slug:
                    headers["Referer"] = f"https://leetcode.com/problems/{title_slug}"

                response = self.session.post(
                    self.GRAPHQL_URL,
                    json=payload,
                    headers=headers,
                    timeout=20,
                )

                response.raise_for_status()

                data = response.json()

                if "errors" in data:
                    raise Exception(data["errors"])

                return data

            except requests.RequestException:

                if attempt == 2:
                    raise

                time.sleep(2)

    def get_all_accepted(self):

        response = self.session.get(
        self.ALL_PROBLEMS_URL,
        timeout=20,
        )

        if response.status_code != 200:
            raise Exception("Unable to fetch problem list.")

        response.raise_for_status()

        data = response.json()

        accepted = []

        for problem in data["stat_status_pairs"]:

            if problem["status"] != "ac":
                continue

            accepted.append(
                {
                    "id":
                    int(problem["stat"]["frontend_question_id"]),

                    "title":
                    problem["stat"]["question__title"],

                    "title_slug":
                    problem["stat"]["question__title_slug"],
                }
            )

        accepted.sort(
            key=lambda x: x["id"]
        )

        return accepted
    
    def get_question_details(self, title_slug):

        payload = copy.deepcopy(QUESTION_DETAIL)

        payload["variables"]["titleSlug"] = title_slug

        return self.graphql(payload)["data"]["question"]


    def get_latest_submission(self, title_slug):

        payload = copy.deepcopy(SUBMISSION_LIST)

        payload["variables"]["questionSlug"] = title_slug

        response = self.graphql(payload)

        submissions = response["data"]["questionSubmissionList"]["submissions"]

        if len(submissions) == 0:
            return None

        return submissions[0]


    def get_submission_code(self, submission_id):

        payload = copy.deepcopy(SUBMISSION_DETAILS)

        payload["variables"]["submissionId"] = submission_id

        response = self.graphql(payload)

        return response["data"]["submissionDetails"]


    def fetch_submission(self, problem):

        title_slug = problem["title_slug"]

        question = self.get_question_details(title_slug)

        latest = self.get_latest_submission(title_slug)

        if latest is None:
            return None

        code = self.get_submission_code(latest["id"])

        return Submission(

            id=problem["id"],

            title=problem["title"],

            title_slug=title_slug,

            difficulty=question["difficulty"],

            skills=[
                tag["name"]
                for tag in question["topicTags"]
            ],

            timestamp=int(latest["timestamp"]),

            language=latest["langName"],

            code=code["code"],

            content=question["content"],
        )
        
    def fetch_all_submissions(self):

        accepted = self.get_all_accepted()

        total = len(accepted)

        print(f"Found {total} accepted problems.\n")

        submissions = []

        failed = []

        for index, problem in enumerate(accepted, start=1):

            print(
                f"[{index}/{total}] "
                f"{problem['id']:04d} "
                f"{problem['title']}"
            )

            try:

                submission = self.fetch_submission(problem)

                if submission is not None:
                    submissions.append(submission)

            except Exception as e:

                print(
                    f"Failed : "
                    f"{problem['title']} "
                    f"({e})"
                )

                failed.append(problem)

        if failed:

            print("\nRetrying failed requests...\n")

            remaining = []

            for problem in failed:

                try:

                    submission = self.fetch_submission(problem)

                    if submission is not None:
                        submissions.append(submission)

                except Exception:

                    remaining.append(problem)

        if remaining:

            print("\nUnable to fetch:\n")

            for problem in remaining:

                print(
                    f"{problem['id']:04d} "
                    f"{problem['title']}"
                )

        submissions.sort(
            key=lambda x: x.timestamp
        )

        print(
            f"\nSuccessfully fetched "
            f"{len(submissions)} submissions."
        )

        return submissions