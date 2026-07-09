import os
from pathlib import Path

from flask import Flask

app = Flask(__name__)

DEFAULT_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
}


def load_config(config_path=None):
    config_file = Path(config_path or os.environ.get('APP_CONFIG', Path(__file__).with_name('app.properties')))
    config = dict(DEFAULT_CONFIG)

    if config_file.exists():
        for raw_line in config_file.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = [part.strip() for part in line.split('=', 1)]
            config[key.lower()] = value

    config['host'] = os.environ.get('HOST', config.get('host', DEFAULT_CONFIG['host']))
    config['port'] = os.environ.get('PORT', config.get('port', DEFAULT_CONFIG['port']))
    config['port'] = int(config['port'])
    return config


@app.route('/')
def hello_world():
    return 'sundari'


if __name__ == '__main__':
    config = load_config()
    app.run(host=config['host'], port=config['port'], debug=False)
