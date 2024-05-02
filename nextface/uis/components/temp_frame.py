from typing import Optional
import gradio

import nextface.globals
import nextface.choices
from nextface import wording
from nextface.typing import TempFrameFormat
from nextface.filesystem import is_video
from nextface.uis.core import get_ui_component

TEMP_FRAME_FORMAT_DROPDOWN : Optional[gradio.Dropdown] = None


def render() -> None:
	global TEMP_FRAME_FORMAT_DROPDOWN

	TEMP_FRAME_FORMAT_DROPDOWN = gradio.Dropdown(
		label = wording.get('uis.temp_frame_format_dropdown'),
		choices = nextface.choices.temp_frame_formats,
		value = nextface.globals.temp_frame_format,
		visible = is_video(nextface.globals.target_path)
	)


def listen() -> None:
	TEMP_FRAME_FORMAT_DROPDOWN.change(update_temp_frame_format, inputs = TEMP_FRAME_FORMAT_DROPDOWN)
	target_video = get_ui_component('target_video')
	if target_video:
		for method in [ 'upload', 'change', 'clear' ]:
			getattr(target_video, method)(remote_update, outputs = TEMP_FRAME_FORMAT_DROPDOWN)


def remote_update() -> gradio.Dropdown:
	if is_video(nextface.globals.target_path):
		return gradio.Dropdown(visible = True)
	return gradio.Dropdown(visible = False)


def update_temp_frame_format(temp_frame_format : TempFrameFormat) -> None:
	nextface.globals.temp_frame_format = temp_frame_format

