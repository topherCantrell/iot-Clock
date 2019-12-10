from disp_base import DisplayBase


class WordDisplay(DisplayBase):

    WORD_COORDS = {
        'IT': (0, 0), 'IS': (3, 0), 'HALF': (7, 0), 'TEN': (12, 0),
        'A QUARTER': (0, 1), 'TWENTY': (9, 1),
        'FIVE': (0, 2), 'MINUTES': (5, 2), 'TO': (13, 2),
        'PAST': (0, 3), 'TWO': (5, 3), 'THREE': (10, 3),
        'ONE': (0, 4), 'FOUR': (5, 4), 'FIVE_': (11, 4),
        'SIX': (0, 5), 'SEVEN': (4, 5), 'EIGHT': (10, 5),
        'NINE': (0, 6), 'TEN_': (5, 6), 'ELEVEN': (9, 6),
        'TWELVE': (0, 7), "O'CLOCK": (8, 7)
    }

    MINUTE_OFFSET = ['', 'FIVE', 'TEN', 'A QUARTER', 'TWENTY', 'TWENTY FIVE', 'HALF']
    HOURS = ['TWELVE', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE_', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN_', 'ELEVEN']

    def __init__(self, window):
        self._window = window

    def get_window_size(self):
        return (15 * 8, 8 * 8)

    def make_time(self, xofs, yofs, hours, minutes, _seconds, _config):

        if hours >= 12:
            hours = hours - 12

        hr = HOURS[hours]

        # IT IS FIVE/TEN/A_QUARTER/TWENTY/TWENTY_FIVE/HALF PAST hour O'CLOCK
        # IT IS FIVE/TEN/A_QUARTER/TWENTY/TWENTY_FIVE TO hour O'CLOCK

        # Round minutes to nearest 5
        minutes = int(minutes / 5) * 5
        min = MINUTE_OFFSET[minutes]

        if minutes <= 30:
            phrase = 'IT IS {min} PAST {hour} O\'CLOCK'
        else:
            phrase = 'IT IS {min} TO {hour} O\'CLOCK'

        phrase = phrase.split(' ')

        for word in WordDisplay.WORD_COORDS:
            coords = WORD_COORDS[word]
            display_text = word.replace('_', '')
            if word in phrase:
                color = 15
            else:
                color = 4
            self._window.draw_text(coords[0] * 8, coords[1] * 8, display_text, color)
