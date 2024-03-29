#!/usr/bin/env python
import os
import argparse
import yaml
import re
import json
import marko
import re
from marko.ast_renderer import ASTRenderer
from marko import Markdown
import sys
import knittingneedles as knit


replacements = {
    '%%sq%%': "'",
    '%%dq%%': '"',
    '%%sp%%': ' ',
}


def dataKv(line):
    for m in re.findall('(?P<k>data-[a-z-]*)="(?P<v>[^"]*)"', line):
        text = m[1].strip('"')
        for k, v in replacements.items():
            text = text.replace(k, v)
        yield (m[0][5:], text)

def fixspoken(kids):
    text = ""
    for y in kids:
        if y['element'] != 'paragraph':
            continue

        for x in y['children']:
            if x['element'] == 'raw_text' and x['children'][0:2] != '{:':
                text += x['children']
            elif x['element'] == 'line_break':
                text += ' '
        text += ' '

    text = re.sub('\s+', ' ', text)
    meta = {'type': 'spoken', 'text': text.strip()}
    meta.update({'data': dict(dataKv(kids[-1]['children'][-1]['children']))})
    return meta

def fixcommit(a, b):
    code = a['children'][0]['children']
    # Remove endraw at end
    code = code.strip().split('\n')
    if code[-1] == '{% endraw %}':
        code = code[:-1]
    code = '\n'.join(code)

    meta = {'type': 'code', 'code': code}
    meta.update({'data': dict(dataKv(b))})
    meta['data']['visual'] = 'terminal'
    return meta

def fixcmd(a, b):
    code = a['children'][0]['children']
    meta = {'type': 'cmd', 'cmd': code.strip()}
    meta.update({'data': dict(dataKv(b))})
    meta['data']['visual'] = 'terminal'
    return meta

def emit(d, i=0):
    # Spoken Text
    if d['element'] == 'quote':
        # print('FOUND')

        # We guard access in try/except
        try:
            kid = d['children'][-1]['children'][-1]
        except:
            kid = None

        # In order to not hide errors of actual access
        if kid is not None and kid['element'] == 'raw_text':
            # print('HERE')
            lastkid = kid['children']
            # print(lastkid)
            if '.spoken' in lastkid:
                yield fixspoken(d['children'])

    # Code blocks (commits)
    if 'children' in d and isinstance(d['children'], list):
        for idx, x in enumerate(d['children']):
            # print(idx, x)
            if x['element'] == 'fenced_code':
                try:
                    # admin tutorials have codeblocks
                    if idx + 1 < len(d['children']):
                        nk = d['children'][idx + 1]['children'][0]['children']
                        if 'data-commit' in nk:
                            yield fixcommit(x, nk)
                        elif 'data-cmd' in nk:
                            yield fixcmd(x, nk)
                except KeyError:
                    # Non-admin don't.
                    pass

    if 'children' in d and isinstance(d['children'], list):
        for child in d['children']:
            # print(f'emit {child}')
            yield from emit(child, i=i+1)


def mergeRefSteps(it):
    # This is fundamentally a sort/collapse problem
    steps = list(it)
    non_text_steps = {
        x['data']['ref']: x
        for x in steps
        if 'text' not in x
    }
    text_steps = [
        x for x in steps
        if 'text' in x
    ]
    for step in text_steps:
        ref = step.get('data', {}).get('ref', None)
        if ref:
            refstep = non_text_steps[ref]
            newstep = {}
            newstep.update(step)
            newstep.update(refstep) # This clobbers some entries like [data, type].
            newstep['type'] = (step['type'], refstep['type'])
            # But it's fine data is clobbered, they should be roughly identical except for data.commit.
            del newstep['data']['ref']

            yield newstep
        else:
            yield step

def reduceSteps(it):
    seen = []
    out = []
    for step in it:
        # print(step)
        if 'ref' in step['data']:
            ref = step['data']['ref']
            if ref not in seen:
                out.append(step)
                seen.append(ref)
            else:
                twin = [x for x in out if x['data'].get('ref', None) == ref][0]
                # the voiced bit always comes after??
                twin['text'] = step['text']
                twin['type'] = [ twin['type'], step['type'] ]
                del twin['data']['ref']
        else:
            out.append(step)
    return out


def process(text: list):
    # Parse out the markdown header
    if text[-1] != '\n':
        raise Exception("lines must end in \n like readlines() output")
    if text[0].strip() != '---':
        raise Exception("markdown file must start with --- for the metadata block.")
    text = text[1:]
    meta = text[:text.index('---\n')]
    text = text[text.index('---\n') + 1:]
    text = ''.join(text)
    meta = ''.join(meta)
    meta = yaml.safe_load(meta)

    # Alternatively, you can register extensions later.
    markdown = Markdown(renderer=ASTRenderer)
    data = markdown(text)

    output = {'meta': {k: v for k, v in meta.items() if k in ('title', 'contributors', 'voice')}}
    output['steps'] = []
    for x in mergeRefSteps(emit(data)):
        output['steps'].append(x)

    return output

if __name__ == '__main__':
    # read in a tutorial, and check the structure of it.
    parser = argparse.ArgumentParser(
        description="Extract a 'script' from a tutorial with commits, commands, and more."
    )
    parser.add_argument("tutorial", type=argparse.FileType("r"), help="Input tutorial")
    args = parser.parse_args()
    text = args.tutorial.read().split('\n')
    text = [x + '\n' for x in text]
    print(yaml.dump(process(text)))
