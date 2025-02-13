from typing import List, Tuple, Literal, Dict, TypeVar, Generic

from .bits.ultility import JsonSerializable, Printable

__all__ = [
    "LuoguType",
    "RequestParams",
    "Response",
    "ListRequestParams",
    "ProblemListRequestParams",
    "ProblemSetListRequestParams",
    "UserListRequestParams",
    "RecordListRequestParams",
    "ThemeListRequestParams",
    "ArticleListRequestParams",
    "BlogListRequestParams",
    "RankingListRequestParams",
    "ProblemRequestParams",
    "UserSearchRequestParams",
    "DiscussionRequestParams",
    "ActivityReuqestParams",
    "ProblemSummary",
    "VjudgeSummary",
    "UserSummary",
    "TeamSummary",
    "TeamMember",
    "Provider",
    "Attachment",
    "ProblemDetails",
    "TestCase",
    "ScoringStrategy",
    "ProblemSettings",
    "TestCaseSettings",
    "UserDetails",
    "ProblemSetSummary",
    "ProblemSetDetails",
    "ContestSummary",
    "ContestDetails",
    "ContestSettings",
    "Activity",
    "Forum",
    "Reply",
    "PostSummary",
    "Post",
    "Paste",
    "Image",
    "TagDetail",
    "TagType",
    "TeamDetail",
    "ProblemListRequestResponse",
    "ProblemSetListRequestResponse",
    "ProblemDataRequestResponse",
    "ProblemSettingsRequestResponse",
    "ProblemModifiedResponse",
    "UpdateTestCasesSettingsResponse",
    "ProblemSetDataRequestResponse",
    "ProblemSolutionRequestResponse",
    "ContestDataRequestResponse",
    "ContestListRequestResponse",
    "UserDataRequestResponse",
    "DiscussionRequestResponse",
    "ActivityRequestResponse",
    "TeamDataRequestResponse",
    "TeamMemberRequestResponse",
    "PasteRequestResponse",
    "ArticleDataRequestResponse",
    "TagRequestResponse",
    "LuoguCookies",
    "ProblemType",
    "ProblemSetType",
    "TransferProblemType"
]

ProblemType = Literal["P", "U", "T", "B", "CF", "AT", "UVA", "SP"]
ProblemSetType = Literal["official", "select"]
TransferProblemType = Literal["P", "U", "B"] | int

class LuoguType(JsonSerializable, Printable):
    __type_dict__ = {}

    def __init__(self,json=None):
        super().__init__(json)

class RequestParams(LuoguType):
    pass

class Response(LuoguType):
    pass

T_of_list = TypeVar("T_of_list", bound=LuoguType)

class PagedList(LuoguType, Generic[T_of_list]):
    __type_dict__ = {
        "results": [T_of_list],
        "count": int,
        "perPage": int,
    }
    results: List[T_of_list]
    count: int
    perPage: int

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

class ProblemSketch(LuoguType):
    __type_dict__ = {
        "pid": str,
        "title": str,
        "difficulty": int,
        "type": str,
        "submitted": bool,
        "accepted": bool
    }
    pid: str
    title: str
    difficulty: int
    type: str
    submitted: bool
    accepted: bool

class ProblemSummary(ProblemSketch):
    __type_dict__ = {
        **ProblemSketch.__type_dict__,
        "tags": [int],
        "totalSubmit": int,
        "totalAccepted": int,
        "flag": int,
        "fullScore": int,
    }
    tags: List[int]
    totalSubmit: int
    totalAccepted: int
    flag: int
    fullScore: int

    def inline(self):
        return f"{self.pid} {self.title} {self.tags} {self.difficulty}"

class VjudgeSummary(LuoguType):
    __type_dict__ = {
        "origin": str,
        "link": str,
        "id": str
    }
    origin: str
    link: str
    id: str

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

class ProblemContent(LuoguType):
    __type_dict__ = {
        "user": UserSummary,
        "version": int,
        "name": str,
        "background": str,
        "description": str,
        "formatI": str,
        "formatO": str,
        "hint": str,
        "locale": str
    }
    user: UserSummary | None
    version: int
    name: str
    background: str
    description: str
    formatI: str
    formatO: str
    hint: str
    locale: str

class Group(LuoguType):
    __type_dict__ = {
        "id": int,
        "name": str,
        "no": int
    }
    id: int
    name: str
    no: int

class TeamMember(LuoguType):
    __type_dict__ = {
        "group": Group,
        "user": UserSummary,
        "type": int,
        "permission": int,
        "realName": str
    }
    group: Group | None
    user: UserSummary
    type: int
    permission: int
    realName: str

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

class ProblemSetSummary(LuoguType):
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
    deadline: int | None
    problemCount: int
    marked: bool
    markCount: int
    id: int
    title: str
    type: int
    provider: Provider

class ContestSketch(LuoguType):
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

class PostSketch(LuoguType):
    __type_dict__ = {
        "id": int,
        "title": str,
        "author": UserSummary,
        "time": int
    }
    id: int
    title: str
    author: UserSummary
    time: int

class PostSummary(PostSketch):
    __type_dict__ = {
        "content": str,
        "createTime": int,
        "updateTime": int,
        "forum": Forum,
        "topped": bool,
        "valid": bool,
        "locked": bool,
        "replyCount": int,
        "recentReply": Reply,
    }
    content: str
    createTime: int
    updateTime: int
    forum: Forum
    topped: bool
    valid: bool
    locked: bool
    replyCount: int
    recentReply: Reply

class Prize(LuoguType):
    __type_dict__ = {
        "year": int,
        "contestName": str,
        "prize": str
    }
    year: int
    contestName: str
    prize: str

class EloRatingSummary(LuoguType):
    __type_dict__ = {
        "contest": ContestSketch,
        "rating": int,
        "time": int,
        "latest": bool
    }
    contest: ContestSketch
    rating: int
    time: int
    latest: bool

class ProblemDetails(ProblemSummary):
    __type_dict__ = {
        **ProblemSummary.__type_dict__,
        "content": ProblemContent, 
        # "contenu" : ???,
        "samples": [(str, str)],
        "provider": Provider,
        "attachments": [Attachment],
        "limits": [(int, int)],
        "showScore": bool,
        "score": int,
        "stdCode": str,
        "vjudge": VjudgeSummary,
        "acceptLanguages": [int]
    }
    content: ProblemContent
    samples: List[Tuple[str, str]]
    provider: Provider
    attachments: List[Attachment]
    limits: List[Tuple[int, int]]
    showScore: bool
    score: int
    stdCode: str
    vjudge: VjudgeSummary | None
    acceptLanguages: List[int]

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
        # "rating": 'Rating', # aka guzhi
        "registerTime": int,
        "introduction": str,
        "prize": [Prize],
        "elo": EloRatingSummary,
        "eloMax": EloRatingSummary,
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
    prize: List[Prize]
    elo: EloRatingSummary
    eloMax: EloRatingSummary
    userRelationship: int
    reverseUserRelationship: int
    passedProblemCount: int
    submittedProblemCount: int

class ProblemSetDetails(ProblemSetSummary):
    __type_dict__ = {
        **ProblemSetSummary.__type_dict__,
        "description": str,
        "problems": [ProblemSummary],
        # "userScore": Optional[Dict[str, Union[UserSummary, int, Dict[str, Optional[int]], Dict[str, bool]]]],
    }
    description: str
    problems: List[ProblemSummary]
    # userScore: Optional[Dict[str, Union[UserSummary, int, Dict[str, Optional[int]], Dict[str, bool]]]]
    
class ContestSummary(ContestSketch):
    __type_dict__ = {
        **ContestSketch.__type_dict__,
        "ruleType": int,
        "visibilityType": int,
        "invitationCodeType": int,
        "rated": bool,
        "problemCount": int,
        "host": Provider,
    }
    ruleType: int
    visibilityType: int
    invitationCodeType: int
    rated: bool
    problemCount: int
    host: Provider

class ContestDetails(ContestSummary):
    __type_dict__ = {
        **ContestSummary.__type_dict__,
        "description": str,
        "totalParticipants": int,
        "eloThreshold": int,
        "eloDone": bool,
        "canEdit": bool,
        "problems": [ProblemSummary],
        "isScoreboardFrozen": bool,
    }
    description: str
    totalParticipants: int
    eloDone: bool
    eloThreshold: int
    canEdit: bool
    problems: List[ProblemSummary]
    isScoreboardFrozen: bool

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
    ratingGroup: str | None
    eloThreshold: int | None
    eloCenter: int | None

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

class TeamSettings(LuoguType):
    __type_dict__ = {
        "description": str,
        "notice": str,
        "contact": {str: str},
        "joinPermission": int
    }
    description: str
    notice: str
    contact: Dict[str, str]
    joinPermission: int

class TeamDetail(TeamSummary):
    __type_dict__ = {
        **TeamSummary.__type_dict__,
        "createTime": int,
        "master": UserSummary,
        "setting": TeamSettings,
        "premiumUntil": int,
        "type": int,
        "memberCount": int
    }
    createTime: int
    master: UserSummary
    setting: TeamSettings
    premiumUntil: int | None
    type: int
    memberCount: int

class Post(PostSummary):
    __type_dict__ = {
        **PostSummary.__type_dict__,
        "pinnedReply": Reply,
        "content": str
    }
    pinnedReply: None
    content: str

class Paste(LuoguType):
    __type_dict__ = {
        "data": str,
        "id": str,
        "user": UserSummary,
        "time": int,
        "public": bool
    }
    data: str
    id: str
    user: UserSummary
    time: int
    public: bool

class Image(LuoguType):
    __type_dict__ = {
        "thumbnailUrl": str,
        "url": str,
        "id": str,
        "provider": UserSummary,
        "uploadTime": int,
        "size": int
    }
    thumbnailUrl: str
    url: str
    id: str
    provider: UserSummary
    uploadTime: int
    size: int

class Article(LuoguType):
    __type_dict__ = {
        "lid": str,
        "title": str,
        "time": int,
        "author": UserSummary,
        "upvote": int,
        "replyCount": int,
        "favorCount": int,
        "category": int,
        "status": int,
        "solutionFor": ProblemSketch,
        "promoteStatus": int,
        # "collection": Optional[Any],
        "content": str,
        "categoryOld": str,
        "contentFull": bool,
        "adminNote": str,
        "adminComment": str,
        "voted": int,
        "canReply": bool,
        "canEdit": bool
    }
    lid: str
    title: str
    time: int
    author: UserSummary
    upvote: int
    replyCount: int
    favorCount: int
    category: int
    status: int
    solutionFor: ProblemSketch
    promoteStatus: int
    # collection: Optional[Any]
    content: str
    categoryOld: str
    contentFull: bool
    adminNote: str | None
    adminComment: str
    voted: int | None
    canReply: bool
    canEdit: bool

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
    }
    problems : List[ProblemSummary]
    count : int
    perPage: int

class ProblemSetListRequestResponse(Response):
    __type_dict__ = {
        "trainings": [ProblemSetSummary],
        "count": int,
        "perPage": int,
        "page": int
    }
    problems : List[ProblemSetSummary]
    count : int
    perPage: int
    page: int

class ProblemDataRequestResponse(LuoguType):
    __type_dict__ = {
        "problem": ProblemDetails,
        "translations": {str: ProblemContent},
        "bookmarked": bool,
        "contest": ContestSketch,
        "vjudgeUsername": str,
        "lastLanguage": int,
        "lastCode": str,
        "recommendations": [ProblemSketch],
        "forum": Forum,
        "discussions": [PostSketch],
        "canEdit": bool
    }
    problem: ProblemDetails
    translations: Dict[str, ProblemContent]
    bookmarked: bool
    contest: ContestSketch | None
    vjudgeUsername: str | None
    lastLanguage: int
    lastCode: str
    recommendations: List[ProblemSummary]
    discussions: List[PostSummary]
    canEdit: bool

class ProblemSettingsRequestResponse(Response):
    __type_dict__ = {
        # "problemDetails": LegacyProblemDetails,
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

class ProblemSolutionRequestResponse(Response):
    __type_dict__ = {
        "perPage": int,
        "count": int,
        "solutions": [Article],
        "problem": ProblemSketch,
        "acceptSolution": bool,
    }
    perPage: int
    count: int
    solutions: List[Article]
    problem: ProblemSketch
    acceptSolution: bool

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

class ContestListRequestResponse(Response):
    __type_dict__ = {
        "contests": [ContestSummary],
        "count": int,
        "perPage": int
    }
    contests: List[ContestSummary]
    count: int
    perPage: int

class UserDataRequestResponse(LuoguType):
    __type_dict__ = {
        "user": UserDetails,
        "passedProblems": [ProblemSummary],
        "submittedProblems": [ProblemSummary],
        "teams": [TeamSummary]
    }
    user: UserDetails
    passedProblems: List['ProblemSummary']
    submittedProblems: List['ProblemSummary']
    teams: List[TeamSummary]

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

class TeamDataRequestResponse(Response):
    __type_dict__ = {
        "team": TeamDetail,
        "currentTeamMember": TeamMember,
        "latestDiscussions": [PostSummary],
        "groups": [Group],
        "usages": {str: (int, int)}
    }
    team: TeamDetail
    currentTeamMember: TeamMember | None
    latestDiscussions: PostSummary | None
    groups: List[Group]
    usages: Dict[str, Tuple[int, int]]

class TeamMemberRequestResponse(Response):
    __type_dict__ = {
        "members": [TeamMember],
        "perPage": int,
        "count": int,
        "group": Group,
        # "groupMemberCount": {int: int}
    }
    member: TeamMember
    perPage: int
    count: int
    group: Group
    # groupMemberCount: Dict[int, int]

class PasteRequestResponse(Response):
    __type_dict__ = {
        "paste": Paste,
        "canEdit": bool
    }
    paste: Paste
    canEdit: bool

class ArticleDataRequestResponse(Response):
    __type_dict__ = {
        "article": Article,
        "favored": bool,
        "voted": int,
        "canReply": bool,
        "canEdit": bool
    }
    article: Article
    favored: bool
    voted: int | None
    canReply: bool
    canEdit: bool

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
