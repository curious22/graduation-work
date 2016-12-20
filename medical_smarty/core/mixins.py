from core.helpers import BColors

class Py3RedisSpider(object):
    def make_request_from_data(self, data):
        # By default, data is an URL.
        data = data.decode()
        if '://' in data:
            return self.make_requests_from_url(data)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, data)


class RedisQueueMixin(object):
    def push_into_redis(self, list_):
        for url in list_:
            self.redis_client.lpush(self.queue, url)
            print(
                BColors.OKGREEN +
                'URL {} send to {} queue'.format(url, self.queue) +
                BColors.ENDC
            )
