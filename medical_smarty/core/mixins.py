class Py3RedisSpider(object):
    def make_request_from_data(self, data):
        # By default, data is an URL.
        data = data.decode()
        if '://' in data:
            return self.make_requests_from_url(data)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, data)