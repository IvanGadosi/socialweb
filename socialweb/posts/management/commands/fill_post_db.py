import random
from django.core.management.base import BaseCommand
from posts.models import Post, Comment
from accounts.models import CustomUser
from categories.models import Category


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int)

    def handle(self, *args, **options):
        imgs_list=['a.jpeg','b.jpeg','c.jpeg','d.jpeg','e.jpeg','f.jpeg','g.jpeg','h.jpeg','i.jpeg','j.jpeg','k.jpeg','l.jpeg','m.jpeg','n.jpeg']
        test_imgs=["test_images/{}".format(imgs_item) for imgs_item in imgs_list]

        user_list=['Peter', 'Loki', 'Silvie', 'Emma', 'Bob', 'Josh', 'Stewe', 'Adam']
        users=[CustomUser.objects.get_or_create(username='{}'.format(user_item), email='{}@gmail.com'.format(user_item),
            password='{}'.format(user_item),user_image=random.choice(test_imgs),
            user_description="Random user description {}".format(random.randint(1, 10000))) for user_item in user_list]

        category_list=['Art', 'Dogs', 'Cats', 'Lamps', 'Houses', 'Lego', 'Toys', 'Cars', 'Birds', 'Plants']
        categories = [Category.objects.get_or_create(category_name='{}'.format(category_item)) for category_item in category_list]

        amount = options['amount'] if options['amount'] else 200
        for i in range(0, amount):
            post = Post.objects.create(
                title='Title {}'.format(random.randint(1, 50000)),
                description='Description {} {}'.format(random.randint(50000, 500000),random.randint(500, 5000)),
                category=random.choice(categories)[0],
                creator=random.choice(users)[0],
                rating=random.randint(-100, 100),
                post_image=random.choice(test_imgs),
            )
            post.save()

        posts=Post.objects.all()
        for _ in range(random.randint(400, 700)):
            comment = Comment.objects.create(
                comment_user = random.choice(users)[0],
                comment_post = random.choice(posts),
                comment_text = 'My comment {}'.format(random.randint(5, 5000000)),
            )
        self.stdout.write(self.style.SUCCESS('Successfully filled the database.'))