# -*- coding: utf-8 -*-


__all__ = ['format_messages']


def format_messages(messages):
    if isinstance(messages, str):
        return messages
    if isinstance(messages, dict):
        return ','.join(
            f'{field}:{message}'
            for field, message in messages.items()
        )
    return str(messages)
