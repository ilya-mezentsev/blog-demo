import random
from typing import (
    Mapping,
    Any,
    Optional,
    Tuple,
    Sequence,
)
from uuid import uuid4

import lorem
from locust import (
    LoadTestShape,
    FastHttpUser,
    task,
)


DEFAULT_PASSWORD = 'password'

exits_users_nicknames = [f'user_{i}' for i in range(100)]
exits_moderators_nicknames = [f'moderator_{i}' for i in range(10)]
exists_articles_paths = []


class AnonymousUser(FastHttpUser):
    weight = 10

    @task
    def get_articles_and_comments(self) -> None:
        articles = self.client.get('/articles').json()['data']['articles']
        random_article: Mapping[str, Any] = random.choice(articles)

        self.client.get(f'/articles/{random_article["id"]}')
        self.client.get(f'/articles/{random_article["id"]}/comments')

    @task
    def register_and_update_user(self) -> None:
        new_user_response = self.client.post('/users', json={
            'nickname': generate_random_user_nickname(),
            'password': DEFAULT_PASSWORD,
        }).json()

        if 'data' in new_user_response:
            new_user = new_user_response['data']['user']

            self.client.post('/session', json={
                'nickname': new_user['nickname'],
                'password': DEFAULT_PASSWORD,
            })

            self.client.patch(f'/users/{new_user["id"]}', json={
                'nickname': generate_random_user_nickname(),
            })

        # Тут нужно удалить сессию юзера,
        # т.к. у следующих запросах она почему-то сохраняется в клиенте
        self.client.delete('/session')


class AuthorizedUser(FastHttpUser):
    weight = 10

    def on_start(self) -> None:
        self.client.post('/session', json={
            'nickname': get_random_user_nickname(),
            'password': DEFAULT_PASSWORD,
        })

    @task
    def crud_with_comments(self) -> None:
        articles = self.client.get('/articles').json()['data']['articles']
        random_article: Mapping[str, Any] = random.choice(articles)

        self.client.get(f'/articles/{random_article["id"]}')
        self.client.get(f'/articles/{random_article["id"]}/comments')

        create_comment_response = self.client.post(f'/articles/{random_article["id"]}/comments', json={
            'text': lorem.sentence(),
        }).json()
        if 'data' in create_comment_response:
            created_comment_data = create_comment_response['data']['comment']

            self.client.patch(f'/articles/{random_article["id"]}/comments/{created_comment_data["id"]}', json={
                'text': lorem.sentence(),
            })

    @task
    def create_update_delete_article(self) -> None:
        created_article_response = self.client.post(
            path='/articles',
            json={
                'title': lorem.sentence(),
                'description': lorem.paragraph(),
                'content': '\n\n'.join(lorem.paragraph() for _ in range(3)),
            },
        ).json()

        if 'data' in created_article_response:
            created_article = created_article_response['data']['article']

            self.client.patch(
                path=f'/articles/{created_article["id"]}',
                json={
                    'title': lorem.sentence(),
                    'description': lorem.paragraph(),
                    'content': '\n\n'.join(lorem.paragraph() for _ in range(3)),
                },
            )

            self.client.delete(f'/articles/{created_article["id"]}')

    def on_stop(self) -> None:
        self.client.delete('/session')


class Moderator(FastHttpUser):
    weight = 1

    def on_start(self) -> None:
        self.client.post('/session', json={
            'nickname': get_random_moderator_nickname(),
            'password': DEFAULT_PASSWORD,
        })

    @task
    def delete_random_article(self) -> None:
        articles_response = self.client.get('/articles').json()
        if 'data' in articles_response:
            articles = articles_response['data']['articles']
            random_article = random.choice(articles)
            self.client.delete(f'/articles/{random_article["id"]}')

    @task
    def delete_random_comment(self) -> None:
        articles_response = self.client.get('/articles').json()
        if 'data' in articles_response:
            articles = articles_response['data']['articles']
            random_article = random.choice(articles)

            comments = (
                self.client.
                get(f'/articles/{random_article["id"]}/comments').
                json().
                get('data', {}).
                get('comments', [])
            )

            # У случайной статьи вполне может не оказаться комментариев
            if comments:
                random_comment = random.choice(comments)
                self.client.delete(f'/articles/{random_article["id"]}/comments/{random_comment["id"]}')

    def on_stop(self) -> None:
        self.client.delete('/session')


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages: Sequence[Mapping[str, int]] = [
        {'duration': 30, 'users': 50, 'spawn_rate': 10},
        {'duration': 210, 'users': 150, 'spawn_rate': 10},
        {'duration': 390, 'users': 200, 'spawn_rate': 10},
        {'duration': 400, 'users': 10, 'spawn_rate': 10},
        {'duration': 410, 'users': 1, 'spawn_rate': 1},
    ]
    stop_at_end = True

    def tick(self) -> Optional[Tuple[int, int]]:
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage['duration']:
                tick_data = (stage['users'], stage['spawn_rate'])
                return tick_data

        return None


def generate_random_user_nickname() -> str:
    return f'user_{str(uuid4())}'


def get_random_user_nickname() -> str:
    return random.choice(exits_users_nicknames)


def get_random_moderator_nickname() -> str:
    return random.choice(exits_moderators_nicknames)
