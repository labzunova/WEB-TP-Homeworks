from django.core.management.base import BaseCommand
from random import choice
from faker import Faker
from app.models import Question
from app.models import Answer
from app.models import User, Author
from app.models import Tag,QuestionLikes

f = Faker()


def fill_users(cnt):
    users = list(
        User.objects.values_list(
            'identificator', flat=True
        )
    )
    users_count = User.objects.all().count()
    for i in range(cnt):
        author = Author.objects.create()  # доп информация(фото)
        User.objects.create(
            identificator=users_count + i + 1,
            name=f.name(),
            password='1111',
            email=f.email(),
            author=author,
        )


def fill_questions(cnt):
    users_ids = list(
        User.objects.values_list(
            'id', flat=True
        )
    )
    tags = Tag.objects.all()
    count = len(Question.objects.all())
    for i in range(cnt):
        question = Question.objects.create(
            identificator=count + i,
            rating=0,
            answers_count=0,
            title=f.sentence()[:128],
            text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            user=User.objects.filter(id=choice(users_ids)).first(),
        )
        question.tags.add(choice(tags))


def fill_answers(cnt):
    questions_ids = list(
        Question.objects.values_list(
            'identificator', flat=True
        )
    )
    users_ids = list(
        User.objects.values_list(
            'identificator', flat=True
        )
    )

    for i in range(cnt):
        question_ = Question.objects.filter(identificator=choice(questions_ids)).first()
        question_.answers_count += 1
        question_.save(update_fields=['answers_count'])
        Answer.objects.create(
            author=User.objects.filter(identificator=choice(users_ids)).first(),
            question=question_,
            rating=0,
            text='. '.join(f.sentences(f.random_int(min=2, max=5))),
        )


def fill_tags(cnt):
    for i in range(cnt):
        Tag.objects.create(
            title=f.word(),
        )


def fill_likes_on_questions(cnt):
    questions_ids = list(
        Question.objects.values_list(
            'identificator', flat=True
        )
    )
    users_ids = list(
        User.objects.values_list(
            'identificator', flat=True
        )
    )

    for i in range(cnt):
        question_ = Question.objects.filter(identificator=choice(questions_ids)).first()
        question_.rating += 1
        question_.save(update_fields=['rating'])
        QuestionLikes.objects.create(
            author=User.objects.filter(identificator=choice(users_ids)).first(),
            question=question_,
            like=1,
        )


def fill_likes_on_answers(cnt):
    answers_ids = list(
        Answer.objects.values_list(
            'identificator', flat=True
        )
    )
    users_ids = list(
        User.objects.values_list(
            'identificator', flat=True
        )
    )

    for i in range(cnt):
        answer_ = Question.objects.filter(identificator=choice(answers_ids)).first()
        answer_.rating += 1
        answer_.save(update_fields=['rating'])
        QuestionLikes.objects.create(
            author=User.objects.filter(identificator=choice(users_ids)).first(),
            answer=answer_,
            like=1,
        )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--all', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--q_likes', type=int)
        parser.add_argument('--a_likes', type=int)

    def handle(self, *args, **options):
        if options['all']:
            n = options['all']
            print("Generating the base")
            fill_tags(n*5)
            fill_users(n*100)
            fill_questions(n*100)
            fill_answers(n*100)
            print("done!")

        if options['users']:
            print("Generating ", options['users'], " users")
            fill_users(options['users'])

        if options['questions']:
            print("Generating ", options['questions'], " questions")
            fill_questions(options['questions'])

        if options['answers']:
            print("Generating ", options['answers'], " answers")
            fill_answers(options['answers'])

        if options['tags']:
            print("Generating ", options['tags'], " tags")
            fill_answers(options['tags'])

        if options['q_likes']:
            print("Generating ", options['q_likes'], " question likes")
            fill_likes_on_questions(options['q_likes'])

        if options['a_likes']:
            print("Generating ", options['a_likes'], " answers likes")
            fill_likes_on_answers(options['a_likes'])
