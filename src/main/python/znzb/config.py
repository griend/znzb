import configparser
import os
import pathlib

class Config:

    def __init__(self):
        self.base_dir = os.path.join(pathlib.Path.home(), 'var', 'zanzibar')
        self.db_dir = os.path.join(self.base_dir, 'db')
        self.etc_dir = os.path.join(self.base_dir, 'etc')
        self.log_dir = os.path.join(self.base_dir, 'log')
        self.tmp_dir = os.path.join(self.base_dir, 'tmp')

        #
        # ./zanzibar.ini
        # /opt/zanzibar/etc/zanzibar.ini
        # ~/var/zanzibar/etc/zanzibar.ini
        # ~/.zanzibar.ini
        #
        files = [
            os.path.join(os.path.dirname(__file__), 'zanzibar.ini'),
            os.path.join('opt', 'zanzibar', 'etc', 'zanzibar.ini'),
            os.path.join(self.etc_dir, 'zanzibar.ini'),
            os.path.join(pathlib.Path.home(), '.zanzibar.ini'),
        ]

        config = configparser.ConfigParser()
        config.read(filenames=files)
        # for name in config.read(filenames=files):
        #     print(f'Read: {name}')

        for section in config.sections():
            for key in config[section]:
                value = config[section][key]
                setattr(self, key, value)
                # print(f'Key: {key}: {value}')

        for d in [self.base_dir, self.db_dir, self.log_dir, self.tmp_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)


if __name__ == '__main__':
    config = Config()
    print(config.tmp_dir)

    if os.path.isdir(config.tmp_dir):
        print(f'Is a dir: {config.tmp_dir}')
    else:
        print(f'Is not a dir: {config.tmp_dir}')
