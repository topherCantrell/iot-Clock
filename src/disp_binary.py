from disp_base import DisplayBase


class BinaryDisplay(DisplayBase):

    BOX_SIZE = 8
    BOX_SPACE = 6

    def __init__(self, window):
        self._window = window

    def get_window_size(self):
        return (BinaryDisplay.BOX_SIZE * 4 + BinaryDisplay.BOX_SPACE * 5, BinaryDisplay.BOX_SIZE * 4 + BinaryDisplay.BOX_SPACE * 3)

    def _convert_to_binary(self, value):
        ret = bin(int(value))[2:]
        while(len(ret)) < 4:
            ret = '0' + ret
        return ret

    def make_time(self, xofs, yofs, hours, minutes, _seconds, config):
        hours_a = self._convert_to_binary(hours / 10)
        hours_b = self._convert_to_binary(hours % 10)
        mins_a = self._convert_to_binary(minutes / 10)
        mins_b = self._convert_to_binary(minutes % 10)

        col_values = [hours_a, hours_b, mins_a, mins_b]

        for cols in range(4):
            for rows in range(4):
                if cols == 0 and rows < 2:
                    continue
                if cols == 2 and rows == 0:
                    continue
                if cols > 1:
                    ofs = BinaryDisplay.BOX_SPACE * 2
                else:
                    ofs = 0

                if col_values[cols][rows] == '1':
                    self._window.DrawBox(xofs + cols * (BinaryDisplay.BOX_SIZE + BinaryDisplay.BOX_SPACE) + ofs, yofs + rows * (BinaryDisplay.BOX_SIZE + BinaryDisplay.BOX_SPACE), BinaryDisplay.BOX_SIZE, BinaryDisplay.BOX_SIZE, config['brightness'])
                else:
                    self._window.draw_rectangle(xofs + cols * (BinaryDisplay.BOX_SIZE + BinaryDisplay.BOX_SPACE) + ofs, yofs + rows * (BinaryDisplay.BOX_SIZE + BinaryDisplay.BOX_SPACE), BinaryDisplay.BOX_SIZE, BinaryDisplay.BOX_SIZE, config['brightness'])
