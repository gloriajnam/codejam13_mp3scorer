def process_music():
  print('Loading core modules. Please wait...')

  import os
  import statistics, math

  print('Loading TMIDIX module...')

  # os.chdir('/content/Melody-Master/')
  import TMIDIX

  # os.chdir('/content/')
  print('Done!')

  """# (MELODY MASTER)"""

  #@title Extract melody
  full_path_to_MIDI_file = "raw_music.mid" #@param {type:"string"}
  composition_time_resolution = 10 #@param {type:"slider", min:1, max:100, step:1}
  mono_melody_or_chorded_melody = False #@param {type:"boolean"}
  add_bass_melody = False #@param {type:"boolean"}
  mono_or_chorded_bass_melody = False #@param {type:"boolean"}
  melody_curve_type = "melody" #@param ["melody", "composition", "bass"]
  use_relative_melody_curve = False #@param {type:"boolean"}
  relative_melody_curve_in_notes = 128 #@param {type:"slider", min:8, max:256, step:8}

  print('=' * 70)
  print('Melody Master')

  print('=' * 70)
  print('Loading MIDI file...')


  score = TMIDIX.midi2ms_score(open("uploads/" +full_path_to_MIDI_file, 'rb').read())

  events_matrix = []

  itrack = 1

  while itrack < len(score):
      for event in score[itrack]:
        if event[0] == 'note' and event[3] != 9:
          events_matrix.append(event)
      itrack += 1

  for e in events_matrix:
    e[1] = math.ceil(e[1] / composition_time_resolution)

  # Sorting...
  events_matrix.sort(key=lambda x: x[4], reverse=True)
  events_matrix.sort(key=lambda x: x[1])

  melody_chords = []
  cho = []
  pe = events_matrix[0]
  for e in events_matrix:
    if e[1] - pe[1] == 0:
      cho.append(e)
    else:
      if len(cho) > 0:
        melody_chords.append(cho)
      cho = []
      cho.append(e)

    pe = e # Previous event

  print('=' * 70)
  print('Processing...')

  #==================================================

  time = [y[0][1] for y in melody_chords]

  melody_pitches = [y[0][4] for y in melody_chords]
  composition_pitches = [y[4] for y in events_matrix]
  bass_pitches = [y[-1][4] for y in melody_chords if len(y) > 1]

  relative_melody_pitches = melody_pitches

  relative_composition_pitches = []
  for m in melody_chords:
    relative_composition_pitches.append(statistics.mean([y[4] for y in m]))

  relative_bass_pitches = []
  for m in melody_chords:
    relative_bass_pitches.append(m[-1][4])

  mean_melody_pitch = statistics.mean(melody_pitches)
  mean_composition_pitch = statistics.mean(composition_pitches)
  mean_bass_pitch = statistics.mean(bass_pitches)

  #==================================================

  melody_curve = []

  relative_curve_step = round(relative_melody_curve_in_notes / 2)

  if melody_curve_type == 'melody':
    if use_relative_melody_curve:
      for i in range(len(melody_chords)):
        melody_curve.append(statistics.mean([melody_pitches[i], statistics.mean(relative_melody_pitches[max(0, i-relative_curve_step):i+relative_curve_step])]))

    else:
      for i in range(len(melody_chords)):
        melody_curve.append(statistics.mean([melody_pitches[i], mean_melody_pitch]))

  if melody_curve_type == 'composition':
    if use_relative_melody_curve:
      for i in range(len(melody_chords)):
        melody_curve.append(statistics.mean([melody_pitches[i], statistics.mean(relative_composition_pitches[max(0, i-relative_curve_step):i+relative_curve_step])]))

    else:
      for i in range(len(melody_chords)):
        melody_curve.append(statistics.mean([melody_pitches[i], mean_composition_pitch]))

  if melody_curve_type == 'bass':
    if use_relative_melody_curve:
      for i in range(len(melody_chords)):
        melody_curve.append(statistics.mean([melody_pitches[i], statistics.mean(relative_bass_pitches[max(0, i-relative_curve_step):i+relative_curve_step])]))

    else:
      for i in range(len(melody_chords)):
        melody_curve.append(statistics.mean([melody_pitches[i], mean_bass_pitch]))

  #==================================================

  if mono_melody_or_chorded_melody:
    for i in range(len(melody_chords)):
      if melody_chords[i][0][4] > melody_curve[i]:
        melody_chords[i][0][3] = 0
        for m in melody_chords[i][1:]:
          if add_bass_melody and m[4] < mean_bass_pitch:
            if not mono_or_chorded_bass_melody:
              m[3] = 2
            else:
              m[3] = 1
          else:
            m[3] = 1
      else:
        for m in melody_chords[i]:
          if add_bass_melody and m[4] < mean_bass_pitch:
            if not mono_or_chorded_bass_melody:
              m[3] = 2
            else:
              m[3] = 1
          else:
            m[3] = 1

      if add_bass_melody and mono_or_chorded_bass_melody:
        if melody_chords[i][-1][4] < mean_bass_pitch:
          melody_chords[i][-1][3] = 2

  else:
    for i in range(len(melody_chords)):
      if melody_chords[i][0][4] > melody_curve[i]:
        for m in melody_chords[i]:
          if m[4] > melody_curve[i]:
            m[3] = 0
          else:
            if add_bass_melody and m[4] < mean_bass_pitch:
              if not mono_or_chorded_bass_melody:
                m[3] = 2
              else:
                m[3] = 1
            else:
              m[3] = 1
      else:
        for m in melody_chords[i]:
          if add_bass_melody and m[4] < mean_bass_pitch:
            if not mono_or_chorded_bass_melody:
              m[3] = 2
            else:
              m[3] = 1
          else:
            m[3] = 1

      if add_bass_melody and mono_or_chorded_bass_melody:
        if melody_chords[i][-1][4] < mean_bass_pitch:
          melody_chords[i][-1][3] = 2
  #==================================================
  print('=' * 70)

  melody_chords_f = []

  for m in melody_chords:
    melody_chords_f.extend(m)

  for m in melody_chords_f:
    m[1] = m[1] * composition_time_resolution

  TMIDIX.Tegridy_SONG_to_MIDI_Converter(melody_chords_f,
                                        output_signature='Melody Master',
                                        track_name='Project Los Angeles',
                                        number_of_ticks_per_quarter=500,
                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0],
                                        output_file_name='processed_music/processed_music.mid')

  print('=' * 70)
  print('Enjoy! :)')
  print('=' * 70)
  print(melody_chords)
  return melody_chords


