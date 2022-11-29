import moviepy.editor as mp
from commons.enums.attributes import Position, TextClipMethod
from src.services.graphics_extensions.moviepy.ClipComponents.BaseComponentClip import BaseComponentClip


class ScrollingTextClip(BaseComponentClip):
    def __init__(self, template, text, start_time, split_text=True) -> None:
        self.__template = template
        self.__text = ''
        if split_text:
            words = text.split(' ')
            counter = 0
            char_limit = int(self.__template.aspect_ratio[0]/30)
            for word in words:
                if counter + len(word) > char_limit:
                    self.__text += '\n' + word + ' '
                    counter = len(word) + 1
                else:
                    counter += len(word) + 1
                    self.__text += word + ' '
        else:
            self.__text = text

        self.__start_time = start_time
        self.__set_scrolling_text_clip()
        self.clip = self.clip.set_start(start_time, change_end=True)

    def __set_scrolling_text_clip(self):
        h = self.__template.aspect_ratio[1]
        speed = 200
        margin = 10
        text_clip = mp.TextClip(self.__text,
                                font=self.__template.font_family,
                                color=self.__template.font_color,
                                fontsize=self.__template.font_size,
                                interline=margin*2,
                                method=TextClipMethod.LABEL.value,)
        duration = (text_clip.size[1] + h + margin*2)/speed
        text_clip = text_clip.set_duration(duration)
        text_clip = text_clip.set_position(
            lambda t: (Position.CENTER.value, h + margin - t*speed))

        self.clip, self.duration = text_clip, duration
