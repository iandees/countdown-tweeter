# -*- coding: utf-8 -*-
import unittest


def progress_bar(progress, width, alphabet=u'⣀⣄⣆⣇⣧⣷⣿'):
    per_char = 1.0 / width
    text = ''

    for i in range(width):
        if progress <= 0:
            text += alphabet[0]
        elif progress <= per_char:
            text += alphabet[int((progress / per_char) * len(alphabet))]
        else:
            text += alphabet[-1]

        progress -= per_char

    return text


class ProgressBarTests(unittest.TestCase):
    def test_progress_bar_empty(self):
        self.assertEqual(progress_bar(0.0, 3, 'eabcdf'), u'eee')

    def test_progress_bar_full(self):
        self.assertEqual(progress_bar(1.0, 3, 'eabcdf'), u'fff')

    def test_progress_bar_partial(self):
        self.assertEqual(progress_bar(0.2, 3, 'eabcdf'), u'cee')
        self.assertEqual(progress_bar(0.2, 3), u'⣧⣀⣀')


if __name__ == '__main__':
    unittest.main()
