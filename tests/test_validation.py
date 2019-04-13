import pyhf
import pyhf.writexml, pyhf.readxml
import json
import pytest
import os


@pytest.fixture(scope='module')
def source_1bin_example1():
    with open('validation/data/1bin_example1.json') as read_json:
        return json.load(read_json)


@pytest.fixture(scope='module')
def spec_1bin_shapesys(source=source_1bin_example1()):
    spec = {
        'channels': [
            {
                'name': 'singlechannel',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'background',
                        'data': source['bindata']['bkg'],
                        'modifiers': [
                            {
                                'name': 'uncorr_bkguncrt',
                                'type': 'shapesys',
                                'data': source['bindata']['bkgerr'],
                            }
                        ],
                    },
                ],
            }
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_1bin_shapesys(mu=1.0):
    if mu == 1:
        expected_result = {
            "exp": [
                0.06371799398864626,
                0.15096503398048894,
                0.3279606950533305,
                0.6046087303039118,
                0.8662627605298466,
            ],
            "obs": 0.4541865416107029,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_1bin_shapesys(
    source=source_1bin_example1(),
    spec=spec_1bin_shapesys(source_1bin_example1()),
    mu=1,
    expected_result=expected_result_1bin_shapesys(1.0),
    config={'init_pars': 2, 'par_bounds': 2},
):
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def spec_1bin_lumi(source=source_1bin_example1()):
    spec = {
        "channels": [
            {
                "name": "channel1",
                "samples": [
                    {
                        "data": [20.0, 10.0],
                        "modifiers": [
                            {"data": None, "name": "mu", "type": "normfactor"}
                        ],
                        "name": "signal",
                    },
                    {
                        "data": [100.0, 0.0],
                        "modifiers": [{"data": None, "name": "lumi", "type": "lumi"}],
                        "name": "background1",
                    },
                    {
                        "data": [0.0, 100.0],
                        "modifiers": [{"data": None, "name": "lumi", "type": "lumi"}],
                        "name": "background2",
                    },
                ],
            }
        ],
        "parameters": [
            {
                "auxdata": [1.0],
                "bounds": [[0.0, 10.0]],
                "inits": [1.0],
                "name": "lumi",
                "sigmas": [0.1],
            }
        ],
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_1bin_lumi(mu=1.0):
    if mu == 1:
        expected_result = {
            "exp": [0.00905976, 0.0357287, 0.12548957, 0.35338293, 0.69589171],
            "obs": 0.00941757,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_1bin_lumi(
    source=source_1bin_example1(),
    spec=spec_1bin_lumi(source_1bin_example1()),
    mu=1,
    expected_result=expected_result_1bin_lumi(1.0),
    config={'init_pars': 2, 'par_bounds': 2},
):
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def source_1bin_normsys():
    source = {
        'binning': [2, -0.5, 1.5],
        'bindata': {'data': [120.0, 180.0], 'bkg': [100.0, 150.0], 'sig': [30.0, 95.0]},
    }
    return source


@pytest.fixture(scope='module')
def spec_1bin_normsys(source=source_1bin_normsys()):
    spec = {
        'channels': [
            {
                'name': 'singlechannel',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'background',
                        'data': source['bindata']['bkg'],
                        'modifiers': [
                            {
                                'name': 'bkg_norm',
                                'type': 'normsys',
                                'data': {'lo': 0.90, 'hi': 1.10},
                            }
                        ],
                    },
                ],
            }
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_1bin_normsys(mu=1.0):
    if mu == 1:
        expected_result = {
            "exp": [
                7.471684419037565e-10,
                5.7411551509088054e-08,
                3.6898088058290313e-06,
                0.000169657315363677,
                0.004392708998183163,
            ],
            "obs": 0.0006735317023683173,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_1bin_normsys(
    source=source_1bin_normsys(),
    spec=spec_1bin_normsys(source_1bin_normsys()),
    mu=1,
    expected_result=expected_result_1bin_normsys(1.0),
    config={'init_pars': 2, 'par_bounds': 2},
):
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def source_2bin_histosys_example2():
    with open('validation/data/2bin_histosys_example2.json') as read_json:
        return json.load(read_json)


@pytest.fixture(scope='module')
def spec_2bin_histosys(source=source_2bin_histosys_example2()):
    spec = {
        'channels': [
            {
                'name': 'singlechannel',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'background',
                        'data': source['bindata']['bkg'],
                        'modifiers': [
                            {
                                'name': 'bkg_norm',
                                'type': 'histosys',
                                'data': {
                                    'lo_data': source['bindata']['bkgsys_dn'],
                                    'hi_data': source['bindata']['bkgsys_up'],
                                },
                            }
                        ],
                    },
                ],
            }
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_2bin_histosys(mu=1):
    if mu == 1:
        expected_result = {
            "exp": [
                7.134513306138892e-06,
                0.00012547100627138575,
                0.001880010666437615,
                0.02078964907605385,
                0.13692494523572218,
            ],
            "obs": 0.1001463460725534,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_2bin_histosys(
    source=source_2bin_histosys_example2(),
    spec=spec_2bin_histosys(source_2bin_histosys_example2()),
    mu=1,
    expected_result=expected_result_2bin_histosys(1.0),
    config={'init_pars': 2, 'par_bounds': 2},
):
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def source_2bin_2channel_example1():
    with open('validation/data/2bin_2channel_example1.json') as read_json:
        return json.load(read_json)


@pytest.fixture(scope='module')
def spec_2bin_2channel(source=source_2bin_2channel_example1()):
    spec = {
        'channels': [
            {
                'name': 'signal',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['channels']['signal']['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'background',
                        'data': source['channels']['signal']['bindata']['bkg'],
                        'modifiers': [
                            {
                                'name': 'uncorr_bkguncrt_signal',
                                'type': 'shapesys',
                                'data': source['channels']['signal']['bindata'][
                                    'bkgerr'
                                ],
                            }
                        ],
                    },
                ],
            },
            {
                'name': 'control',
                'samples': [
                    {
                        'name': 'background',
                        'data': source['channels']['control']['bindata']['bkg'],
                        'modifiers': [
                            {
                                'name': 'uncorr_bkguncrt_control',
                                'type': 'shapesys',
                                'data': source['channels']['control']['bindata'][
                                    'bkgerr'
                                ],
                            }
                        ],
                    }
                ],
            },
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_2bin_2channel(mu=1.0):
    if mu == 1:
        expected_result = {
            "exp": [
                0.00043491354821983556,
                0.0034223000502860606,
                0.02337423265831151,
                0.1218654225510158,
                0.40382074249477845,
            ],
            "obs": 0.056332621064982304,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_2bin_2channel(
    source=source_2bin_2channel_example1(),
    spec=spec_2bin_2channel(source_2bin_2channel_example1()),
    mu=1,
    expected_result=expected_result_2bin_2channel(1.0),
    config={'init_pars': 5, 'par_bounds': 5},
):
    # 1 mu + 2 gammas for 2 channels each
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def source_2bin_2channel_couplednorm():
    with open('validation/data/2bin_2channel_couplednorm.json') as read_json:
        return json.load(read_json)


@pytest.fixture(scope='module')
def spec_2bin_2channel_couplednorm(source=source_2bin_2channel_couplednorm()):
    spec = {
        'channels': [
            {
                'name': 'signal',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['channels']['signal']['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'bkg1',
                        'data': source['channels']['signal']['bindata']['bkg1'],
                        'modifiers': [
                            {
                                'name': 'coupled_normsys',
                                'type': 'normsys',
                                'data': {'lo': 0.9, 'hi': 1.1},
                            }
                        ],
                    },
                    {
                        'name': 'bkg2',
                        'data': source['channels']['signal']['bindata']['bkg2'],
                        'modifiers': [
                            {
                                'name': 'coupled_normsys',
                                'type': 'normsys',
                                'data': {'lo': 0.5, 'hi': 1.5},
                            }
                        ],
                    },
                ],
            },
            {
                'name': 'control',
                'samples': [
                    {
                        'name': 'background',
                        'data': source['channels']['control']['bindata']['bkg1'],
                        'modifiers': [
                            {
                                'name': 'coupled_normsys',
                                'type': 'normsys',
                                'data': {'lo': 0.9, 'hi': 1.1},
                            }
                        ],
                    }
                ],
            },
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_2bin_2channel_couplednorm(mu=1.0):
    if mu == 1:
        expected_result = {
            "exp": [
                0.055223914655538435,
                0.13613239925395315,
                0.3068720101493323,
                0.5839470093910164,
                0.8554725461337025,
            ],
            "obs": 0.5906228034705155,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_2bin_2channel_couplednorm(
    source=source_2bin_2channel_couplednorm(),
    spec=spec_2bin_2channel_couplednorm(source_2bin_2channel_couplednorm()),
    mu=1,
    expected_result=expected_result_2bin_2channel_couplednorm(1.0),
    config={'init_pars': 2, 'par_bounds': 2},
):
    # 1 mu + 1 alpha
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def source_2bin_2channel_coupledhisto():
    with open('validation/data/2bin_2channel_coupledhisto.json') as read_json:
        return json.load(read_json)


@pytest.fixture(scope='module')
def spec_2bin_2channel_coupledhistosys(source=source_2bin_2channel_coupledhisto()):
    spec = {
        'channels': [
            {
                'name': 'signal',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['channels']['signal']['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'bkg1',
                        'data': source['channels']['signal']['bindata']['bkg1'],
                        'modifiers': [
                            {
                                'name': 'coupled_histosys',
                                'type': 'histosys',
                                'data': {
                                    'lo_data': source['channels']['signal']['bindata'][
                                        'bkg1_dn'
                                    ],
                                    'hi_data': source['channels']['signal']['bindata'][
                                        'bkg1_up'
                                    ],
                                },
                            }
                        ],
                    },
                    {
                        'name': 'bkg2',
                        'data': source['channels']['signal']['bindata']['bkg2'],
                        'modifiers': [
                            {
                                'name': 'coupled_histosys',
                                'type': 'histosys',
                                'data': {
                                    'lo_data': source['channels']['signal']['bindata'][
                                        'bkg2_dn'
                                    ],
                                    'hi_data': source['channels']['signal']['bindata'][
                                        'bkg2_up'
                                    ],
                                },
                            }
                        ],
                    },
                ],
            },
            {
                'name': 'control',
                'samples': [
                    {
                        'name': 'background',
                        'data': source['channels']['control']['bindata']['bkg1'],
                        'modifiers': [
                            {
                                'name': 'coupled_histosys',
                                'type': 'histosys',
                                'data': {
                                    'lo_data': source['channels']['control']['bindata'][
                                        'bkg1_dn'
                                    ],
                                    'hi_data': source['channels']['control']['bindata'][
                                        'bkg1_up'
                                    ],
                                },
                            }
                        ],
                    }
                ],
            },
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_2bin_2channel_coupledhistosys(mu=1.0):
    if mu == 1:
        expected_result = {
            "exp": [
                1.7653746536962154e-05,
                0.00026265644807799805,
                0.00334003612780065,
                0.031522353024659715,
                0.17907742915143962,
            ],
            "obs": 0.07967400132261188,
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_2bin_2channel_coupledhistosys(
    source=source_2bin_2channel_coupledhisto(),
    spec=spec_2bin_2channel_coupledhistosys(source_2bin_2channel_coupledhisto()),
    mu=1,
    expected_result=expected_result_2bin_2channel_coupledhistosys(1.0),
    config={'auxdata': 1, 'init_pars': 2, 'par_bounds': 2},
):
    # 1 mu 1 shared histosys
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


@pytest.fixture(scope='module')
def source_2bin_2channel_coupledshapefactor():
    with open('validation/data/2bin_2channel_coupledshapefactor.json') as read_json:
        return json.load(read_json)


@pytest.fixture(scope='module')
def spec_2bin_2channel_coupledshapefactor(
    source=source_2bin_2channel_coupledshapefactor()
):
    spec = {
        'channels': [
            {
                'name': 'signal',
                'samples': [
                    {
                        'name': 'signal',
                        'data': source['channels']['signal']['bindata']['sig'],
                        'modifiers': [
                            {'name': 'mu', 'type': 'normfactor', 'data': None}
                        ],
                    },
                    {
                        'name': 'bkg1',
                        'data': source['channels']['signal']['bindata']['bkg1'],
                        'modifiers': [
                            {
                                'name': 'coupled_shapefactor',
                                'type': 'shapefactor',
                                'data': None,
                            }
                        ],
                    },
                ],
            },
            {
                'name': 'control',
                'samples': [
                    {
                        'name': 'background',
                        'data': source['channels']['control']['bindata']['bkg1'],
                        'modifiers': [
                            {
                                'name': 'coupled_shapefactor',
                                'type': 'shapefactor',
                                'data': None,
                            }
                        ],
                    }
                ],
            },
        ]
    }
    return spec


@pytest.fixture(scope='module')
def expected_result_2bin_2channel_coupledshapefactor(mu=1.0):
    if mu == 1:
        expected_result = {
            'obs': 0.5421679124909312,
            'exp': [
                0.013753299929451691,
                0.048887400056355966,
                0.15555296253957684,
                0.4007561343326305,
                0.7357169630955912,
            ],
        }
    return expected_result


@pytest.fixture(scope='module')
def setup_2bin_2channel_coupledshapefactor(
    source=source_2bin_2channel_coupledshapefactor(),
    spec=spec_2bin_2channel_coupledshapefactor(
        source_2bin_2channel_coupledshapefactor()
    ),
    mu=1,
    expected_result=expected_result_2bin_2channel_coupledshapefactor(1.0),
    config={'auxdata': 0, 'init_pars': 3, 'par_bounds': 3},
):
    # 1 mu 2 shared shapefactors
    return {
        'source': source,
        'spec': spec,
        'mu': mu,
        'expected': {'result': expected_result, 'config': config},
    }


def validate_hypotest(pdf, data, mu_test, expected_result, tolerance=1e-6):
    init_pars = pdf.config.suggested_init()
    par_bounds = pdf.config.suggested_bounds()

    CLs_obs, CLs_exp_set = pyhf.utils.hypotest(
        mu_test, data, pdf, init_pars, par_bounds, return_expected_set=True
    )

    assert abs(CLs_obs - expected_result['obs']) / expected_result['obs'] < tolerance
    for result, expected_result in zip(CLs_exp_set, expected_result['exp']):
        assert abs(result - expected_result) / expected_result < tolerance


@pytest.mark.parametrize(
    'setup_and_tolerance',
    [
        (setup_1bin_shapesys(), 1e-6),
        (setup_1bin_lumi(), 1e-6),
        (setup_1bin_normsys(), 1e-6),
        (setup_2bin_histosys(), 8e-5),
        (setup_2bin_2channel(), 1e-6),
        (setup_2bin_2channel_couplednorm(), 1e-6),
        (setup_2bin_2channel_coupledhistosys(), 1e-6),
        (setup_2bin_2channel_coupledshapefactor(), 2.5e-6),
    ],
    ids=[
        '1bin_shapesys_mu1',
        '1bin_lumi_mu1',
        '1bin_normsys_mu1',
        '2bin_histosys_mu1',
        '2bin_2channel_mu1',
        '2bin_2channel_couplednorm_mu1',
        '2bin_2channel_coupledhistosys_mu1',
        '2bin_2channel_coupledshapefactor_mu1',
    ],
)
def test_validation(setup_and_tolerance):
    setup, tolerance = setup_and_tolerance
    source = setup['source']

    pdf = pyhf.Model(setup['spec'])

    if 'channels' in source:
        data = []
        for c in pdf.config.channels:
            data += source['channels'][c]['bindata']['data']
        data = data + pdf.config.auxdata
    else:
        data = source['bindata']['data'] + pdf.config.auxdata

    if 'auxdata' in setup['expected']['config']:
        assert len(pdf.config.auxdata) == setup['expected']['config']['auxdata']
    assert len(pdf.config.suggested_init()) == setup['expected']['config']['init_pars']
    assert (
        len(pdf.config.suggested_bounds()) == setup['expected']['config']['par_bounds']
    )

    validate_hypotest(
        pdf, data, setup['mu'], setup['expected']['result'], tolerance=tolerance
    )


@pytest.mark.parametrize(
    'toplvl, basedir',
    [
        (
            'validation/xmlimport_input/config/example.xml',
            'validation/xmlimport_input/',
        ),
        (
            'validation/xmlimport_input2/config/example.xml',
            'validation/xmlimport_input2',
        ),
        (
            'validation/xmlimport_input3/config/examples/example_ShapeSys.xml',
            'validation/xmlimport_input3',
        ),
    ],
    ids=['example-one', 'example-two', 'example-three'],
)
def test_import_roundtrip(tmpdir, toplvl, basedir):
    parsed_xml_before = pyhf.readxml.parse(toplvl, basedir)
    spec = {
        'channels': parsed_xml_before['channels'],
        'parameters': parsed_xml_before['measurements'][0]['config']['parameters'],
    }
    pdf_before = pyhf.Model(spec, poiname='SigXsecOverSM')

    tmpconfig = tmpdir.mkdir('config')
    tmpdata = tmpdir.mkdir('data')
    tmpxml = tmpdir.join('FitConfig.xml')
    tmpxml.write(
        pyhf.writexml.writexml(
            parsed_xml_before,
            tmpconfig.strpath,
            tmpdata.strpath,
            os.path.join(tmpdir.strpath, 'FitConfig'),
        ).decode('utf-8')
    )
    parsed_xml_after = pyhf.readxml.parse(tmpxml.strpath, tmpdir.strpath)
    spec = {
        'channels': parsed_xml_after['channels'],
        'parameters': parsed_xml_after['measurements'][0]['config']['parameters'],
    }
    pdf_after = pyhf.Model(spec, poiname='SigXsecOverSM')

    data_before = [
        binvalue
        for k in pdf_before.spec['channels']
        for binvalue in parsed_xml_before['data'][k['name']]
    ] + pdf_before.config.auxdata

    data_after = [
        binvalue
        for k in pdf_after.spec['channels']
        for binvalue in parsed_xml_after['data'][k['name']]
    ] + pdf_after.config.auxdata

    assert data_before == data_after

    init_pars_before = pdf_before.config.suggested_init()
    init_pars_after = pdf_after.config.suggested_init()
    assert init_pars_before == init_pars_after

    par_bounds_before = pdf_before.config.suggested_bounds()
    par_bounds_after = pdf_after.config.suggested_bounds()
    assert par_bounds_before == par_bounds_after

    CLs_obs_before, CLs_exp_set_before = pyhf.utils.hypotest(
        1,
        data_before,
        pdf_before,
        init_pars_before,
        par_bounds_before,
        return_expected_set=True,
    )
    CLs_obs_after, CLs_exp_set_after = pyhf.utils.hypotest(
        1,
        data_after,
        pdf_after,
        init_pars_after,
        par_bounds_after,
        return_expected_set=True,
    )

    tolerance = 1e-6
    assert abs(CLs_obs_after - CLs_obs_before) / CLs_obs_before < tolerance
    for result, expected_result in zip(CLs_exp_set_after, CLs_exp_set_before):
        assert abs(result - expected_result) / expected_result < tolerance
