# test_cabwiz.py    -*- coding: utf-8 -*-


import app.cabwiz as CW
import app.cabinet as C


def test_get_parser():
    p = CW.get_parser()
    args = p.parse_args(['--fullwidth', '161'])
    assert args.fullwidth == 161.0


def test_parse_longopts_attached_values():
    p = CW.get_parser()
    args = p.parse_args(['--fullwidth=177.75', '--height=26.25',
                         '--depth=27.0', '--name=Long Opts Job'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Long Opts Job'


def test_parse_longopts_separate_values():
    p = CW.get_parser()
    args = p.parse_args(['--fullwidth', '177.75', '--height', '26.25',
                         '--depth', '27.0', '--name', 'Parse Long Opts Job'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Parse Long Opts Job'


def test_parse_shortopts_separate_values():
    p = CW.get_parser()
    args = p.parse_args(['-w', '177.75', '-ht', '26.25',
                         '-d', '27.0', '-n', 'Short Opts Job'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Short Opts Job'


def test_parse_shortopts_sep_values_desc():
    p = CW.get_parser()
    args = p.parse_args(['-w', '177.75', '-ht', '26.25',
                         '-d', '27.0', '-n', 'Short Opts Job',
                         '-s', 'A job to test parsing short options.'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Short Opts Job'
    assert args.desc == 'A job to test parsing short options.'


def test_parse_shortopts_sep_values_fillers_both():
    p = CW.get_parser()
    args = p.parse_args(['-w', '177.75', '-ht', '26.25',
                         '-d', '27.0', '-n', 'Short Opts Job',
                         '-s', 'A job to test parsing short options.',
                         '-f', 'both'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Short Opts Job'
    assert args.desc == 'A job to test parsing short options.'
    assert args.fillers == C.Ends.both


def test_parse_shortopts_sep_values_fillers_left():
    p = CW.get_parser()
    args = p.parse_args(['-w', '177.75', '-ht', '26.25',
                         '-d', '27.0', '-n', 'Short Opts Job',
                         '-s', 'A job to test parsing short options.',
                         '-f', 'left'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Short Opts Job'
    assert args.desc == 'A job to test parsing short options.'
    assert args.fillers == C.Ends.left


def test_parse_shortopts_sep_values_fillers_right():
    p = CW.get_parser()
    args = p.parse_args(['-w', '177.75', '-ht', '26.25',
                         '-d', '27.0', '-n', 'Short Opts Job',
                         '-s', 'A job to test parsing short options.',
                         '-f', 'right'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Short Opts Job'
    assert args.desc == 'A job to test parsing short options.'
    assert args.fillers == C.Ends.right


def test_parse_shortopts_sepvals_primmatl():
    p = CW.get_parser()
    args = p.parse_args(['-w', '177.75', '-ht', '26.25',
                         '-d', '27.0', '-n', 'Short Opts Job',
                         '-s', 'A job to test parsing short options.',
                         '-pm', 'Melamine', '-pt', '0.77'])
    assert args.fullwidth == 177.75
    assert args.height == 26.25
    assert args.depth == 27.0
    assert args.name == 'Short Opts Job'
    assert args.desc == 'A job to test parsing short options.'
    assert args.fillers == C.Ends.neither
    assert args.prim_matl == 'Melamine'
    assert args.prim_thick == 0.77


# test_cabwiz.py  ends here
