from rest_framework.throttling import SimpleRateThrottle


class Throttles(SimpleRateThrottle):
    scope = 'THROTTLE'

    def get_cache_key(self, request, view):
        if not request.user:
            return self.get_ident(request)
        return request.user.id

