import unittest

class TestCase(unittest.TestCase):
    def test_1(self):
        from Project7.project import generate_LMAOcode_from_LOLcode, generate_ROFLcode_from_LOLcode
        from Project7.interpreter import interpret
        SEED = 0
        STANDARD_INPUT = "aabb \n\t .,'! fasdf"
        def strip_leading_whitespace(text):
            lines = [line.lstrip() for line in text.splitlines()]
            return '\n'.join(lines)
        def expect_exception(lolcode_str):
            print(f"LOLcode str:\n{lolcode_str}")
            with self.assertRaises(Exception) as e:
                generate_LMAOcode_from_LOLcode(lolcode_str)
            with self.assertRaises(Exception) as e:
                generate_ROFLcode_from_LOLcode(lolcode_str)
            print("Correctly raised exception")
        def check_output(lolcode_str, expected_output):
            print(f"LOLcode str:\n{lolcode_str}")
            lmaocode = generate_LMAOcode_from_LOLcode(lolcode_str)
            print("Generated LMAOcode:")
            print(lmaocode)
            executed_lmao_output = interpret(lmaocode, 'LMAOcode', seed=SEED, standard_input=STANDARD_INPUT)
            
            self.assertEqual(expected_output, executed_lmao_output)
            roflcode = generate_ROFLcode_from_LOLcode(lolcode_str)
            print("Generated ROFLcode:")
            print(roflcode)
            executed_rofl_output = interpret(roflcode, 'ROFLcode', seed=SEED, standard_input=STANDARD_INPUT)
            
            self.assertEqual(expected_output, executed_rofl_output)
        
          

        print("test1")
        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I factorial YR arg ITZ A NUMBR MKAY
        	O RLY? SAEM arg AN 1
        	YA RLY
        		FOUND YR 1
        	NO WAI
        		FOUND YR PRODUKT OF arg AN I IZ factorial YR DIFF OF arg AN 1 MKAY
        	OIC
        IF U SAY SO ITZ A NUMBR
        VISIBLE I IZ factorial YR 1 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n1\n97\n')
        print("test2")
        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I factorial YR arg ITZ A NUMBR MKAY
        	O RLY? SAEM arg AN 1
        	YA RLY
        		FOUND YR 1
        	NO WAI
        		FOUND YR PRODUKT OF arg AN I IZ factorial YR DIFF OF arg AN 1 MKAY
        	OIC
        IF U SAY SO ITZ A NUMBR
        VISIBLE I IZ factorial YR 3 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n6\n97\n')
        print("test3")
        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I factorial YR arg ITZ A NUMBR MKAY
        	O RLY? SAEM arg AN 1
        	YA RLY
        		FOUND YR 1
        	NO WAI
        		FOUND YR PRODUKT OF arg AN I IZ factorial YR DIFF OF arg AN 1 MKAY
        	OIC
        IF U SAY SO ITZ A NUMBR
        VISIBLE I IZ factorial YR 10 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n3628800\n97\n')


if __name__ == '__main__':
    unittest.main()