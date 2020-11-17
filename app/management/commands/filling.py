from django.core.management.base import BaseCommand
from random import choice
from faker import Faker
from app.models import Question
from app.models import Answer
from app.models import User
from app.models import Tag

f = Faker()


def fill_questions(cnt):
    author_ids = list(
        User.objects.values_list(
            'name', flat=True
        )
    )
    tags = Tag.objects.all()
    count = len(Question.objects.all())
    for i in range(cnt):
        Question.objects.create(
            identificator=count,
            rating=0,
            answers_count=0,
            title=f.sentence()[:128],
            text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            author=choice(author_ids),
            tags=choice(tags),
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        fill_questions(5)

"""
    def fill_answers(self, cnt):
        questions_ids = list(
            Question.objects.values_list(
                'identificator'
            )
        )
        author_ids = list(
            User.objects.values_list(
                'name', flat=True
            )
        )

        for i in range(cnt):
            id = choice(questions_ids)
            Answer.objects.create(
                author=choice(author_ids),
                question=Question.objects.filter(identificator=id),
                rating=0,
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            )
"""
