import click
import glob
import gzip
import json
import os
import pandas


# TODO:
# - fix concert pitch
# - fix octave index


CP = 443  # TODO: fix concert pitch
C0 = 2 ** (-(9 + 4*12) / 12)
SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def frequency(note, octave, precision=2):

    c0 = C0 * CP
    semitone = SCALE.index(note)

    return round(2 ** (semitone / 12 + octave) * c0, precision)


def decode(file):

    name, ext = os.path.splitext(os.path.basename(file))
    attrs = name.split('_')
    assert len(attrs) == 5

    instrument = attrs[0]
    note = attrs[1][:-1]
    octave = attrs[1][-1:]
    length = attrs[2]
    dynamic = attrs[3]
    style = attrs[4]

    percussion = not (note and octave)

    if percussion:
        note = None
        octave = None
        pitch = None
    else:
        note = note[:-1] + '#' if note.endswith('s') else note
        octave = int(octave) - 1  # TODO: fix octave index
        pitch = frequency(note, octave)

    file = dict(file=file,
                name=name,
                instrument=instrument,
                percussion=percussion,
                note=note,
                octave=octave,
                pitch=pitch,
                length=length,
                dynamic=dynamic,
                style=style)

    return file


def sync(fileroot='data', filepattern='*.mp3'):

    query = os.path.join(fileroot, '**', filepattern)

    files = glob.glob(query, recursive=True)
    files = [decode(file) for file in files]

    print(f'found {len(files)} {filepattern} files in {fileroot} directory')

    return files


def philharmonia():

    zip = True
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file = os.path.join(root, 'data' + ('.json.zip' if zip else '.json'))

    if zip:

        with gzip.open(file, 'rt', encoding='ascii') as file:

            data = pandas.read_json(file)

    else:

        data = pandas.read_json(file)

    return data


@click.command('data', help='Browse the Philharmonia Orchestra sound samples.', no_args_is_help=False, context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-u', '--update', is_flag=True, default=False, help='Sync sound sample database.')
@click.option('-c', '--columns', is_flag=True, default=False, help='List available table columns.')
@click.option('-s', '--sort', multiple=True, help='Column names to sort by.')
@click.option('-f', '--filter', multiple=True, help='Column names to filter.')
@click.option('-o', '--output', default='string', show_default=True, help='Print query results as csv, html, json or markdown.')
@click.argument('query', nargs=-1)
def main(update, columns, sort, filter, output, query):

    zip = True
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file = os.path.join(root, 'data' + ('.json.zip' if zip else '.json'))

    if update:

        data = sync(root)

        print(f'updating {file}')

        if zip:

            with gzip.open(file, 'wt', encoding='ascii') as file:

                json.dump(data, file, ensure_ascii=True)

        else:

            with open(file, 'w', encoding='ascii') as file:

                json.dump(data, file, indent=2, ensure_ascii=True)

        return

    if zip:

        with gzip.open(file, 'rt', encoding='ascii') as file:

            data = pandas.read_json(file)

    else:

        data = pandas.read_json(file)

    if columns:

        for column in list(data):

            print(column)

        return

    if query:

        query = ','.join(map(str, query))
        data = data.query(query)

    if sort:

        data = data.sort_values(by=list(sort))

    if filter:

        data = data.filter(items=list(filter))

    print(getattr(data, f'to_{output}')())


if __name__ == '__main__':

    main()
