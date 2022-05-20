from .bits.ultility import JsonSerializable


class LuoguType(JsonSerializable):
    pass


class ListParams(LuoguType):
    def __init__(self):
        self.page = None
        self.orderBy = None
        self.keyword = None
        self.order = None
        self.type = None


class ProblemListParams(ListParams):
    def __init__(self):
        super().__init__()
        self.content = None
        self.number = None
        self.tag = None


class ProblemSetListParams(ListParams):
    def __init__(self):
        super().__init__()


class RecordListParams(ListParams):
    def __init__(self):
        super().__init__()
        self.pid = None
        self.contestId = None
        self.user = None
        self.status = None
        self.language = None


class ListThemesParams(ListParams):
    def __init__(self):
        super().__init__()


class ListArticlesParams(ListParams):
    def __init__(self):
        super().__init__()
        self.uid = None


class GetRankingListParams(ListParams):
    def __init__(self):
        super().__init__()


class DataResponse(LuoguType):
    raise NotImplementedError


class Problem:
    raise NotImplementedError


class ProblemStatus:
    raise NotImplementedError


class ProblemData:
    raise NotImplementedError


class ProblemSettings:
    raise NotImplementedError


class ProblemSetListData:
    raise NotImplementedError


class ProblemSet:
    raise NotImplementedError


class ProblemSetData:
    raise NotImplementedError


class ProblemSetSettings:
    raise NotImplementedError


class Contest:
    raise NotImplementedError


class ContestData:
    raise NotImplementedError


class BaseRecord:
    raise NotImplementedError


class RecordData:
    raise NotImplementedError


class CreateProblemRequest:
    raise NotImplementedError


class UpdateTestCasesSettingsRequest:
    raise NotImplementedError


class EditContestRequest:
    raise NotImplementedError


class UpdateTestCasesSettingsResponse:
    raise NotImplementedError


class GetScoreboardResponse:
    raise NotImplementedError
