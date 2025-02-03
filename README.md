# timewarrior-tagsum

timewarrior extension that prints the total length of time spent on each of the selected tags in the selected time frame.

## Prerequisites

* Python >= 3.9

## Installation

1. Identify the timewarrior extensions directory by running `timew extensions`.
   Per default, the path should be `~/.config/timewarrior/extensions`.
2. Copy `tagsum.py` from this repository to your extensions directory and make sure it's executable.
   If your extensions directory is set to default, you can use the following command:

   ```console
   curl https://raw.githubusercontent.com/danteu/timewarrior-tagsum/main/tagsum.py > ~/.config/timewarrior/extensions/tagsum.py && \
   chmod +x ~/.config/timewarrior/extensions/tagsum.py
   ```
3. When you run `timew extensions` again, it should now list `tagsum.py` as an active extension.

## Usage

```console
timew tagsum [range] [tag]
```

### Example

```console
~ timew summary :ids

Wk  Date       Day ID Tags           Start      End    Time   Total
W16 2022-04-23 Sat @3 First Task   9:00:00 11:00:00 2:00:00
                   @2 Second Task 11:00:00 12:30:00 1:30:00
                   @1 First Task  13:25:42        - 4:00:02 7:30:02

                                                            7:30:02

~ timew tagsum today
First Task  -- 6:00:02
Second Task -- 1:30:00

Total       -- 7:30:02
```
