import json

from .bits.ultility import JsonSerializable, Printable

class LuoguType(JsonSerializable, Printable):
    __type_dict__ = {}

    def __init__(self,json=None):
        super().__init__(json)

class RequestParams(LuoguType):
    pass

class Response(LuoguType):
    pass

class ListRequestParams(RequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": int
    }

    def __init__(
            self,
            page: int = None,
            orderBy: int = None
    ):
        super().__init__()
        self.page = page
        self.orderBy = orderBy

class ProblemListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": int,
        "keyword": str,
        "content": bool,
        "type": str,
        "difficulty": int,
        "tag": str
    }

    def __init__(
            self,
            page: int = None,
            orderBy: int = None,
            keyword: str = None,
            content: bool = None,
            type: str = None,
            difficulty: int = None,
            tag: str = None
    ):
        super().__init__(page, orderBy)
        self.keyword = keyword
        self.content = content
        self.type = type
        self.difficulty = difficulty
        self.tag = tag

class ProblemSetListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "keyword": str,
        "type": str
    }

    def __init__(
            self,
            page: int = None,
            keyword: str = None,
            type: str = None
    ):
        super().__init__(page=page)
        self.keyword = keyword
        self.type = type

class RecordListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "pid": str,
        "contestId": int,
        "user": str,
        "status": int,
        "language": int,
        "orderBy": int
    }

    def __init__(
            self,
            page: int = None,
            pid: str = None,
            contestId: int = None,
            user: str = None,
            status: int = None,
            language: int = None,
            orderBy: int = None
    ):
        super().__init__(page=page, orderBy=orderBy)
        self.pid = pid
        self.contestId = contestId
        self.user = user
        self.status = status
        self.language = language

class ThemeListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": str,
        "order": str,
        "type": str
    }

    def __init__(
            self,
            page: int = None,
            orderBy: str = None,
            order: str = None,
            type: str = None
    ):
        super().__init__(page=page, orderBy=None)  # orderBy 是 str 类型，这里设置为 None
        self.orderBy = orderBy
        self.order = order
        self.type = type

class ArticleListRequestParams(LuoguType):
    __type_dict__ = {
        "user": int,
        "page": int,
        "category": int,
        "ascending": bool,
        "promoted": bool,
        "title": str
    }

    def __init__(
            self,
            user: int,
            page: int = None,
            category: int = None,
            ascending: bool = None,
            promoted: bool = None,
            title: str = None
    ):
        super().__init__()
        self.user = user
        self.page = page
        self.category = category
        self.ascending = ascending
        self.promoted = promoted
        self.title = title

class BlogListRequestParams(ListRequestParams):
    __type_dict__ = {
        "uid": int,
        "keyword": str,
        "type": str,
        "page": int
    }

    def __init__(
            self,
            uid: int,
            keyword: str = None,
            type: str = None,
            page: int = None
    ):
        super().__init__(page=page)
        self.uid = uid
        self.keyword = keyword
        self.type = type

class RankingListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": int
    }

    def __init__(
            self,
            page: int = None,
            orderBy: int = None
    ):
        super().__init__(page=page, orderBy=orderBy)

class ProblemRequestParams(RequestParams):
    __type_dict__ = {
        "contest_id": int
    }

    def __init__(
            self,
            contest_id: int = None
    ):
        self.contest_id = contest_id

class Attachment(LuoguType):
    __type_dict__ = {
        "size": int,  # 附件大小（字节）
        "uploadTime": int,  # 上传时间（时间戳）
        "downloadLink": str,  # 下载链接
        "id": str,  # 附件 ID
        "fileName": str  # 文件名
    }

class ProblemaSummary(LuoguType):
    __type_dict__ = {
        "pid": str,
        "title": str,
        "difficulty": int,
        "tags": [int],
        "wantsTranslation": bool,
        "totalSubmit": int,
        "totalAccepted": int,
        "flag": int,
        "fullScore": int,
        "type": str
    }
    pid: str
    title: str
    difficulty: int
    tags: [int]
    wantsTranslation: bool
    totalSubmit: int
    totalAccepted: int
    flag: int
    fullScore: int
    type: str

class ProblemDetails(ProblemaSummary):
    __type_dict__ = {
        **ProblemaSummary.__type_dict__,
        "background": str,
        "description": str,
        "inputFormat": str,
        "outputFormat": str,
        "samples": [(str, str)],  # 嵌套列表
        "hint": str,
        # "provider": (UserSummary, TeamSummary),
        "attachments": [Attachment],
        "canEdit": bool,
        # "limits": {
        #     "time": [int],
        #     "memory": [int]
        # } ,
        "showScore": bool,
        "score": int,
        "stdCode": str,
        # "vjudge": {
        #    "origin": str,
        #    "link": str,
        #    "id": str
        # },
        "translation": str
    }
    background: str
    description: str
    inputFormat: str
    outputFormat: str
    samples: [(str, str)]
    hint: str
    attachments: [Attachment]
    canEdit: bool
    showScore: bool
    score: int
    stdCode: str
    translation: str

class ProblemData(LuoguType):
    __type_dict__ = {
        "problem": ProblemDetails,
        # "contest": ContestSummary,
        # "discussions": [LegacyPostSummary],
        "bookmarked": bool,
        "vjudgeUsername": str,
        # "recommendations": [LegacyProblemSummary],  # 列表中的每个元素是 LegacyProblemSummary
        "lastLanguage": int,
        "lastCode": str,
        # "privilegedTeams": [TeamSummary],
        "userTranslation": str,
    }
    problem: ProblemDetails
    bookmarked: bool
    vjudgeUsername: str
    lastLanguage: int
    lastCode: str
    userTranslation: str

class TestCase(LuoguType):
    __type_dict__ = {
        "upid": int,  # 测试用例唯一 ID
        "inputFileName": str,  # 输入文件名
        "outputFileName": str,  # 输出文件名
        "timeLimit": int,  # 时间限制（毫秒）
        "memoryLimit": int,  # 内存限制（MB）
        "fullScore": int,  # 满分
        "isPretest": bool,  # 是否为预测试
        "subtaskId": int  # 所属子任务 ID
    }
    upid: int
    inputFileName: str
    outputFileName: str
    timeLimit: int
    memoryLimit: int
    fullScore: int
    isPretest: bool
    subtaskId: int

class ScoringStrategy(LuoguType):
    __type_dict__ = {
        "type": int,    # 评分策略类型
        "script": str   # 评分脚本内容
    }

class ProblemSettings(LuoguType):
    __type_dict__ = {
        "title": str,
        "background": str,
        "description": str,
        "inputFormat": str,
        "outputFormat": str,
        "samples": [(str, str)],
        "hint": str,
        "translation": str,
        "needsTranslation": bool,
        "acceptSolution": bool,
        "allowDataDownload": bool,
        "tags": [int],
        "difficulty": int,
        "showScore": bool,
        "flag": int
    }
    title: str
    background: str
    description: str
    inputFormat: str
    outputFormat: str
    samples: [(str, str)]
    hint: str
    translation: str
    needsTranslation: bool
    acceptSolution: bool
    allowDataDownload: bool
    tags: [int]
    difficulty: int
    showScore: bool
    flag: int
    @staticmethod
    def get_default():
        return ProblemSettings(
            json={
                "title": "",
                "background": "",
                "description": "",
                "inputFormat": "",
                "outputFormat": "",
                "samples": [],
                "hint": "",
                "translation": "",
                "needsTranslation": False,
                "acceptSolution": True,
                "allowDataDownload": False,
                "tags": [],
                "difficulty": 0,
                "showScore": True,
                "flag": 0
            }
        )

class TestCaseSettings(LuoguType):
    __type_dict__ = {
        "cases": [TestCase],  # 测试用例列表
        # "subtaskScoringStrategies": {int: ScoringStrategy},  # 子任务评分策略（字典）
        "scoringStrategy": ScoringStrategy,  # 总评分策略
        "showSubtask": bool  # 是否显示子任务
    }
    case: [TestCase]
    subtaskScoringStrategies: {int: ScoringStrategy}
    scoringStrategy: ScoringStrategy
    showSubtask: bool

class ProblemListRequestResponse(Response):
    __type_dict__ = {
        "problems": [ProblemaSummary],
        "count": int,
        "perPage": int,
        "page": int
    }
    problems : [ProblemaSummary]

class ProblemSettingsRequestResponse(Response):
    __type_dict__ = {
        "problem": ProblemDetails,
        "problemSettings": ProblemSettings,
        "testCaseSettings": TestCaseSettings,
        "comment": str,
        "clonedFrom": bool,
        "isClonedTestCases": bool,
        "updating": bool,
        "testDataDownloadLink": str,
        # "updateStatus": {
        #     "success": bool,
        #     "message": str
        # }
        "isProblemAdmin": bool,
        # "privilegedTeams": [TeamSummary]
    }
    problemSettings: ProblemSettings
    testCaseSettings: TestCaseSettings
    comment: str

class ProblemModifiedResponse(Response):
    __type_dict__ = {
        "pid": str
    }
    pid: str

class UpdateTestCasesSettingsResponse(Response):
    __type_dict__ = {
        "problem": ProblemDetails,
        "testCases": [TestCase],
        "scoringStrategy": ScoringStrategy,
        # "subtaskScoringStrategies": [ScoringStrategy]
    }
    problem: ProblemDetails
    testCases: [TestCase]
    scoringStrategy: ScoringStrategy
    subtaskScoringStrategies: [ScoringStrategy]

class LuoguCookies(LuoguType):
    __type_dict__ = {
        "__client_id": str,
        "_uid": str,
    }

    def __init__(self, __client_id: str, _uid: str):
        self.__setattr__( "__client_id", __client_id )
        self._uid = _uid

    @staticmethod
    def from_file(path: str):
        ret = LuoguCookies("", "")

        with open(path, 'r') as json_file:
            data = json.load(json_file)

        ret.parse(data)

        return ret