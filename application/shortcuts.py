import re
from typing import Union
from application.models import Person, Org

def cite(person: Union[str, int], org: Union[str, int]):
    assert type(person) in (str, int), 'person must be type str or int.'
    assert type(org) in (str, int), 'org must be type str or int.'

    if type(person) == int:
        person_instance = Person.query.filter_by(id=person).first()
        person_initials = f'{person_instance.firstName[0]}{person_instance.lastName[0]}'
        data_title = f"<a href='/library/person/{person}'>{person_instance.firstName} {person_instance.lastName}</a>"
    else:
        person_initials = ''.join(re.findall(r'[A-Z]', person))
        data_title = person

    if type(org) == int:
        org_instance = Org.query.filter_by(id=org).first()
        data_content_org = f"<a href='/library/org/{org}'>{org_instance.acronym}</a>"
    else:
        data_content_org = org

    html_str = f"""
    <sup>
        <a class="citation" href="#" data-toggle="popover" data-title="{data_title}"
        data-content="{data_content_org}">{person_initials}</a>
    </sup>"""

    return html_str

def presets(initials: str):

    tn_gasshuku = """
        <a href='/library/person/20'>Tatsuya Naka</a><br>
        <a href='https://www.facebook.com/video.php?v=727616257291532&fref=nf' target='_blank'>Germany Gasshuku 2014</a>"""

    presets = {
        'RA': cite(person=32, org=8),
        'ST': cite(person="Shinji Tanaka", org="<a href='/library/org/2'>SKIF</a> HQ"),
        'MM': cite(person=29, org=2),
        'TN_gasshuku': cite(tn_gasshuku, org=1).replace('TNGG', 'TN')
    }

    print(re.sub(r'[\s]{5,}', '    ', presets[initials]))


print("Use presets(initials) or cite(person: Union[int, str], org: Union[int, str]")
