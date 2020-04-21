from flask import current_app

"""
Creates abstraction of search engine so that other search engines could be used.
All one would have to do is reimplement these three functions.

Whoosh used as pythonanywhere cannot accomodate Elasticsearch with virtualization.

current_app.whoosh_search boolean so that application could continue to run even
if search engine isn't configured."""

# def add_to_index(index, model):
#     if not current_app.search:
#         return
#     payload = {}
#     for field in model.__searchable__:
#         payload[field] = getattr(model, field)
#     current_app.elasticsearch.index(index=index, id=model.id, body=payload)

# def remove_from_index(index, model):
#     if not current_app.search:
#         return
#     current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(model, query:str, page:int, per_page:int):
    if not current_app.search:
        return [], 0

    """whoosh_search(text, limit=int, field=Tuple[str], or_:bool=False);
    field arg specifies indexed field to use in model;
    or_ arg specifies if results contain all of (AND) or a (OR) query term"""
    ids = [row.id for row in model.query.whoosh_search(query).all()]
    start_idx = (page - 1) * per_page
    end_idx = page * per_page

    return ids[start_idx:end_idx], len(ids)

""" May have to reinitialize whoosh_search index:
>> whoosh.whoosh_index(app, Post)
>> posts = [i for i in Post.query.all()]
>> for post in Post.query.all(): db.session.delete(post)
>> for post in posts: db.session.add(body=post.body, user_id=5)
"""