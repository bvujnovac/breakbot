SLACK_API_TOKEN = '...'
PLUGINS = [
    'machine.plugins.builtin.general.PingPongPlugin',
    'machine.plugins.builtin.debug.EventLoggerPlugin',
    'plugins.channeltopic.TopicSetPlugin',
    'plugins.channeltopic.TopicReadPlugin'
]
STORAGE_BACKEND = 'machine.storage.backends.memory.MemoryStorage'
ALIASES='!,@'
DISABLE_HTTP = True
#ALIASES='!,%'
#KEEP_ALIVE = 5
#LOGLEVEL = 'DEBUG'
