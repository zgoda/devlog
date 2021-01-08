import factory
import markdown
from factory.base import Factory, FactoryOptions, OptionDefault

from devlog.models import Link, Post, Tag, TaggedPost, User, db
from devlog.utils.text import PostProcessor, slugify

factory.Faker._DEFAULT_LOCALE = 'pl_PL'
DEFAULT_PASSWORD = 'password'


class PeeweeOptions(FactoryOptions):

    def _build_default_options(self):
        return super()._build_default_options() + [
            OptionDefault('database', None, inherit=True),
        ]


class PeeweeModelFactory(Factory):

    _options_class = PeeweeOptions

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        return target_class.create(**kwargs)


class BaseFactory(PeeweeModelFactory):

    class Meta:
        database = db


class PostFactory(BaseFactory):

    class Meta:
        model = Post

    author = factory.Faker('user_name')
    title = factory.Faker('sentence')
    text = factory.Faker('text')

    @factory.lazy_attribute
    def c_year(self):
        return self.created.year

    @factory.lazy_attribute
    def c_month(self):
        return self.created.month

    @factory.lazy_attribute
    def c_day(self):
        return self.created.day

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)

    @factory.lazy_attribute
    def summary(self):
        return markdown.markdown(
            PostProcessor.summary_src(self.text), **PostProcessor.MD_KWARGS
        )

    @factory.lazy_attribute
    def text_html(self):
        return markdown.markdown(self.text, **PostProcessor.MD_KWARGS)


class TagFactory(BaseFactory):

    class Meta:
        model = Tag

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class TaggedPostFactory(BaseFactory):

    class Meta:
        model = TaggedPost


class LinkFactory(BaseFactory):

    class Meta:
        model = Link

    text = factory.Faker('text')

    @factory.lazy_attribute
    def text_html(self):
        return markdown.markdown(self.text, **PostProcessor.MD_KWARGS)


class UserFactory(BaseFactory):
    name = factory.Faker('user_name')
    password = DEFAULT_PASSWORD

    class Meta:
        model = User
