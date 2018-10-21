#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import *
import os
import json
from vd2svg import *


def extract_permissions(aosp_root_dir):
    permissions = {}
    manifest = os.path.join(aosp_root_dir, 'core/res/AndroidManifest.xml')
    xml = parse(manifest)
    permission_elements = xml.getElementsByTagName('permission')

    for p in permission_elements:
        name = p.attributes['android:name'].value.encode('utf-8').decode('utf-8')
        permissions[name] = {
            'name': name,
            'label': '',
            'label_ptr': '',
            'description': '',
            'description_ptr': '',
            'permission_group': '',
            'protection_level': p.attributes['android:protectionLevel'].value.encode('utf-8').decode('utf-8')
        }
        if p.hasAttribute('android:label'):
            permissions[name]['label_ptr'] = p.attributes['android:label'].value.replace('@string/', '')
        if p.hasAttribute('android:description'):
            permissions[name]['description_ptr'] = p.attributes['android:description'].value.replace('@string/', '')
        if p.hasAttribute('android:permissionGroup'):
            permissions[name]['permission_group'] = p.attributes['android:permissionGroup'].value
            
    return permissions


def extract_permission_groups(aosp_root_dir):
    groups = {}
    manifest = os.path.join(aosp_root_dir, 'core/res/AndroidManifest.xml')
    xml = parse(manifest)
    group_elements = xml.getElementsByTagName('permission-group')

    for g in group_elements:
        name = str(g.attributes['android:name'].value)
        groups[name] = {
            'name': name,
            'request_ptr': str(g.attributes['android:request'].value.replace('@string/', '')),
            'description': '',
            'description_ptr': '',
            'label': '',
            'label_ptr': '',
            'icon': '',
            'icon_ptr': '',
        }
        if g.hasAttribute('android:label'):
            groups[name]['label_ptr'] = g.attributes['android:label'].value.replace('@string/', '')
        if g.hasAttribute('android:description'):
            groups[name]['description_ptr'] = g.attributes['android:description'].value.replace('@string/', '')
        if g.hasAttribute('android:icon'):
            groups[name]['icon_ptr'] = g.attributes['android:icon'].value.replace('@drawable/', '')
    
    return groups


def extract_drawable(aosp_root_dir, elements):
    for e in elements:
        if 'icon_ptr' in elements[e]:
            drawable_file = os.path.join(aosp_root_dir, 'core/res/res/drawable/', '{}.xml'.format(elements[e]['icon_ptr']))
            if os.path.isfile(drawable_file):
                svg = convertVd(drawable_file)
                elements[e]['icon'] = svg

    return elements


def _clean_string(s):
    s = s.replace('"', '').replace('\\', '')
    return str(s)


def extract_string_prt(translation_file, elements):
    xml = parse(translation_file)
    translations = xml.getElementsByTagName('string')

    for t in translations:
        for p in elements:
            if elements[p]['label_ptr'] == t.attributes['name'].value:
                elements[p]['label'] = _clean_string(t.firstChild.nodeValue)
            if elements[p]['description_ptr'] == t.attributes['name'].value:
                elements[p]['description'] = _clean_string(t.firstChild.nodeValue)

    return elements


def gen_html(elements, file_name):
    groups = elements['groups']
    permissions = elements['permissions']
    with open(file_name, 'w') as h:
        h.write('<html>\n')
        h.write('<style>body{font-family: monospace;}</style>\n')
        h.write('<h1>Permissions groups</h1>\n')
        for g in groups:
            h.write('<div>\n')
            h.write('{}\n'.format(groups[g]['icon']))
            h.write('<ul>\n')
            h.write('<li>Label: {}</li>\n'.format(groups[g]['label']))
            h.write('<li>Description: {}</li>\n'.format(groups[g]['description']))
            h.write('</ul>\n')
            h.write('</div>\n')
        h.write('<h1>Permissions</h1>\n')
        for g in permissions:
            h.write('<div>\n')
            h.write('<h2>{}</h2>\n'.format(permissions[g]['name']))
            h.write('<ul>\n')
            h.write('<li>Label: {}</li>\n'.format(permissions[g]['label']))
            h.write('<li>Description: {}</li>\n'.format(permissions[g]['description']))
            h.write('<li>Group: {}</li>\n'.format(permissions[g]['permission_group']))
            h.write('<li>Protection level: {}</li>\n'.format(permissions[g]['protection_level']))
            h.write('</ul>\n')
            h.write('</div>\n')
        h.write('</html>\n')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print('python extract.py <AOSP root dir> <2-letter locale> <output dir>')
        sys.exit(1)

    aosp_root_dir = sys.argv[1]
    locale = sys.argv[2]
    output_dir = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    translation_file = os.path.join(aosp_root_dir, 'core/res/res/values-{}/strings.xml'.format(locale))
    if locale == 'en':
        translation_file = os.path.join(aosp_root_dir, 'core/res/res/values/strings.xml'.format(locale))
    if not os.path.isfile(translation_file):
        print('Locale file not found: {}'.format(translation_file))
        sys.exit(1)

    permissions = extract_permissions(aosp_root_dir)
    permissions = extract_string_prt(translation_file, permissions)

    groups = extract_permission_groups(aosp_root_dir)
    groups = extract_string_prt(translation_file, groups)
    groups = extract_drawable(aosp_root_dir, groups)

    definitions = {
        'groups': groups,
        'permissions': permissions
    }

    html_file = os.path.join(output_dir, 'permissions-{}.html'.format(locale))
    json_file = os.path.join(output_dir, 'permissions-{}.json'.format(locale))

    gen_html(definitions, html_file)

    with open(json_file, 'w') as j:
        json.dump(definitions, j, indent=2, sort_keys=True, ensure_ascii=False)