from drf_yasg import openapi
from users.doc import USER_NOT_AUTHORIZED_RESPONSE, AUTH_PARAMETER

CATEGORIES_EXAMPLE = [
    {'pk': 1, 'name': 'python'},
    {'pk': 2, 'name': 'js'}
]

POST_VIEW_RESPONSE = openapi.Response(description='ok',
                                      examples={'application/json': {
                                          'pk': 4,
                                          'name': 'post',
                                          'markdown': '# Post',
                                          'description': 'very nice post',
                                          'categories': CATEGORIES_EXAMPLE

                                      }})

post_create_doc = {
    'manual_parameters': [
        AUTH_PARAMETER,
        openapi.Parameter('name',
                          openapi.IN_FORM,
                          description='post name',
                          type=openapi.TYPE_STRING),
        openapi.Parameter('description',
                          openapi.IN_FORM,
                          description='post description',
                          type=openapi.TYPE_STRING),
        openapi.Parameter('markdown',
                          openapi.IN_FORM,
                          description='для создания фото:  ![]([image_name.jpg_0])',
                          type=openapi.TYPE_STRING),
        openapi.Parameter('categories',
                          openapi.IN_FORM,
                          description='категории',
                          type=openapi.TYPE_ARRAY,
                          items=openapi.Items(openapi.TYPE_NUMBER)),
        openapi.Parameter('images',
                          openapi.IN_FORM,
                          description='фотографии',
                          type=openapi.TYPE_ARRAY,
                          items=openapi.Items(openapi.TYPE_FILE)),
    ],
    'responses': {
        '201': POST_VIEW_RESPONSE,

        '400': openapi.Response('bad request',
                                examples={'application/json': {
                                    'name': ['обязательное поле'],
                                    'markdown': ['обязательное поле']
                                }}),

        '403': USER_NOT_AUTHORIZED_RESPONSE
    }
}

get_categories_doc = {
    'responses': {
        '200': openapi.Response('ok',
                                examples={'application/json': CATEGORIES_EXAMPLE})
    }
}
