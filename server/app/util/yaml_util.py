import yaml


def read_yaml(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    return data


if __name__ == '__main__':
    log = read_yaml("../../resource\\log_config.yml")
    print(log["weibo"]["name"])
    print(log["weibo"]["password"])
