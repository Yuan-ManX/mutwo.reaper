import unittest

from mutwo import core_events
from mutwo import core_parameters
from mutwo import reaper_converters


class ReaperMarkerConverterTest(unittest.TestCase):
    def test_convert_simple_event(self):
        converter = reaper_converters.ReaperMarkerConverter()

        event = core_events.SimpleEvent(2)
        event.name = "testMarker"
        event.color = r"0 16797088 1 B {A4376701-5AA5-246B-900B-28ABC969123A}"

        absolute_entry_delay = core_parameters.DirectDuration(10)

        self.assertEqual(
            converter._convert_simple_event(event, absolute_entry_delay),
            (f"10.0 {event.name} {event.color}",),
        )

        # with different init arguments
        converter = reaper_converters.ReaperMarkerConverter(
            simple_event_to_marker_name=lambda simple_event: simple_event.marker_name,
            simple_event_to_marker_color=lambda simple_event: simple_event.marker_color,
        )

        event.marker_name = event.name
        event.marker_color = event.color

        self.assertEqual(
            converter._convert_simple_event(event, absolute_entry_delay),
            (f"10.0 {event.name} {event.color}",),
        )

    def test_convert(self):
        converter = reaper_converters.ReaperMarkerConverter()

        events = core_events.SequentialEvent(
            [core_events.SimpleEvent(2), core_events.SimpleEvent(3)]
        )

        events[0].name = "beginning"
        events[0].color = r"0 16797088 1 B {A4376701-5AA5-246B-900B-28ABC969123A}"
        events[1].name = "center"
        events[1].color = r"0 18849803 1 B {E4DD7D23-98F4-CA97-8587-F4259A9498F7}"

        self.assertEqual(
            converter.convert(events),
            f"MARKER 0 0.0 {events[0].name} {events[0].color}\nMARKER 1 2.0 {events[1].name} {events[1].color}",
        )


if __name__ == "__main__":
    unittest.main()
