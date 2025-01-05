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


class ProblemAbstract(LuoguType):
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

class ProblemDetails(ProblemAbstract):
    __type_dict__ = {
        **ProblemAbstract.__type_dict__,
        "background": str,
        "description": str,
        "inputFormat": str,
        "outputFormat": str,
        "samples": [(str, str)],  # 嵌套列表
        "hint": str,
        # "provider": (UserSummary, TeamSummary),
        # "attachments": [{
        #    "size": int,
        #    "uploadTime": int,
        #    "downloadLink": str,
        #    "id": str,
        #    "fileName": str
        # }],
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

class ProblemData(LuoguType):
    __type_dict__ = {
        "problem": ProblemDetails,  # 嵌套 ProblemDetails，并支持 Maybe 类型
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


class ProblemListRequestResponse(Response):
    __type_dict__ = {
        "problems": [ProblemAbstract],
        "count": int,
        "perPage": int,
        "page": int
    }

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