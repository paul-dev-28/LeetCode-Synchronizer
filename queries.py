"""
GraphQL queries used by the LeetCode Synchronizer.
"""

QUESTION_DETAIL = {
    "query": """
query getQuestionDetail($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        content
        difficulty
        topicTags {
            name
            slug
        }
    }
}
""",
    "variables": {
        "titleSlug": ""
    },
    "operationName": "getQuestionDetail"
}


SUBMISSION_LIST = {
    "query": """
query submissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
    questionSubmissionList(
        offset: $offset
        limit: $limit
        questionSlug: $questionSlug
    ) {
        submissions {
            id
            langName
            timestamp
            statusDisplay
            runtime
            memory
        }
    }
}
""",
    "variables": {
        "questionSlug": "",
        "offset": 0,
        "limit": 1
    },
    "operationName": "submissionList"
}


SUBMISSION_DETAILS = {
    "query": """
query submissionDetails($submissionId: Int!) {
    submissionDetails(submissionId: $submissionId) {
        code
        runtime
        memory
        runtimePercentile
        memoryPercentile
    }
}
""",
    "variables": {
        "submissionId": 0
    },
    "operationName": "submissionDetails"
}


USER_PROFILE = {
    "query": """
query globalData {
    userStatus {
        username
        realName
        avatar
    }
}
""",
    "variables": {},
    "operationName": "globalData"
}


PROBLEM_LIST = {
    "query": """
query problemsetQuestionList(
    $categorySlug: String,
    $limit: Int,
    $skip: Int,
    $filters: QuestionListFilterInput
) {
    problemsetQuestionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
    ) {
        total
        questions {
            questionFrontendId
            title
            titleSlug
            difficulty
        }
    }
}
""",
    "variables": {
        "categorySlug": "",
        "limit": 100,
        "skip": 0,
        "filters": {}
    },
    "operationName": "problemsetQuestionList"
}