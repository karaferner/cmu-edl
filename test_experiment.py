from experiment import Experiment

test_exp = Experiment('name', 0.5, 0.4, 10)

def test_get_iridium_loading():
    assert (test_exp.get_Ir_loading()==0.5)

def test_get_platinum_loading():
    assert (test_exp.get_Pt_loading()==0.4)

def test_get_active_area():
    assert (test_exp.get_active_area()==10)
