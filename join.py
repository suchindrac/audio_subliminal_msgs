from pydub import AudioSegment
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-1", "--first", required=True, type=str, help="The first wave")
parser.add_argument("-2", "--second", required=True, type=str, help="The second wave")
parser.add_argument("-0", "--output", required=True, type=str, help="The output file")

args = parser.parse_args()

waves = [args.first, args.second]

sound1 = AudioSegment.from_file(args.first)
sound2 = AudioSegment.from_file(args.second)

combined = sound1.overlay(sound2)

combined.export(args.output, format='wav')
