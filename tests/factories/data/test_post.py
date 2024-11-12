from app.factories.post import PostDataFactory


def test_post_data_factory_create_one(post_data_factory: PostDataFactory) -> None:
    post = post_data_factory.create_one()

    assert post.id
    assert post.title
    assert post.content
    assert post.author_id
    assert post.tags

    assert post.author is not None
    assert post.author.id == post.author_id
    assert post.author.username
    assert post.author.email

    # Check if post in post factory data
    assert str(post.id) in post_data_factory.data
    # Check if user in user factory data
    assert str(post.author_id) in post_data_factory.user_data_factory.data


def test_post_data_factory_create_one_with_override(
    post_data_factory: PostDataFactory,
) -> None:
    custom_data = {
        "title": "Custom Title",
        "content": "Custom Content",
        "tags": ["tag1", "tag2"],
    }

    post = post_data_factory.create_one(**custom_data)

    assert post.id
    assert post.title == custom_data["title"]
    assert post.content == custom_data["content"]
    assert post.author_id
    assert post.tags == custom_data["tags"]

    assert post.author is not None
    assert post.author.id == post.author_id
    assert post.author.username
    assert post.author.email

    # Check if post in post factory data
    assert str(post.id) in post_data_factory.data
    # Check if user in user factory data
    assert str(post.author_id) in post_data_factory.user_data_factory.data


def test_post_data_factory_create_many(
    post_data_factory: PostDataFactory,
) -> None:
    count = 3

    posts = post_data_factory.create_many(count)

    assert len(posts) == count
    assert len(post_data_factory.data) == count
    assert len(post_data_factory.user_data_factory.data) == count
