from slacker import Slacker

class Messenger:

  def __init__(self, token, channel):
    self.slack = Slacker(token)
    self.channel = channel

  def post_message(self, msg):
    response = self.slack.chat.post_message(self.channel, msg, username='Keras Robot', icon_emoji=':keras:')
    return self.__gen_msg('post_message', response)

  def post_image(self, file_path):
    response = self.slack.files.upload(file_path, channels=[self.channel])
    return self.__gen_msg('post_image', response)

  def __gen_msg(self, method_name, response):
    if response.body['ok']:
      return '[Slacker] Success on %s' % method_name
    else:
      return '[Slacker] Failed to %s' % method_name

