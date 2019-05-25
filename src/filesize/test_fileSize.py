from unittest import TestCase

from src.filesize.filesize import FileSize


class TestFileSize(TestCase):
    def test_from_string(self):
        from_bytes = FileSize.from_string('1024')
        self.assertEqual(from_bytes.get_in_unit(''), 1024)

        from_kilobytes = FileSize.from_string('1024 kb', ' ')
        self.assertEqual(from_kilobytes.get_in_unit(''), 1048576)

        from_kilobytes = FileSize.from_string('1024kb')
        self.assertEqual(from_kilobytes.get_in_unit(''), 1048576)

        from_kilobytes_fraction = FileSize.from_string('1.5kb')
        self.assertEqual(from_kilobytes_fraction.get_in_unit(''), 1536)

    def test_from_int(self):
        from_bytes = FileSize.from_int(1024)
        self.assertEqual(1024, from_bytes.get_in_unit(''))
        self.assertEqual(1, from_bytes.get_in_unit('kb'))

        from_kilobytes = FileSize.from_int(1024, 'kb')
        self.assertEqual(1048576, from_kilobytes.get_in_unit(''))
        self.assertEqual(1024, from_kilobytes.get_in_unit('kb'))
        self.assertEqual(1, from_kilobytes.get_in_unit('mb'))

    def test_get_display_name(self):
        half_kb = FileSize.from_int(512)
        self.assertEqual('512B', half_kb.get_display_name())

        one_and_half_kb = FileSize.from_int(1536)
        self.assertEqual('1.5KB', one_and_half_kb.get_display_name())

        one_kb = FileSize.from_int(1024)
        self.assertEqual('1KB', one_kb.get_display_name())

        two_mb = FileSize.from_int(2, 'mb')
        self.assertEqual('2MB', two_mb.get_display_name())

        five_gb = FileSize.from_string('5GB')
        self.assertEqual('5GB', five_gb.get_display_name())

