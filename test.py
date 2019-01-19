#!/usr/bin/env python3
import unittest
import random
from threading import Thread

import short_id


class FuncsTest(unittest.TestCase):
    def test_encode(self):
        normal_id = 9876543210
        sid = short_id.encode(normal_id)
        self.assertEqual(sid, 'aMoY42')

    def test_decode(self):
        sid = 'ZaU1OxBxw981lfe821e0'
        normal_id = short_id.decode(sid)
        self.assertEqual(normal_id, 695059889628005113016054548042632536)

    def test_convert(self):
        for i in range(5):
            normal_id = random.randrange(1, 1000000000000000)
            sid = short_id.encode(normal_id)
            decoded_id = short_id.decode(sid)
            self.assertEqual(normal_id, decoded_id)

    def test_length(self):
        length = 6
        for i in range(10000):
            num = random.randrange(1, 62 ** length)
            sid = short_id.encode(num)
            self.assertLessEqual(len(sid), length)


class ShortIDTest(unittest.TestCase):
    def setUp(self):
        self.default_id = short_id.id_generator
        self.hex_id = short_id.ShortID('0123456789abcdef')
        self.other_id = short_id.ShortID('0123456789abcdefghijklmnopqrstuv')

    def test_iter(self):
        count = 0
        for sid in self.default_id:
            if count < 10:
                result_true = self.default_id.is_valid(sid)
                self.assertTrue(result_true)
                count += 1
            else:
                break

    def test_next(self):
        for i in range(10):
            sid = next(self.default_id)
            result_true = self.default_id.is_valid(sid)
            self.assertTrue(result_true)

    def test_encode(self):
        num_x = self.default_id.encode(9876543210)
        self.assertEqual(num_x, 'aMoY42')

        num_16 = self.hex_id.encode(9876543210)
        self.assertEqual(int(num_16, 16), 9876543210)

        num_32 = self.other_id.encode(9876543210)
        self.assertEqual(int(num_32, 32), 9876543210)

    def test_decode(self):
        for i in range(5):
            normal_id = random.randrange(1, 1000000000000000)
            sid = self.default_id.encode(normal_id)
            decoded_id = self.default_id.decode(sid)
            self.assertEqual(normal_id, decoded_id)

    def test_is_valid(self):
        sid = ''.join(random.sample(self.default_id.characters, 10))
        result_true = self.default_id.is_valid(sid)
        self.assertTrue(result_true)

        result_false = self.default_id.is_valid('iwqew*&^!123|}682{":?>785')
        self.assertFalse(result_false)

    def test_length(self):
        length = 6
        for i in range(1000):
            num = random.randrange(1, 62 ** length)
            sid = self.default_id.encode(num)
            self.assertLessEqual(len(sid), length)

    def gen_id_set(self, generator, id_set, count):
        for i in range(count):
            sid = next(generator)
            id_set.add(sid)

    def test_collision(self):
        id_set = set()
        self.gen_id_set(self.default_id, id_set, 1000000)
        self.assertEqual(1000000 - len(id_set), 0)

    @unittest.skip('skip single_instance')
    def test_single_instance_conflict_by_multi_threads(self):
        s1, s2, s3 = set(), set(), set()
        id_generator = short_id.ShortID()
        threads = [
            Thread(target=self.gen_id_set, args=(id_generator, s1, 100000)),
            Thread(target=self.gen_id_set, args=(id_generator, s2, 100000)),
            Thread(target=self.gen_id_set, args=(id_generator, s3, 100000))
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(s1 & s2), 0)
        self.assertEqual(len(s2 & s3), 0)
        self.assertEqual(len(s3 & s1), 0)

    @unittest.skip('skip multi instance')
    def test_multi_instance_conflict_by_multi_threads(self):
        s1, s2, s3 = set(), set(), set()
        g1, g2, g3 = short_id.ShortID(), short_id.ShortID(), short_id.ShortID()
        threads = [
            Thread(target=self.gen_id_set, args=(g1, s1, 100000)),
            Thread(target=self.gen_id_set, args=(g2, s2, 100000)),
            Thread(target=self.gen_id_set, args=(g3, s3, 100000))
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(s1 & s2), 0)
        self.assertEqual(len(s2 & s3), 0)
        self.assertEqual(len(s3 & s1), 0)


if __name__ == "__main__":
    unittest.main()
