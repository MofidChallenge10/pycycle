import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from pycycle import cycles
class Tests(unittest.TestCase):
 def test_no_cycle(self): self.assertEqual([],cycles({"a":{"b"},"b":set()}))
 def test_cycle(self): self.assertEqual([["a","b"]],cycles({"a":{"b"},"b":{"a"}}))
 def test_self_cycle(self): self.assertEqual([["a"]],cycles({"a":{"a"}}))
if __name__=="__main__": unittest.main()
