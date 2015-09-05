
BROKER_URL = 'redis://localhost:6379:0'

CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_IMPORTS = [
    'image_mediating.tasks',
    'camera_streaming.tasks',
]
