def _convert(iter_obj):
    return [_[0] for _ in iter_obj]


if __name__ == "__main__":
    print(_convert([(5,), (8,)]))

