from copy import deepcopy
from rrd_xml_parser.parsers.kpt import settings_pars_kpt
from rrd_xml_parser.parsers.zu import settings_pars_zu
from rrd_xml_parser.parsers.oks import settings_pars_oks
from rrd_xml_parser.parsers.extract import settings_pars_extract
from rrd_xml_parser.parsers.mp import settings_pars_mp
from rrd_xml_parser.parsers.bozo import settings_pars_bozo
from rrd_xml_parser.parsers.sp import settings_pars_sp
from rrd_xml_parser.exceptions import NotImplementedTypeError, NotImplementedValueError

setting_pars = dict()

setting_pars.update(deepcopy(settings_pars_kpt))
setting_pars.update(deepcopy(settings_pars_zu))
setting_pars.update(deepcopy(settings_pars_oks))
setting_pars.update(deepcopy(settings_pars_extract))
setting_pars.update(deepcopy(settings_pars_mp))
setting_pars.update(deepcopy(settings_pars_bozo))
setting_pars.update(deepcopy(settings_pars_sp))

__all__ = ['setting_pars', 'NotImplementedTypeError', 'NotImplementedValueError']
