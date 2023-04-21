# audio_subliminal_msgs

Summary:

This is an attempt to display text with varying transparency based on the frequencies in a song

Details:

The script sub_msgs.py as of now reads a file named "output.wav" in the same folder, and displays
 text that is input in the Qt app's input window (top one as of now), with varying transparency
 based on the frequency of the section of the audio

This needs to be modified further

Additional files:

gen_wave.py: generates a wave of specified frequency

join.py: merges two waves

NOTE: In the below scripts, messages are displayed when <RETURN> key is pressed

sub_msgs_live.py: Script to display subliminal messages synced with a live recording
                   Has both single character and complete message display options
                   
sub_msgs_timebased.py: Script to display subliminal messages as single character in a location on the window, and with
 varying time gaps
 
sub_msgs_timebased_multiple_cols.py: Script to display subliminal messages as single character, one in each small box in a sequence of boxes, and shifted in index based on tesla technique

sub_msgs_gap.py: Script to display messages with varying gaps while typing (to send the message to higher dimension)

sub_msgs_enlarge.py: Script to display message typed, in a repeated way, with varying gaps

