from disp_base import DisplayBase


class WordDisplay(DisplayBase):

    WORD_COORDS = {
        'IT': (0, 0), 'IS': (3, 0), 'HALF': (7, 0), 'TEN': (13, 0),
        'A_QUARTER': (0, 1), 'TWENTY': (10, 1),
        'FIVE': (0, 2), 'MINUTES': (5, 2), 'TO': (14, 2),
        'PAST': (0, 3), 'TWO': (6, 3), 'THREE': (11, 3),
        'ONE': (0, 4), 'FOUR': (6, 4), 'FIVE_': (12, 4),
        'SIX': (0, 5), 'SEVEN': (5, 5), 'EIGHT': (11, 5),
        'NINE': (0, 6), 'TEN_': (6, 6), 'ELEVEN': (10, 6),
        'TWELVE': (0, 7), "O'CLOCK": (9, 7)
    }

    MINUTE_OFFSET = ['', 'FIVE MINUTES', 'TEN MINUTES', 'A_QUARTER', 'TWENTY MINUTES', 'TWENTY FIVE MINUTES', 'HALF',
                     'TWENTY FIVE MINUTES', 'TWENTY MINUTES', 'A_QUARTER', 'TEN MINUTES', 'FIVE MINUTES']
    HOURS = ['TWELVE', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE_', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN_', 'ELEVEN', 'TWELVE']

    def __init__(self, window):
        self._window = window

    def get_window_size(self):
        # This is how big the display is
        return (16 * 8, 8 * 8)

    def make_time(self, xofs, yofs, hours, minutes, _seconds, config):

        # Print one of these phrases:

        # IT IS hour O'CLOCK
        # IT IS FIVE/TEN/A_QUARTER/TWENTY/TWENTY_FIVE/HALF PAST hour O'CLOCK
        # IT IS FIVE/TEN/A_QUARTER/TWENTY/TWENTY_FIVE TO next_hour O'CLOCK

        # Round minutes to nearest 5
        minutes = 5 * round(minutes / 5)
        if minutes > 55:  # Round up to the next hour
            minutes = 0
            hours = hours + 1

        # No words for AM/PM. Limit hour to 0-11.
        if hours >= 12:
            hours = hours - 12

        # Word for the hours
        hr = WordDisplay.HOURS[hours]  # Word for this hour
        hr_next = WordDisplay.HOURS[hours + 1]  # Word for next hour

        # Word(s) for the minutes
        mins = WordDisplay.MINUTE_OFFSET[int(minutes / 5)]

        # Pick the correct phrase based on the minutes. Either on the hour, past the hour,
        # or to the next hour.
        if minutes == 0:
            phrase = f'IT IS {hr} O\'CLOCK'
        elif minutes <= 30:
            phrase = f'IT IS {mins} PAST {hr} O\'CLOCK'
        else:
            phrase = f'IT IS {mins} TO {hr+1} O\'CLOCK'

        # List of words to light up
        phrase = phrase.split(' ')

        for word in WordDisplay.WORD_COORDS:
            # Get the coordinates for the word
            coords = WordDisplay.WORD_COORDS[word]
            # Underscores become printed spaces
            display_text = word.replace('_', ' ')
            if word in phrase:
                # This word is part of the phrase ... print it bright
                color = config['brightness']
            else:
                # This word is NOT part of the phrase ... print it dim
                color = 1
            self._window.draw_text(xofs + coords[0] * 8, yofs + coords[1] * 8, display_text, color)
