#!/usr/bin/env ruby
require 'json'

def timefmt(t, fmt)
  seconds = (t / 1000) % (24 * 3600)
  hours = seconds.to_i / 3600
  seconds = seconds % 3600
  minutes = seconds.to_i / 60
  seconds = seconds % 60
  (seconds, ms) = seconds.divmod(1)
  seconds = seconds
  ms = 1000 * ms

  if fmt == "vtt"
    "%02d:%02d:%02d.%03d" % [hours, minutes, seconds, ms]
  else
    "%02d:%02d:%02d,%03d" % [hours, minutes, seconds, ms]
  end
end

offset = 0
data = JSON.load(File.open(ARGV[0], 'r'))
results = []
data.each{|delay, meta|
  offset += delay

  #puts "#{offset / 1000} #{meta['text'][0..30]}"
  results.push({
    "start" => offset,
    "text" => meta['text'],
    "end" => offset + meta['mediameta']['end'] * 1000
  })
  offset += meta['mediameta']['end'] * 1000
}


def split_sentence(sentence, timing)
  split_sentence = sentence.split(' ')
  spaces = sentence.count(" ")

  # Assumes roughly uniform word length.
  parts = 1 + (spaces / 16)
  part_off = spaces / parts

  o = 0
  tacc = 0

  range = (0..parts).to_a
  results = []

  range.each{|i|
    if i == parts
        results.push([
          split_sentence[o..-1].join(' '),
          tacc,
          tacc + timing / parts
        ])
    else
        results.push([
          split_sentence[o..o + part_off - 1].join(' '),
          tacc,
          tacc + timing / parts
        ])
    end
    o += part_off
    tacc += timing / parts
  }
  return results
end

results = results.map{|item|
  split_sentence(item['text'], item['end'] - item['start']).map{|split, start, endd|
    {
      "start" => item['start'] + start,
      "end" => item['start'] + endd,
      "text" => split
    }
  }
}.flatten

output = File.open(ARGV[1], 'w')
results.each_with_index{|x, idx|
  output.write("#{idx + 1}\n")
  output.write("#{timefmt(x['start'], 'srt')} --> #{timefmt(x['end'], 'srt')}\n")
  output.write("#{x['text']}\n")
  output.write("\n")
}
output.close
