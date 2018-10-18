from itertools import cycle
import emoji
import hexchat


__module_name__ = "emojifier"
__module_version__ = "0.1"
__module_description__ = "Translate the text with colons into emojis"


print("Loading emojifier")
EMOJI_VALUES = list(emoji.UNICODE_EMOJI.values())
EMOJI_VALUES.extend(list(emoji.UNICODE_EMOJI_ALIAS.values()))
EMOJI_VALUES = sorted(EMOJI_VALUES)
emoji_autocompletion = []
last_msg = []


def autocomplete(avoid_infinite_loop=False):
    msg = hexchat.get_info('inputbox')
    if msg is None:
        return hexchat.EAT_NONE

    global emoji_autocompletion, last_msg
    if emoji_autocompletion:
        suggestion = next(emoji_autocompletion)
        replaced = ':'.join(last_msg[:-1]) + suggestion
        hexchat.command("settext %s" % replaced)
        return hexchat.EAT_ALL
    last_msg = msg.split(':')
    if not last_msg[-1]:
        return
    emoji_search = ':' + last_msg[-1]
    emoji_autocompletion = []
    for v in EMOJI_VALUES:
        if v.startswith(emoji_search):
            emoji_autocompletion.append(v)
    if not avoid_infinite_loop:
        if len(emoji_autocompletion) > 1:
            print(emoji_autocompletion)
        if emoji_autocompletion:
            emoji_autocompletion = cycle(emoji_autocompletion)
        return autocomplete(True)


def send_message(word, word_eol, userdata):
    if (word[0] == "65289"):
        return autocomplete()
    global emoji_autocompletion, last_msg
    emoji_autocompletion = []
    last_msg = []
    if not(word[0] == "65293"):
        return hexchat.EAT_NONE
    msg = hexchat.get_info('inputbox')
    if msg is None:
        return hexchat.EAT_NONE

    replaced = emoji.emojize(msg, use_aliases=True)
    if replaced != msg:
        hexchat.command("settext %s" % replaced)


hexchat.hook_print('Key Press', send_message)
