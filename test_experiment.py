from experiment import Experiment

test_exp = Experiment('name', 0.5, 0.4, 10)

def test_get_iridium_loading():
    assert (test_exp.get_Ir_loading()==0.5)

