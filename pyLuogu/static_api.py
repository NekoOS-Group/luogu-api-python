from .api import luoguAPI
from .types import *
from .bits.ultility import CachePool

class staticLuoguAPI:
    def __init__(
            self,
            base_url="https://www.luogu.com.cn",
            cookies: LuoguCookies = None
    ):
        self.inner = luoguAPI(base_url=base_url, cookies=cookies)
        problem_cache_pool = CachePool[ProblemDetails](
                default_cache_duration = 1200,
                default_load_function = lambda pid: self.inner.get_problem(pid).problem
        )
        problem_setting_cache = CachePool[ProblemDetails](
                default_cache_duration = 1200,
                default_load_function = lambda pid: self.inner.get_problem_settings(pid).problemSettings 
        )

luogu = staticLuoguAPI()