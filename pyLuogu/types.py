from typing import List, Tuple, Literal, Dict, Union, Optional, Any

ProblemType = Literal["P", "U", "T", "B", "CF", "AT", "UVA", "SP"]
TransferProblemType = Literal["P", "U", "B"] | int

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
    page: int
    orderBy: int
    keyword: str
    content: bool
    type: ProblemType
    difficulty: int
    tag: str

class ProblemSetListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "keyword": str,
        "type": str
    }

class UserListRequestParams(ListRequestParams):
    __type_dict__ = {
        "user": int,
        "page": int,
        "orderBy": int
    }

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

class ThemeListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": str,
        "order": str,
        "type": str
    }

class ArticleListRequestParams(LuoguType):
    __type_dict__ = {
        "user": int,
        "page": int,
        "category": int,
        "ascending": bool,
        "promoted": bool,
        "title": str
    }

class BlogListRequestParams(ListRequestParams):
    __type_dict__ = {
        "uid": int,
        "keyword": str,
        "type": str,
        "page": int
    }

class RankingListRequestParams(ListRequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": int
    }

class ProblemRequestParams(RequestParams):
    __type_dict__ = {
        "contest_id": int
    }

class UserSearchRequestParams(RequestParams):
    __type_dict__ = {
        "keyword": str
    }

class DiscussionRequestParams(RequestParams):
    __type_dict__ = {
        "page": int,
        "orderBy": int
    }

class ActivityReuqestParams(RequestParams):
    __type_dict__ = {
        "user": int,
        "page": int
    }
    user: int
    page: int

class ProblemSummary(LuoguType):
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
    tags: List[int]
    wantsTranslation: bool
    totalSubmit: int
    totalAccepted: int
    flag: int
    fullScore: int
    type: str

    def inline(self):
        return f"{self.pid} {self.title} {self.tags} {self.difficulty}"

class UserSummary(LuoguType):
    __type_dict__ = {
        "uid": int, 
        "name": str,
        "avatar": str, 
        "slogan": str, 
        "badge": str, 
        "isAdmin": bool, 
        "isBanned": bool, 
        "isRoot": bool, 
        "color": str, 
        "ccfLevel": int, 
        "background": str, 
    }
    uid: int
    name: str
    avatar: str
    slogan: str
    badge: str
    isAdmin: bool
    isBanned: bool
    color: str
    ccfLevel: int
    background: str
    isRoot: bool

class TeamSummary(LuoguType):
    __type_dict__ = {
        "id": int,
        "name": str,
        "isPremium": bool
    }
    id: int
    name: str
    isPremium: bool

class Provider(LuoguType):
    __type_dict__ = {
        "user": UserSummary,
        "team": TeamSummary
    }
    user: UserSummary | None
    team: TeamSummary | None

    def __init__(self, json=None):
        super().__init__(json=None)
        self.user = None
        self.team = None
        if json.get("uid") is not None:
            self.user = UserSummary(json)
        else:
            self.team = TeamSummary(json)

    def get(self):
        return self.user or self.team

class Attachment(LuoguType):
    __type_dict__ = {
        "size": int,  # 附件大小（字节）
        "uploadTime": int,  # 上传时间（时间戳）
        "downloadLink": str,  # 下载链接
        "id": str,  # 附件 ID
        "fileName": str  # 文件名
    }
    size: int
    uploadTime: int
    downloadLink: str
    id: str
    fileName: str

class ProblemDetails(ProblemSummary):
    __type_dict__ = {
        **ProblemSummary.__type_dict__,
        "background": str,
        "description": str,
        "inputFormat": str,
        "outputFormat": str,
        "samples": [(str, str)],
        "hint": str,
        "provider": Provider,
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
    pid: str
    title: str
    difficulty: int
    tags: List[int]
    wantsTranslation: bool
    totalSubmit: int
    totalAccepted: int
    flag: int
    fullScore: int
    type: str
    background: str
    description: str
    inputFormat: str
    outputFormat: str
    samples: List[Tuple[str, str]]
    hint: str
    provider: Provider
    attachments: List[Attachment]
    canEdit: bool
    showScore: bool
    score: int
    stdCode: str
    translation: str

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
        "comment": str,
        "needsTranslation": bool,
        "acceptSolution": bool,
        "allowDataDownload": bool,
        "tags": [int],
        "difficulty": int,
        "showScore": bool,
        "providerID": int,
        "flag": int
    }
    title: str
    background: str
    description: str
    inputFormat: str
    outputFormat: str
    samples: List[Tuple[str, str]]
    hint: str
    comment: str
    translation: str
    needsTranslation: bool
    acceptSolution: bool
    allowDataDownload: bool
    tags: List[int]
    difficulty: int
    showScore: bool
    providerID: int
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
                "comment": "",
                "translation": "",
                "needsTranslation": False,
                "acceptSolution": True,
                "allowDataDownload": False,
                "tags": [],
                "difficulty": 0,
                "showScore": True,
                "providerID": None,
                "flag": 0
            }
        )
    def get_markdown(self):
        return "\n## 题目背景\n" + str(self.background) + \
        "\n## 题目描述\n" + str(self.description) + \
        "\n## 输入格式\n" + str(self.inputFormat) + \
        "\n## 输出格式\n" + str(self.outputFormat) + \
        "\n## 数据范围与提示\n" + str(self.hint)
    
    def append_tags(self, tags: List[int] | int ):
        if isinstance(tags, int):
            tags = [tags]
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)

    def remove_tags(self, tags: List[int] | int):
        if isinstance(tags, int):
            tags = [tags]
        for tag in tags:
            if tag in self.tags:
                self.tags.remove(tag)

class TestCaseSettings(LuoguType):
    __type_dict__ = {
        "cases": [TestCase],  # 测试用例列表
        "subtaskScoringStrategies": {str: ScoringStrategy},  # 子任务评分策略（字典）
        "scoringStrategy": ScoringStrategy,  # 总评分策略
        "showSubtask": bool  # 是否显示子任务
    } 
    cases: List[TestCase] 
    subtaskScoringStrategies: Dict[str, ScoringStrategy]
    scoringStrategy: ScoringStrategy
    showSubtask: bool

class UserDetails(UserSummary):
    __type_dict__ = {
        **UserSummary.__type_dict__,
        "followingCount": int,
        "followerCount": int,
        "ranking": int,
        "eloValue": int,
        # "rating": 'Rating',
        "registerTime": int,
        "introduction": str,
        #"prize": List[Dict[str, Union[str, int]]],
        # "elo": 'EloRatingSummary'
        "userRelationship": int,
        "reverseUserRelationship": int,
        "passedProblemCount": int,
        "submittedProblemCount": int
    }
    followingCount: int
    followerCount: int
    ranking: int
    eloValue: int
    # rating: Rating
    registerTime: int
    introduction: str
    # prize: List[Dict[str, Union[str, int]]]
    # elo: 'EloRatingSummary'
    userRelationship: int
    reverseUserRelationship: int
    passedProblemCount: int
    submittedProblemCount: int

class SelfDetails(LuoguType):
    __type_dict__ = {
        "verified": bool,
        "unreadMessageCount": int,
        "unreadNoticeCount": int,
        "organization": Optional[str],
        "email": str,
        "phone": str
    }
    # ...existing fields...

class ProblemSet(LuoguType):
    __type_dict__ = {
        "createTime": int,
        "deadline": int,
        "problemCount": int,
        "marked": bool,
        "markCount": int,
        "id": int,
        "title": str,
        "type": int,
        "provider": Provider
    }
    createTime: int
    deadline: Optional[int]
    problemCount: int
    marked: bool
    markCount: int
    id: int
    title: str
    type: int
    provider: Provider

class ProblemSetDetails(ProblemSet):
    __type_dict__ = {
        **ProblemSet.__type_dict__,
        "description": str,
        "problems": [ProblemSummary],
        # "userScore": Optional[Dict[str, Union[UserSummary, int, Dict[str, Optional[int]], Dict[str, bool]]]],
    }
    description: str
    problems: List[ProblemSummary]
    # userScore: Optional[Dict[str, Union[UserSummary, int, Dict[str, Optional[int]], Dict[str, bool]]]]

class ContestSummary(LuoguType):
    __type_dict__ = {
        "id": int,
        "name": str,
        "startTime": int,
        "endTime": int,
    }
    id: int
    name: str
    startTime: int
    endTime: int
    
class ContestDetails(ContestSummary):
    __type_dict__ = {
        **ContestSummary.__type_dict__,
        "description": str,
        "totalParticipants": int,
        "eloDone": bool,
        "canEdit": bool,
        "ruleType": int,
        "visibilityType": int,
        "invitationCodeType": int,
        "rated": bool,
        "eloThreshold": int,
        "problemCount": int,
        "problems": [ProblemSummary],
        "isScoreboardFrozen": bool,
        "host": Provider,
    }
    description: str
    totalParticipants: int
    eloDone: bool
    canEdit: bool
    ruleType: int
    visibilityType: int
    invitationCodeType: int
    isScoreboardFrozen: bool
    rated: bool
    eloThreshold: Optional[int]
    problemCount: int
    problems: List[ProblemSummary]
    host: Provider

class ContestSettings(LuoguType):
    __type_dict__ = {
        "name": str,
        "description": str,
        "visibilityType": int,
        "invitationCodeType": int,
        "ruleType": int,
        "startTime": int,
        "endTime": int,
        "rated": bool,
        "ratingGroup": str,
        "eloThreshold": int,
        "eloCenter": int,
    }
    name: str
    description: str
    visibilityType: int
    invitationCodeType: int
    ruleType: int
    startTime: int
    endTime: int
    rated: bool
    ratingGroup: Optional[str]
    eloThreshold: Optional[int]
    eloCenter: Optional[int]

class Activity(LuoguType):
    __type_dict__ = {
        "content": str,
        "id": int,
        "type": int,
        "time": int,
        "user": UserSummary
    }
    content: str
    id: int
    type: int
    time: int
    user: UserSummary

class Forum(LuoguType):
    __type_dict__ = {
        "name": str,
        "type": int,
        "slug": str,
        "color": str,
    }
    name: str
    type: int
    slug: str
    color: str

class Reply(LuoguType):
    __type_dict__ = {
        "id": int,
        "content": str,
        "time": int,
        "author": UserSummary,
    }
    id: int
    content: str
    author: UserSummary
    time: int

class PostSummary(LuoguType):
    __type_dict__ = {
        "id": int,
        "title": str,
        "author": UserSummary,
        "createTime": int,
        "updateTime": int,
        "forum": Forum,
        "topped": bool,
        "valid": bool,
        "locked": bool,
        "replyCount": int,
        # "recentReply": Reply | bool,
    }
    id: int
    title: str
    content: str
    author: UserSummary
    createTime: int
    updateTime: int
    forum: Forum
    topped: bool
    valid: bool
    locked: bool
    replyCount: int
    # recentReply: Union[Reply, bool]

class Post(PostSummary):
    __type_dict__ = {
        **PostSummary.__type_dict__,
        "pinnedReply": Reply,
        "content": str
    }
    pinnedReply: None
    content: str

class TagDetail(LuoguType):
    __type_dict__ = {
        "id": int,
        "name": str,
        "type": int,
        "parent": int
    }
    id: int
    name: str
    type: int
    parent: int | None

class TagType(LuoguType):
    __type_dict__ = {
        "id": int,
        "name": str,
        "color": str
    }
    id: int
    name: str
    color: str

class ProblemListRequestResponse(Response):
    __type_dict__ = {
        "problems": [ProblemSummary],
        "count": int,
        "perPage": int,
        "page": int
    }
    problems : List[ProblemSummary]
    count : int
    perPage: int
    page: int

class ProblemDataRequestResponse(LuoguType):
    __type_dict__ = {
        "problem": ProblemDetails,
        "contest": ContestSummary,
        # "discussions": [LegacyPostSummary],
        "bookmarked": bool,
        "vjudgeUsername": str,
        "recommendations": [ProblemSummary], 
        "lastLanguage": int,
        "lastCode": str,
        "privilegedTeams": [TeamSummary],
        "userTranslation": str,
    }
    problem: ProblemDetails
    contest: ContestSummary
    bookmarked: bool
    vjudgeUsername: str
    recommendations: List[ProblemSummary]
    lastLanguage: int
    lastCode: str
    privilegedTeams: List[TeamSummary]
    userTranslation: str

class ProblemSettingsRequestResponse(Response):
    __type_dict__ = {
        "problemDetails": ProblemDetails,
        "problemSettings": ProblemSettings,
        "testCaseSettings": TestCaseSettings,
        # "clonedFrom": dict,
        "isClonedTestCases": bool,
        "updating": bool,
        "testDataDownloadLink": str,
        # "updateStatus": {
        #     "success": bool,
        #     "message": str
        # }
        "isProblemAdmin": bool,
        "privilegedTeams": [TeamSummary]
    }
    problemDetails: ProblemDetails
    problemSettings: ProblemSettings
    testCaseSettings: TestCaseSettings

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
        "subtaskScoringStrategies": {str: ScoringStrategy}
    }
    problem: ProblemDetails
    testCases: List[TestCase]
    scoringStrategy: ScoringStrategy
    subtaskScoringStrategies: Dict[str, ScoringStrategy]

class ProblemSetDataRequestResponse(Response):
    __type_dict__ = {
        "training": ProblemSetDetails,
        # "trainingProblems": {
        #    "result": List[List[Any]],
        #    "perPage": type(None),
        #    "count": int
        # },
        "canEdit": bool,
        "privilegedTeams": [TeamSummary]
    }
    training: ProblemSetDetails
    # trainingProblems: Dict[str, Union[List[List[Any]], None, int]]
    canEdit: bool
    privilegedTeams: List[TeamSummary]

class ContestDataRequestResponse(Response):
    __type_dict__ = {
        "contest": ContestDetails,
        "joined": bool,
        "accessLevel": int,
        # "userElo": EloRatingSummary
        # "userScore" : Optional[Dict[str, Union[UserSummary, int, Dict[str, Optional[int]], Dict[str, bool]]]]
    }
    contest : ContestDetails
    joined : bool
    accessLevel : int

class UserDataRequestResponse(LuoguType):
    __type_dict__ = {
        "user": UserDetails,
        # "eloMax": Optional[Dict[str, Union[int, bool]]],
        "passedProblems": [ProblemSummary],
        "submittedProblems": [ProblemSummary],
        # "teams": Optional[List[Dict[str, Union['TeamSummary', 'Group', 'UserSummary', int]]]]
    }
    user: UserDetails
    # eloMax: Optional[Dict[str, Union[int, bool]]]
    passedProblems: List['ProblemSummary']
    submittedProblems: List['ProblemSummary']
    # teams: Optional[List[Dict[str, Union['TeamSummary', 'Group', 'UserSummary', int]]]]

class DiscussionRequestResponse(Response):
    __type_dict__ = {
        "forum": Forum,
        "post": Post,
        "count": int,
        "perPage": int,
        "replies": [Reply],
        "canReply": bool,
    }
    forum: Forum
    post: Post
    count: int
    perPage: int 
    replies: List[Reply]
    canReply: bool

class ActivityRequestResponse(Response):
    __type_dict__ = {
        "activities": [Activity],
        "count": int,
        "perPage": int,
    }
    activities: List[Activity]
    count: int
    perPage: int

class TagRequestResponse(Response):
    __type_dict__ = {
        "tags": [TagDetail],
        "types": [TagType]
    }
    tags: List[TagDetail]
    types: List[TagType]

class LuoguCookies(LuoguType):
    __type_dict__ = {
        "__client_id": str,
        "_uid": str,
    }
    __client_id: str
    _uid: str
