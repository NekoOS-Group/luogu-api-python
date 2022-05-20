from .types import *
from typing import NoReturn


class ProblemAPI:
    @staticmethod
    def get_problem_list(
            params: ProblemListParams
    ) -> list[Problem | ProblemStatus]:
        raise NotImplementedError

    @staticmethod
    def get_created_problems(
            user_id: int,
            page: int
    ) -> list[Problem]:
        raise NotImplementedError

    @staticmethod
    def get_problem(
            problem_id: str,
            contest_id: int = None
    ) -> ProblemData:
        raise NotImplementedError

    @staticmethod
    def create_problem(
            rq: CreateProblemRequest
    ) -> str:
        raise NotImplementedError

    @staticmethod
    def edit_problem(
            setting: ProblemSettings
    ) -> str:
        raise NotImplementedError

    @staticmethod
    def edit_problem_testcase(
            problem_id: str,
            rq: UpdateTestCasesSettingsRequest
    ) -> UpdateTestCasesSettingsResponse:
        raise NotImplementedError

    @staticmethod
    def delete_problem(
            pid: str
    ) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def move_problem(
            operation: str = "transfer",
            _type: str = None,
            teamID: int = None
    ) -> str:
        raise NotImplementedError


class ProblemSetAPI:
    @staticmethod
    def get_problem_set_list(
            params: ProblemSetListParams
    ) -> ProblemSetListData:
        raise NotImplementedError

    @staticmethod
    def get_created_problem_set(
            user_id: int,
            page: int
    ) -> list[ProblemSet]:
        raise NotImplementedError

    @staticmethod
    def get_group_problem_set(
            group_id: int,
            page: int
    ) -> list[ProblemSet]:
        raise NotImplementedError

    @staticmethod
    def get_marked_problem_set(
            user_id: int,
            page: int
    ) -> list[ProblemSet]:
        raise NotImplementedError

    @staticmethod
    def get_problem_set(
            problem_set_id: int
    ) -> ProblemSetData:
        raise NotImplementedError

    @staticmethod
    def mark_problem_set(
            problem_set_id: int
    ) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def unmark_problem_set(
            problem_set_id: int
    ) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def create_problem_set(
            settings: ProblemSetSettings,
            provider_user_id: int = None
    ) -> int:
        raise NotImplementedError

    @staticmethod
    def edit_problem_set(
            settings: ProblemSetSettings,
    ) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def move_problem_set(
            _type: int,
            provider_user_id: int = None
    ) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def delete_problem_set(
            problem_set_id: int
    ) -> NoReturn:
        raise NotImplementedError


class ContestAPI:
    @staticmethod
    def get_contest_list(

    ) -> list[Contest]:
        raise NotImplementedError

    @staticmethod
    def get_created_contest_list(
            user_id: int,
            page: int
    ) -> list[Contest]:
        raise NotImplementedError

    @staticmethod
    def get_joined_contest_list(
            user_id: int,
            page: int
    ) -> list[Contest]:
        raise NotImplementedError

    @staticmethod
    def get_contest(
            contest_id: int
    ) -> ContestData:
        raise NotImplementedError

    @staticmethod
    def get_contest_scoreboard(
            contest_id: int
    ) -> GetScoreboardResponse:
        raise NotImplementedError

    @staticmethod
    def create_contest(
            rq: EditContestRequest,
    ) -> int:
        raise NotImplementedError

    @staticmethod
    def edit_contest(
            contest_id: int,
            rq: EditContestRequest
    ) -> int:
        raise NotImplementedError

    @staticmethod
    def delete_contest(
            contest_id: int
    ) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def join_contest(
            contest_id: int,
            code: str
    ) -> int:
        raise NotImplementedError


class RecordAPI:
    @staticmethod
    def get_record_list(
            params: RecordListParams
    ) -> list[BaseRecord]:
        raise NotImplementedError

    @staticmethod
    def get_record(
            record_id: int
    ) -> RecordData:
        raise NotImplementedError


class DiscussAPI:
    raise NotImplementedError


class UserAPI:
    raise NotImplementedError


class GroupAPI:
    raise NotImplementedError


class ChatAPI:
    raise NotImplementedError


class ThemeAPI:
    raise NotImplementedError


class ImageAPI:
    raise NotImplementedError


class BlogAPI:
    raise NotImplementedError


class PasteAPI:
    raise NotImplementedError


class IDE_API:
    raise NotImplementedError


class VerifyAPI:
    raise NotImplementedError


class FeedAPI:
    raise NotImplementedError


class PaintAPI:
    raise NotImplementedError


class RankingAPI:
    raise NotImplementedError

